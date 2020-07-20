from pysnmp.hlapi import *
from helpers import parse_kwargs

class Switch():
    def bulk(self,mib,oid):
        l = []
        for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((self.ip,self.snmp_port)),
            ContextData(),
            0,100, #GETBULK specific request up to 100 OIDs in a single response
            ObjectType(ObjectIdentity(mib,oid)),
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
        print(self.__dict__)

    def update_mac_table(self):
        m = {}
        ignore = '1.3.6.1.2.1.17.4.3.1.2.' #OID prefix to ignore for mac address parsing
        varBinds = self.bulk('BRIDGE-MIB','dot1dTpFdbPort')
        for varBind in varBinds:
            stringed = str(varBind[0]).replace(ignore,"")
            stringed = stringed.split(".")
            index = str(varBind[1])
            def convert(value):
                hexVal = hex(int(value))[2:]
                if(len(hexVal) == 1):
                    return "0"+hexVal
                else:
                    return hexVal        
            try:
                 m[index].append('-'.join([convert(i) for i in stringed]))
            except KeyError:
                m[index] = []
                m[index].append('-'.join([convert(i) for i in stringed]))
            except Exception as e:
                print(type(e).__name__,e.args)
        if(m):
            self.mac_table.update(m)
            return True
        else:
            return False