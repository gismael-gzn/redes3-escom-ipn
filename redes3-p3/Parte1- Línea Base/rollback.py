from sys import argv
import os
import rrdtool
import time
import datetime
from  Notify import send_alert_attached
import time

rrdpath = '/home/dio/school/Introduccion_SNMP/6-AdministraciónDeRendimiento/RRD/'
imgpath = '/home/dio/school/Introduccion_SNMP/6-AdministraciónDeRendimiento/IMG/'

def generarGrafica(ultima_lectura):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv( imgpath+"deteccion.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",
                    "DEF:cargaCPU="+rrdpath+"trend.rrd:CPUload:AVERAGE",
                     "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                     "VDEF:cargaMIN=cargaCPU,MINIMUM",
                     "VDEF:cargaSTDEV=cargaCPU,STDEV",
                     "VDEF:cargaLAST=cargaCPU,LAST",
                     "CDEF:umbral50=cargaCPU,50,LT,0,cargaCPU,IF",
                     "AREA:cargaCPU#00FF00:Carga del CPU",
                     "AREA:umbral50#FF9F00:Carga CPU mayor de 50",
                     "HRULE:8#FF0000:Umbral  50%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    print (ret)


IMG_PATH = ''
DST_EMAIL = 'onfunct.123@gmail.com'

rsrc_name = ''
LOG_size = 15
LOG = ['']*LOG_size
LOG_pos = 0

def doLog(timestamp:float, dato:int):
    global rsrc_name
    global LOG_size
    global LOG
    global LOG_pos

    warn_msg = f'{datetime.datetime.fromtimestamp(timestamp)}: {dato}'
    LOG[LOG_pos] = warn_msg
    LOG_pos = (LOG_pos + 1) % LOG_size
    print(f'Se sobrepaso el uso de {rsrc_name}, {warn_msg}')

def detect(RSRC_NAME:str, RRD_FILEPATH:str, IMG_PATH:str, DST_MAIL:str):
    dato = 0
    while (1):
        ultima_actualizacion = rrdtool.lastupdate(rrdpath + "trend.rrd")
        timestamp=ultima_actualizacion['date'].timestamp()
        dato=ultima_actualizacion['ds']["CPUload"]
        print(dato)

        if dato >= 5:
            generarGrafica(int(timestamp))


        if dato > 60:
            doLog(timestamp, dato)

        if dato > 80:
            send_alert_attached(f'Sobre-uso de {rsrc_name}', DST_EMAIL, '\n'.join(LOG), IMG_PATH)

        if dato > 95:
            break
        
        time.sleep(40)

    if dato > 95:
        os.system('sudo shutdown')

if __name__ == '__main__':
    detect()
