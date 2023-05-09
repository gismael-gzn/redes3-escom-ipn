import rrdtool

def create(rrd_filepath:str, TRANS:str, FN:str):
    ret = rrdtool.create(rrd_filepath,
                        "--start",'N',
                        "--step",'60',
                        f"DS:CPUload:{TRANS}:60:U:U",
                        f"RRA:{FN}:0.5:1:24")
    # CPULoad to LOAD
    if ret:
        print (rrdtool.error())

# def create(wd:str, name:str):
#     ret = rrdtool.create("/home/dio/school/Introduccion_SNMP/6-AdministraciónDeRendimiento/RRD/trend.rrd",
#                         "--start",'N',
#                         "--step",'60',
#                         "DS:CPUload:GAUGE:60:0:100",
#                         "RRA:AVERAGE:0.5:1:24")
#     if ret:
#         print (rrdtool.error())
