from bundle import bundle as cat
import trendCreate as tc

import subprocess as sp
import time

import atexit


def killAll(killable:list):
    print('killed')
    for k in killable:
        try:
            k.kill()
        except:
            exit('Error fatal, ignore esto...')

def begin():
    sleep_time = '10'
    com = 'GerardoIsmaelGarzonDominguez'
    localhost = 'localhost'
    dst_email = 'tanibet.escom@gmail.com'

    try:
        tc.create(cat.rrd_cpu_filepath, 'GAUGE', 'AVERAGE')
        tc.create(cat.rrd_ram_filepath, 'GAUGE', 'AVERAGE')
        tc.create(cat.rrd_nic_filepath, 'DERIVE', 'AVERAGE')
        cpu = sp.Popen([cat.py_intrpr, cat.update, cat.rrd_cpu_filepath, sleep_time, com, localhost, cat.oid.cpu, cat.cpu_rsrc])
        ram = sp.Popen([cat.py_intrpr, cat.update, cat.rrd_ram_filepath, sleep_time, com, localhost, cat.oid.cpu, cat.ram_rsrc])
        nic = sp.Popen([cat.py_intrpr, cat.update, cat.rrd_nic_filepath, sleep_time, com, localhost, cat.oid.cpu, cat.nic_rsrc])

        time.sleep(1)

        cpu_g = sp.Popen([cat.py_intrpr, cat.detect, cat.cpu_rsrc, cat.rrd_cpu_filepath, cat.img_cpu_filepath, dst_email, sleep_time])
        ram_g = sp.Popen([cat.py_intrpr, cat.detect, cat.ram_rsrc, cat.rrd_ram_filepath, cat.img_ram_filepath, dst_email, sleep_time])
        nic_g = sp.Popen([cat.py_intrpr, cat.detect, cat.nic_rsrc, cat.rrd_nic_filepath, cat.img_nic_filepath, dst_email, sleep_time])

        spcs = [cpu, ram, nic, cpu_g, ram_g, nic_g]
        atexit.register(killAll, spcs)
        
    except:
        print('excepted')
        killAll(spcs)

    finally:
        print('esperando cancelación en proceso principal con CTRL+C')
        for s in spcs:
            s.wait()

    # while True:
    #     try:
    #         pass
    #     except KeyboardInterrupt:
    #         killAll()

if __name__ == '__main__':
    begin()

