from pysnmp.hlapi import *
g = getCmd(SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('192.168.61.6', 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)))
gen = next(g)
print(gen[3])
for item in gen[3]:
    print(item)