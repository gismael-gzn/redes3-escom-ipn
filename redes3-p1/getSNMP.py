from pysnmp.hlapi import *
import re
import binascii

def consultaSNMP(comunidad:str,host:str,oid:str, port:str):
    comunidad = str(comunidad)
    host = str(host)
    oid = str(oid)
    port = int(port)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split('= ')[1]
            hx = re.compile('0x')
            if hx.match(resultado) != None: 
                resultado = resultado.strip('0x')
                resultado = binascii.unhexlify(resultado)
                resultado = resultado.decode('utf-8')
    return resultado

#print(consultaSNMP("comunidadSNMP","localhost","1.3.6.1.2.1.1.1.0"))