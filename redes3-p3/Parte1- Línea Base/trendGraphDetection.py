from bundle import bundle as cat

from sys import argv
import os
import rrdtool
import time
import datetime
from  Notify import send_alert_attached
import time

def generarGrafica(ultima_lectura:int, RSRC_NAME:str, IMG_FILEPATH:str, RRD_FILEPATH:str):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    mul = 1 if RSRC_NAME != cat.nic_rsrc else cat.SLA.Mbs_max/100
    umax = 100 if RSRC_NAME != cat.nic_rsrc else cat.SLA.Mbs_max
    ret = rrdtool.graphv(IMG_FILEPATH,
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     f'--vertical-label=Carga de {RSRC_NAME}',
                    '--lower-limit', '0',
                    '--upper-limit', f'{umax}',
                    f'--title=Carga de su {RSRC_NAME}',
                    f'DEF:cargaRSRC={RRD_FILEPATH}:CPUload:AVERAGE',
                     "VDEF:cargaMAX=cargaRSRC,MAXIMUM",
                     "VDEF:cargaMIN=cargaRSRC,MINIMUM",
                     "VDEF:cargaSTDEV=cargaRSRC,STDEV",
                     "VDEF:cargaLAST=cargaRSRC,LAST",
                    f"CDEF:umbralNOT=cargaRSRC,{cat.SLA.Soft*mul},LT,0,cargaRSRC,IF",
                    f"AREA:cargaRSRC#00FF00:Carga de {RSRC_NAME}",
                    f"AREA:umbralNOT#FF642B:Carga de {RSRC_NAME} mayor de {cat.SLA.Moderate*mul}",
                    f"HRULE:{cat.SLA.Soft*mul}#00FF00:Umbral de advertencia {cat.SLA.Soft*mul}%",
                    f"HRULE:{cat.SLA.Moderate*mul}#FFFF00:Umbral de notificación {cat.SLA.Moderate*mul}%",
                    f"HRULE:{cat.SLA.Critical*mul}#FF0000:Umbral de acción {cat.SLA.Critical*mul}%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    # print (ret)


LOG_size = 15
LOG = ['']*LOG_size
LOG_pos = 0

def doLog(timestamp:float, dato:int, RSRC_NAME:str):
    global LOG_size
    global LOG
    global LOG_pos

    warn_msg = f'{datetime.datetime.fromtimestamp(timestamp)}: {RSRC_NAME}:{dato}%'
    LOG[LOG_pos] = warn_msg
    LOG_pos = (LOG_pos + 1) % LOG_size
    print(f'Se sobrepaso el uso de {RSRC_NAME} establecido en el umbral de advertencia, {warn_msg}')
    print(LOG)

firstSleep = 8
def detect(RSRC_NAME:str, RRD_FILEPATH:str, IMG_FILEPATH:str, DST_MAIL:str, SLEEP_TIME:int):
    dato = 0
    while (1):


        ultima_actualizacion = rrdtool.lastupdate(RRD_FILEPATH)
        timestamp=ultima_actualizacion['date'].timestamp()
        dato=ultima_actualizacion['ds']["CPUload"]
        # print(f'>>>{dato}')

        print(f'Gráfica de {RSRC_NAME} generada...')
        generarGrafica(int(timestamp), RSRC_NAME, IMG_FILEPATH, RRD_FILEPATH)

        global firstSleep
        if RSRC_NAME == cat.nic_rsrc:
            if firstSleep:
                time.sleep(firstSleep*SLEEP_TIME)
                firstSleep = False

            (start_time, end_time, step), _, data = rrdtool.fetch(RRD_FILEPATH, 'AVERAGE')
            # Find the index of the desired data source
            ds_index = _.index('CPUload')
            # print(data)
            # Extract the values for the specified data source and remove None values
            values = [row[ds_index] for row in data if row[ds_index] is not None]

            # Calculate the average of the values
            try:
                dato = sum(values) / len(values)
                dato = 100.0*(dato/cat.SLA.Mbs_max)
                print(f'>>>>>>>>>{dato}')
            except:
                time.sleep(SLEEP_TIME)
                continue
            # dato = int(dato/cat.SLA.Mbs_max)

        # print(f'{RSRC_NAME}{dato}')

        if dato >= cat.SLA.Soft and dato < cat.SLA.Moderate:
            msg = f"""
            {cat.SLA.body} {cat.SLA.Soft_str} de {RSRC_NAME}
            {datetime.datetime.fromtimestamp(timestamp)}: {RSRC_NAME}:{dato}%
            """
            print(msg)
            send_alert_attached(f'{cat.SLA.subject} {RSRC_NAME} ({cat.SLA.Soft_str}) ', DST_MAIL, msg, IMG_FILEPATH, False)

        elif dato >= cat.SLA.Moderate and dato < cat.SLA.Critical:
            msg = f"""
            {cat.SLA.body} {cat.SLA.Moderate_str} de {RSRC_NAME}
            {datetime.datetime.fromtimestamp(timestamp)}: {RSRC_NAME}:{dato}%
            """
            print(msg)
            send_alert_attached(f'{cat.SLA.subject} {RSRC_NAME} ({cat.SLA.Moderate_str}) ', DST_MAIL, msg, IMG_FILEPATH, False)

        elif dato >= cat.SLA.Critical :
            msg = f"""
            {cat.SLA.body} {cat.SLA.Critical_str} de {RSRC_NAME}
            {datetime.datetime.fromtimestamp(timestamp)}: {RSRC_NAME}:{dato}%
            """
            print(msg)
            send_alert_attached(f'{cat.SLA.subject} {RSRC_NAME} ({cat.SLA.Critical_str}) ', DST_MAIL, msg, IMG_FILEPATH, True)
            break
        
        time.sleep(SLEEP_TIME)

    if dato > cat.SLA.Critical:
        os.system('shutdown')


if __name__ == '__main__':
    if len(argv) != 6:
        exit(f"""
        asegurese de llamar el programa con los argumentos en este orden:
        RSRC_NAME:str
        RRD_FILEPATH:str
        IMG_FILEPATH:str
        DST_MAIL:str
        SLEEP_TIME:int
        """)
    
    detect(argv[1], argv[2], argv[3], argv[4], int(argv[5]))
            