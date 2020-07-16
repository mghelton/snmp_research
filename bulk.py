from pysnmp.hlapi import *

for errorIndication, errorStatus, \
    errorIndex, varBinds in bulkCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('192.168.61.6', 161)),
        ContextData(),
        0, 50,  # GETBULK specific: request up to 50 OIDs in a single response
        ObjectType(ObjectIdentity('IF-MIB', 'ifIndex').addAsn1MibSource('file:///Users/michaelhelton/Downloads/mibBrowser/IF-MIB')),
        lookupMib=False, lexicographicMode=False):

    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
        break
    else:
        for varBind in varBinds:
            
            print(' = '.join([x.prettyPrint() for x in varBind]))