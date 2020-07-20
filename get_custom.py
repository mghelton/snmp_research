''''
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('192.168.61.6', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('LUXL-POE-MIB', 'luxlPoeStatusInterfaceCurrentState', 1000002).addAsn1MibSource('file:///Users/michaelhelton/Downloads/LUXL_MIBs_ALL/LUXL-POE-MIB.mib')))
)

print(errorIndication)
print(errorStatus)
print(errorIndex)
print(varBinds)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
'''

from pysnmp.hlapi import *
import sys

#errorIndication, errorStatus, errorIndex, varBinds = next(
g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('192.168.61.6', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('IF-MIB', 'ifDescr').addAsn1MibSource('file:///Users/michaelhelton/Downloads/mibBrowser/IF-MIB')))
'''
)
print(errorIndication)
print(errorStatus)
print(errorIndex)
print(varBinds)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
'''
print(g)
for i in g:
    print(i)
while True:
    try:
        for var in next(g)[3]:
            pretty = ' = '.join([x.prettyPrint() for x in var])
            print(pretty)
            #if("ifIndex" in pretty):
            #    print(pretty)
            #else:
            #    sys.exit()
    except Exception as e:
        print(type(e).__name__,e.args)
        sys.exit()