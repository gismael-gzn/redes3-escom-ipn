import time
import rrdtool
from getSNMP import consultaSNMP

from sys import argv

from bundle import bundle as cat

# rrdpath = '/home/dio/school/Introduccion_SNMP/6-AdministraciónDeRendimiento/RRD/'

def query(RRD_FILEPATH:str, SLEEP_TIME:int, SNMP_COMMUNITY:str, HOST:str, OID:str, RSRC_NAME:str):
    load = 0
    while 1:

        doOnce = False

        if(doOnce == False):
            doOnce = True
            fixed_ram = int(consultaSNMP(SNMP_COMMUNITY, HOST, cat.oid.ram_fixed))

        match RSRC_NAME:
            case cat.cpu_rsrc:
                load = int(consultaSNMP(SNMP_COMMUNITY, HOST, cat.oid.cpu))
            case cat.ram_rsrc:
                last = int(consultaSNMP(SNMP_COMMUNITY, HOST, cat.oid.ram_free))
                load = int(100*(fixed_ram - last - 1800000)/fixed_ram)
            case cat.nic_rsrc:
                load = int(consultaSNMP(SNMP_COMMUNITY, HOST, cat.oid.in_oct)) + int(
                    consultaSNMP(SNMP_COMMUNITY, HOST, cat.oid.ou_oct))

        valor = f'N:{load}' # "N:" + str(load)
        print (f'{RSRC_NAME}:{valor}')
        rrdtool.update(RRD_FILEPATH, valor)
        time.sleep(SLEEP_TIME)

if __name__=='__main__':
    if len(argv) != 7:
        exit(f"""
        asegurese de llamar el programa con los argumentos en este orden:
        RRD_FILEPATH:str
        SLEEP_TIME:int
        SNMP_COMMUNITY:str
        HOST:str
        OID:str #non used
        RSRC_NAME:str
        """)

    query(argv[1], int(argv[2]), argv[3], argv[4], argv[5], argv[6])

    # try:
    #     query(argv[1], int(argv[2]), argv[3], argv[4], argv[5], argv[6])
    # except:
    #     pass
    # query()

    # if ret:
    #     print (rrdtool.error())
    #     time.sleep(300)
