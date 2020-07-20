from pysnmp.hlapi import *

ignore = '1.3.6.1.2.1.17.4.3.1.2.'

l = []
'''
m = {
    "0":[],
    "1":[],
    "2":[],
    "3":[],
    "4":[],
    "5":[],
    "6":[],
    "7":[],
    "8":[],
    "9":[],
    "10":[],
    "11":[],
    "12":[]
}
'''

m = {}

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
            #for x in varBind:
            #    print(x)
            #l.append(varBind[0].replace(ignore,""))
            #l.append(' = '.join([x.prettyPrint() for x in varBind]))
#l.pop(0) #remove root oid
#for i in range(len(l)):
#    print(i+1,l[i])


for port,addr in m.items():
    print(port," - ",addr)
