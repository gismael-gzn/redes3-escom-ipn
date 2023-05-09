import os
import sys

app_wd = os.path.dirname(os.getcwd())

python_binary_path = sys.executable
python_binary_name = os.path.basename(python_binary_path)

# print("Python binary path:", python_binary_path)
# print("Python binary name:", python_binary_name)

class bundle:
    py_intrpr = python_binary_name
    update = 'TrendUpdate.py'
    detect = 'trendGraphDetection.py'
    
    cpu_rsrc = 'CPU'
    rrd_cpu_filepath = f'{app_wd}/RRD/CPU.rrd'
    img_cpu_filepath = f'{app_wd}/IMG/CPU.png'

    ram_rsrc = 'RAM'
    rrd_ram_filepath = f'{app_wd}/RRD/RAM.rrd'
    img_ram_filepath = f'{app_wd}/IMG/RAM.png'
    
    nic_rsrc = 'NIC'
    rrd_nic_filepath = f'{app_wd}/RRD/NIC.rrd'
    img_nic_filepath = f'{app_wd}/IMG/NIC.png'

    class SLA:
        Mbs_max = 4 * 1000000
        Soft = 80
        Moderate = 85
        Critical = 98
        subject = 'Advertencia - Sobreutilización de'
        body = 'Se supero el umbral de uso'
        Soft_str = f'Suave ({Soft}%)'
        Moderate_str = f'Moderado ({Moderate}%)'
        Critical_str = f'Crítico ({Critical}%)'

    class oid:
        cpu = '1.3.6.1.2.1.25.3.3.1.2.196608'
        ram_fixed = '1.3.6.1.4.1.2021.4.5.0'
        ram_free = '1.3.6.1.4.1.2021.4.6.0'
        in_oct = '1.3.6.1.2.1.2.2.1.10.2'
        ou_oct = '1.3.6.1.2.1.2.2.1.16.2'

