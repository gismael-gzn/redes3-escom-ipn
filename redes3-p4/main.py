import telnetlib
from ftplib import FTP
import re

from bundle import *

ipv4 = re.compile("^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
user = "rcp"
pas = "rcp"
filenam = "startup-config"
cip = ''
    
def get_current_ip(force:bool):
    global cip

    if cip == '' or force:
        cip = input(text.prompt_ip)
    
    if ipv4.match(cip) == None:
        print(text.err_ipv4_regex)
        cip = ''

    return cip

def generate_file():
    print(text.title_generate)

    host = get_current_ip(False)
    if host == '':
        return

    tn = telnetlib.Telnet()
    tn.open(host)
    tn.read_until(telnet.user_prompt)
    tn.write(user.encode(text.ascii)+text.eol)
    tn.read_until(telnet.pass_prompt)
    tn.write(pas.encode(text.ascii)+text.eol)
    tn.write(rcp.enable)
    tn.write(rcp.config)
    tn.write(rcp.cpy_run_str)
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.read_all()
    tn.close()
    print(text.generate_succ)
    

def show_current_ip():
    global cip
    if cip == '':
        print(text.none_ipv4)
    else:
        print(f'{text.fine_ipv4}{yellow(cip)}')

def extract_file():
    print(text.title_extract)

    host = get_current_ip(False)
    if host == '':
        return

    name = filenam
    tn = telnetlib.Telnet()
    tn.open(host)
    tn.read_until(telnet.user_prompt)
    tn.write(user.encode(text.ascii)+text.eol)
    tn.read_until(telnet.pass_prompt)
    tn.write(pas.encode(text.ascii)+text.eol)
    tn.write(rcp.enable)
    tn.write(rcp.config)
    tn.write(b"service ftp\r\n")
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.read_all()
    tn.close()
    
    ftp = FTP (host)
    ftp.login(user,pas)
    ftp.retrbinary('RETR startup-config',open(name , 'wb').write)
    ftp.quit()
    print(text.extract_succ)



def import_file():
    print(text.title_import)

    host = get_current_ip(False)
    if host == '':
        return

    name = filenam
    tn = telnetlib.Telnet()
    tn.open(host)
    tn.read_until(telnet.user_prompt)
    tn.write(user.encode(text.ascii)+text.eol)
    tn.read_until(telnet.pass_prompt)
    tn.write(pas.encode(text.ascii)+text.eol)
    tn.write(rcp.enable)
    tn.write(rcp.config)
    tn.write(b"service ftp\r\n")
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.write(rcp.exit)
    tn.read_all()
    tn.close()
    
    ftp = FTP (host)
    ftp.login(user,pas)
    f = open(name,'rb')
    ftp.storbinary('STOR startup-config',f)
    f.close()
    ftp.quit()
    print(text.import_succ)

import readline
import os

OPTIONS = ['generate', 'extract', 'import', 'cip', 'exit']
HISTORY_FILE = os.path.join(os.getcwd(), ".history")

def initialize_readline():
    readline.parse_and_bind('tab: complete')
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)

    readline.set_completer(completer)

def completer(text, state):
    options = [i for i in OPTIONS if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def save_history():
    readline.write_history_file(HISTORY_FILE)

def menu():
    initialize_readline()
    print(text.options)

    opc = ''
    while opc != 'exit':
        show_current_ip()
        opc = input(text.prompt)

        if opc == OPTIONS[0]:
            generate_file()
        elif opc == OPTIONS[1]:
            extract_file()
        elif opc == OPTIONS[2]:
            import_file()
        elif opc == OPTIONS[3]:
            get_current_ip(True)

        save_history()

    print("Saliendo...")

if __name__=='__main__':
    menu()
    
