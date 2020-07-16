from pysnmp.hlapi import *
g = setCmd(SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('192.168.61.6', 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0),'test'))
gen = next(g)
print(gen[3])
