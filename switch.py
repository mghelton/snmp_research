from pysnmp.hlapi import *
from pysnmp.hlapi import UsmUserData
from helpers import parse_kwargs
from logg3r import Log

class SNMP():
    def SNMP_set_state(self,_MIB: str,_OID: str,_PORT: int, _STATE: int):
        l = []
        errorIndication, errorStatus, errorIndex, varBinds = next(
            setCmd(SnmpEngine(),
                UsmUserData(self.snmp_username,authKey=self.snmp_password),
                UdpTransportTarget((self.ip, self.snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity('LUXL-POE-MIB', 'luxlPoeConfigInterfaceParamMode', _PORT),_STATE))
        )

        if errorIndication:
            self.logger.log("GET_BULK: errorIndicaton | {}".format(errorIndication),5)
        elif errorStatus:
            self.logger.log("GET_BULK: errorStatus | {} at {}".format(errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'),5)
        else:
            for varBind in varBinds:
                l.append(varBind)
        return l

    def SNMP_get_one(self,_MIB: str,_OID: str, _INT: int):
        g = getCmd(SnmpEngine(),
                    CommunityData('public'),
                    UdpTransportTarget((self.ip,self.snmp_port)),
                    ContextData(),
                    ObjectType(ObjectIdentity(_MIB, _OID, _INT)))
        gen = next(g)
        for item in gen:
            if(isinstance(item,list)):
                return [x.prettyPrint() for x in item][0].split("=")[1].strip()

    def SNMP_get_bulk(self,_MIB: str,_OID: str):
        l = []
        for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((self.ip,self.snmp_port)),
            ContextData(),
            0,100, #GETBULK specific request up to 100 OIDs in a single response
            ObjectType(ObjectIdentity(_MIB,_OID)),
            lookupMib=False,lexicographicMode=False):

            if errorIndication:
                self.logger.log("GET_BULK: errorIndicaton | {}".format(errorIndication),5)
                break
            elif errorStatus:
                self.logger.log("GET_BULK: errorStatus | {} at {}".format(errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'),5)
            else:
                for varBind in varBinds:
                    l.append(varBind)
        return l

class Switch(SNMP): #not meant to be used standalone. Inherit to sub switch classes
    def __init__(self):
        super(Switch,self).__init__()
        self.mac_table = {}
        self.interface_status = {}
    
    def update_interface_status(self,**kwargs):
        s = {}
        translate = {"1":"up","2":"down"}
        varBinds = self.SNMP_get_bulk('IF-MIB','ifOperStatus')

        index = -1
        for varBind in varBinds:
            index += 1
            try:
                s[str(index)] = translate[varBind[1].prettyPrint()]
            except Exception as e:
                print(type(e).__name__,e.args)
        if(s):
            del s['0']
            self.interface_status.update(s)
            return True
        else: return False

    def update_mac_table(self,**kwargs):
        #set join character, default to colon
        try: join_char = kwargs['join_character'] 
        except KeyError: join_char = ":"
        
        m = {}
        ignore = '1.3.6.1.2.1.17.4.3.1.2.' #OID prefix to ignore for mac address parsing

        varBinds = self.SNMP_get_bulk('BRIDGE-MIB','dot1dTpFdbPort')
        for varBind in varBinds:
            index = str(varBind[1])
            addr = str(varBind[0]).replace(ignore,"").split(".")
            def convert(value):
                hexVal = hex(int(value))[2:]
                if(len(hexVal) == 1): return "0"+hexVal
                else: return hexVal.lower()
            try:
                 m[index].append(join_char.join([convert(i) for i in addr]))
            except KeyError:
                m[index] = [] #initialize key
                m[index].append(join_char.join([convert(i) for i in addr]))
            except Exception as e:
                print(type(e).__name__,e.args)
        if(m):
            self.mac_table.update(m)
            return True
        else: return False

class Luxul(Switch):
    def __init__(self,**kwargs):
        required = {'uid':{'type':str,'state':False},
                    'ip':{'type':str,'state':False},
                    'snmp_port':{'type':int,'state':False},
                    'snmp_trap_port':{'type':int,'state':False},
                    'snmp_username':{'type':str,'state':False},
                    'snmp_password':{'type':str,'state':False}
        }
        success,error = parse_kwargs(required,kwargs)
        if(success):
            self.__dict__.update(kwargs)
            super(Luxul,self).__init__()
            self.logger = Log(log_path="./logs/",name='luxul_'+self.__dict__['uid'],level=1)
            self.logger.log("object initialized",1)
        else:
            print("ERROR: {}".format(error))

    def update_poe_status(self):
        varBinds = self.SNMP_get_bulk('LUXL-POE-MIB','luxlPoeStatusInterfaceCurrentState')
        join_char = " - "
        for varBind in varBinds:
            print(join_char.join([x.prettyPrint() for x in varBind]))

    def control_poe(self,_PORT: int,_STATE: int):
        # _STATE
        # 0 = disabled
        # 1 = PoE
        # 2 = PoE+

        if(len(str(_PORT)) == 1):
            _PORT = int("100000"+str(_PORT))
        elif(len(str(_PORT)) == 2):
            _PORT = int("10000"+str(_PORT))
        
        varBinds = self.SNMP_set_state('LUXL-POE-MIB','luxlPoeConfigInterfaceParamMode',_PORT,_STATE)
        join_char = " - "
        for varBind in varBinds:
            print(join_char.join([x.prettyPrint() for x in varBind]))
        '''
        errorIndication, errorStatus, errorIndex, varBinds = next(
            setCmd(SnmpEngine(),
                UsmUserData(self.snmp_username,authKey=self.snmp_password),
                UdpTransportTarget((self.ip, self.snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity('LUXL-POE-MIB', 'luxlPoeConfigInterfaceParamMode', _PORT),_STATE))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
        '''

    def control_port(self):
        pass