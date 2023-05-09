import readline
import atexit
import re
import time
import datetime 
import threading as Thr

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

import bundle
import rrdtool as rrd
from state import state as Snap

snap = Snap()

def setup_readln():
    # Set up the history file
    histfile = '.myhistory'
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)

    # Define a function to be used as a completer
    def complete(text, state):
        options = bundle.keyword.cmds
        matches = [opt for opt in options if opt.startswith(text)]
        if state < len(matches):
            return matches[state]
        else:
            return None

    # Set the completer function
    readline.set_completer(complete)
    readline.parse_and_bind('tab: complete')

def Tkn(line:str) -> list[str]:
    args = re.split(r' \s* | \n*', line)
    args = list(filter(lambda ln: ln != '', args))
    return args

def Tkn0(line:str) -> list[str]:
    return Tkn(line)[0]

def Add(args:list[str]):
    # print(args)
    if args.__len__() == 1:
        alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
        alias = Tkn0(alias)
        if snap.alias_exists(alias):
            print(bundle.Msg.exists_err)
            return
        if bundle.checks.alias.fullmatch(alias) != None:
            args.append(alias)
        else:
            print(bundle.Msg.alias_err)
        Add(args)
        return
    
    if args.__len__() == 2:
        ip:str = input(f'{bundle.keys.ip}{bundle.Msg.cont_prompt}')
        ip = Tkn0(ip)
        if bundle.checks.ipv4.fullmatch(ip) != None:
            args.append(ip)
        else:
            print(bundle.Msg.ipv4_err)
        Add(args)
        return

    if args.__len__() == 3:
        snmp_v:str = input(f'{bundle.keys.ver}{bundle.Msg.cont_prompt}')
        snmp_v = Tkn0(snmp_v)
        if bundle.checks.snmp_v.fullmatch(snmp_v) != None:
            args.append(snmp_v)
        else:
            print(bundle.Msg.snmp_v_err)
        Add(args)
        return

    if args.__len__() == 4:
        com:str = input(f'{bundle.keys.com}{bundle.Msg.cont_prompt}')
        com = Tkn0(com)
        if bundle.checks.com_nm.fullmatch(com) != None:
            args.append(com)
        else:
            print(bundle.Msg.com_err)
        Add(args)
        return

    if args.__len__() == 5:
        port:str = input(f'{bundle.keys.port}{bundle.Msg.cont_prompt}')
        port = Tkn0(port)
        if bundle.checks.ports.fullmatch(port) != None:
            args.append(port)
        else:
            print(bundle.Msg.ports_err)
        Add(args)
        return

    #redundant check
    if args.__len__() == 6:
        checks = [
            (bundle.checks.alias, bundle.Msg.alias_err),
            (bundle.checks.ipv4, bundle.Msg.ipv4_err),
            (bundle.checks.snmp_v, bundle.Msg.snmp_v_err),
            (bundle.checks.com_nm, bundle.Msg.com_err),
            (bundle.checks.ports, bundle.Msg.ports_err),
        ]
        valid:bool = True
        trimed = args[1:]

        for i, s in enumerate(trimed):
            if checks[i][0].fullmatch(s) != None:
                continue
            else:
                print(checks[i][1])
                valid = False

        if valid:
            try:
                rv = snap.add_agent(*tuple(trimed))
                if rv != '':
                    print(rv)
            except:
                print(bundle.Msg.qry_err)
        else:
            print(bundle.Msg.correct_err)

    else:
        print(bundle.Msg.Add.err)

def Mod(args:list[str]):
    if args.__len__() == 1:
        alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
        alias = Tkn0(alias)
        if bundle.checks.alias.fullmatch(alias) != None:
            if snap.rem_agent(alias) == '':
                args = [bundle.keyword.add]
                Add(args)
        else:
            print(bundle.Msg.alias_err)
        return

def Rem(args):
    if args.__len__() == 1:
        alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
        alias = Tkn0(alias)
        if bundle.checks.alias.fullmatch(alias) != None:
            snap.rem_agent(alias)
        else:
            print(bundle.Msg.alias_err)

def Qry(args):
    if args.__len__() == 1:
        alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
        alias = Tkn0(alias)
        if bundle.checks.alias.fullmatch(alias) != None:
            try:
                snap.update_qry(alias)
            except:
                print(bundle.Msg.qry_err)
        else:
            print(bundle.Msg.alias_err)

def List():
    print(snap.list_agents())

def Pdf(args):
    if args.__len__() == 1:
        alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
        alias = Tkn0(alias)
        if bundle.checks.alias.fullmatch(alias) != None:
            if not snap.alias_exists(alias):
                print(bundle.Msg.not_exists_err)
                return
            
            lines = snap.str_agent(alias).splitlines()

            pdf = canvas.Canvas(alias, pagesize=letter)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(inch, 10*inch, alias)

            pdf.setFont("Helvetica-Bold", 8)
            y = 9*inch
            for line in lines:
                pdf.drawString(inch, y, line)
                y -= 0.3*inch

            y -= 3*inch
            for os, r in zip(bundle.checks.oss, bundle.checks.oss_rgx):
                if r.search(lines[2]) != None:
                    pdf.drawImage(f'./{bundle.dir.src}/{os}', inch, y, width=200, height=200)
                    break

            pdf.save()

            # print(snap.str_agent(alias).splitlines())
        else:
            print(bundle.Msg.alias_err)

def Jump(args:list[str]):
    if args.__len__() >= 1:
        if args[0] == bundle.keyword.add:
            return Add(args)
        elif args[0] == bundle.keyword.mod:
            return Mod(args)
        elif args[0] == bundle.keyword.rem:
            return Rem(args)
        elif args[0] == bundle.keyword.qry:
            return Qry(args)
        elif args[0] == bundle.keyword.pdf:
            return Pdf(args)
        elif args[0] == bundle.keyword.lst:
            return List()
        elif args[0] == bundle.keyword.poll:
            return p2_qry()
        elif args[0] == bundle.keyword.graph:
            return graphica(None)
        else:
            print(bundle.Msg.unknown_cmd_err)

def p2_init():
    ret = rrd.create("monitorNET.rrd",
                        "--start",'N',
                        "--step",'15',
                        f"DS:{bundle.p2.varnames.multicast_packs}:COUNTER:120:U:U",
                        f"DS:{bundle.p2.varnames.ip_rcv}:COUNTER:120:U:U",
                        f"DS:{bundle.p2.varnames.icmp_omsg}:COUNTER:120:U:U",
                        f"DS:{bundle.p2.varnames.sent_seg_noretransmit}:COUNTER:120:U:U",
                        f"DS:{bundle.p2.varnames.udp_in_errs}:COUNTER:120:U:U",
                        "RRA:AVERAGE:0.5:1:120")
    if ret:
        print (rrd.error())

def p2_imgs(t_inicial:int, t_final:int):
    ds_names = bundle.p2.varnames.arr
    for ds_name in ds_names:
        rrd.graphv(f"{ds_name}.png",
                    "--start", f"{t_inicial}",
                    "--end", f"{t_final}",
                    "--title", f"{ds_name} graph",
                    "--vertical-label", "Units / Sec",
                    "DEF:data=monitorNET.rrd:" + ds_name + ":AVERAGE",
                    "LINE1:data#FFAF00:" + ds_name)

polling = False
alias_polled = None

def p2_poll(alias:str, secs:int):
    global alias_polled
    alias_polled = alias

    t_inicial = datetime.datetime.now()
    t_inicial = int(t_inicial.timestamp())
    global polling
    if polling == True:
        print('Ya se esta consultando un trafico de red')
        return
    
    print('trabajando en ello...')

    while secs:
        time.sleep(1)

        polled:dict = snap.p2_qry(alias)
        data = f'N'
        for vals in polled.values():
            data = f'{data}:{vals}'

        print(data)
        
        t_final = datetime.datetime.now()
        t_final = int(t_final.timestamp())

        if secs%15 == 0:
            rrd.update("monitorNET.rrd", data)
            rrd.dump('monitorNET.rrd','monitorNET.rrd.xml')
            p2_imgs(t_inicial, t_final)
        
        # print(data)
        secs -= 1





    graphica(alias)
    polling = False
    
    print('Hecho!, gráfica generada')
    print(bundle.Msg.prompt, end='')


def graphica(alias:str):
    if alias == None:
        global alias_polled
        alias = alias_polled
    # if alias == None:
    #     alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
    #     alias = Tkn0(alias)
    #     if bundle.checks.alias.fullmatch(alias) == None:
    #         print(bundle.Msg.alias_err)

    ds_names = bundle.p2.varnames.arr
    # Set up the PDF canvas

    file_name = f"report - {alias} - {int(time.time()) % 256}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    # Add the title
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_text = f'Monitoreo de "{alias}" : {snap.agents[alias][bundle.keys.com]} con {snap.agents[alias][bundle.keys.ip]}'
    title_paragraph = Paragraph(title_text, title_style)
    title_width, title_height = title_paragraph.wrap(letter[0], letter[1])
    title_top = letter[1] - title_height - 50
    title_left = (letter[0] - title_width) / 2
    title_paragraph.drawOn(c, title_left, title_top)
    
    image_top = title_top - title_height - 30
    image_left = 50
    image_width = 250
    image_height = 180

    for idx, ds_name in enumerate(ds_names):
        image_file = f"{ds_name}.png"
        img = Image(image_file, image_width, image_height)
        
        if idx % 2 == 0:
            image_top -= image_height + 20
            image_left = 50
        else:
            image_left += image_width + 50
        
        img.drawOn(c, image_left, image_top)

    # Save the PDF
    c.save()


def p2_qry():
    p2_init()
    alias:str = input(f'{bundle.keys.alias}{bundle.Msg.cont_prompt}')
    alias = Tkn0(alias)
    if bundle.checks.alias.fullmatch(alias) != None:
        global polling
        job = Thr.Thread(target=p2_poll, args=(alias, 600))
        job.start()
        polling = True
    else:
        print(bundle.Msg.alias_err)

def main():
    # x = consultaSNMP('asr-gismael', '192.168.100.110', '1.3.6.1.2.1.1.1.0', '161')
    # print(x)
    # exit()

    print(bundle.Msg.sayit)
    setup_readln()

    while True:
        try:
            command = input(bundle.Msg.prompt)
            if command == bundle.keyword.qt:
                raise EOFError
            args = Tkn(command)
            Jump(args)
        except EOFError:
            break

    print(bundle.Msg.ext)


if __name__ == '__main__':
    main()

