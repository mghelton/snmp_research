
from pysnmp.hlapi import *
g = getCmd(SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('192.168.61.6', 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)))
gen = next(g)
for item in gen:
    if(isinstance(item,list)):
        print([x.prettyPrint() for x in item])

'''
from pysnmp.hlapi import *

for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
                          CommunityData('public'),
                          UdpTransportTarget(('192.168.61.6', 161)),
                          ContextData(),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.1.100000')),
                          lookupMib=False):

    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break
    else:
        for varBind in varBinds:
            for x in varBind:
                print(x)
            print(' = '.join([x.prettyPrint() for x in varBind]))
'''

