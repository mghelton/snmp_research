'''
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    setCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('192.168.61.6', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('LUXL-POE-MIB', 'luxlPoeConfigInterfaceParamMode', 1000001).addAsn1MibSource('file:///Users/michaelhelton/Downloads/LUXL_MIBs_ALL/LUXL-POE-MIB.mib'),2))
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

from pysnmp.hlapi import *
from pysnmp.hlapi import UsmUserData

errorIndication, errorStatus, errorIndex, varBinds = next(
    setCmd(SnmpEngine(),
           UsmUserData('user',authKey='password'),
           UdpTransportTarget(('192.168.61.6', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('LUXL-POE-MIB', 'luxlPoeConfigInterfaceParamMode', 1000001).addAsn1MibSource('file:///Users/michaelhelton/Downloads/LUXL_MIBs_ALL/LUXL-POE-MIB.mib'),2))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))