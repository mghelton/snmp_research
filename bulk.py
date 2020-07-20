from pysnmp.hlapi import *

ignore = '1.3.6.1.2.1.17.4.3.1.2.'

l = []
switch = '192.168.61.6'
for errorIndication, errorStatus, \
    errorIndex, varBinds in bulkCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((switch, 161)),
        ContextData(),
        0, 100,  # GETBULK specific: request up to 50 OIDs in a single response
        #ObjectType(ObjectIdentity('BRDIGE-MIB', 'dot1dTpFdbAddress').addAsn1MibSource('./mibBrowser/BRIDGE-MIB')),
        ObjectType(ObjectIdentity('BRIDGE-MIB','dot1dTpFdbPort')),
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
            stringed = str(varBind[0]).replace(ignore,"")
            stringed = stringed.split(".")
            print(stringed)
            l.append(':'.join([hex(int(i))[2:] for i in stringed]))
            #for x in varBind:
            #    print(x)
            #l.append(varBind[0].replace(ignore,""))
            #l.append(' = '.join([x.prettyPrint() for x in varBind]))
l.pop(0) #remove root oid
for i in range(len(l)):
    print(i+1,l[i])
