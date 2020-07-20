from pysnmp.hlapi import *
from helpers import parse_kwargs

class Switch():
    def get_bulk(self,_MIB: str,_OID: str):
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
                print(errorIndication)   
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            else:
                for varBind in varBinds:
                    l.append(varBind)
        return l

class luxul(Switch):
    def __init__(self,**kwargs):
        required = {'ip':{'type':str,'state':False},'snmp_port':{'type':int,'state':False},'snmp_trap_port':{'type':int,'state':False}}
        success,error = parse_kwargs(required,kwargs)
        if(success):
            self.__dict__.update(kwargs)
            self.mac_table = {}
        else:
            print("ERROR: {}".format(error))

    def update_poe_status(self):
        pass

    def update_mac_table(self,**kwargs):
        #set join character, default to colon
        try: join_char = kwargs['join_character'] 
        except KeyError: join_char = ":"
        
        m = {}
        ignore = '1.3.6.1.2.1.17.4.3.1.2.' #OID prefix to ignore for mac address parsing

        varBinds = self.get_bulk('BRIDGE-MIB','dot1dTpFdbPort')
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

    def control_poe(self):
        pass

    def control_port(self):
        pass