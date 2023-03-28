import re

class keyword(object):
    add = 'add'
    mod = 'mod'
    rem = 'rem'
    qry = 'qry'
    pdf = 'pdf'
    lst = 'lst'
    qt = 'q'
    cmds = [
        add, mod, rem, qry, pdf, lst, qt,
    ]

class Msg(object):
    add = 'añade agente'
    rem = 'remover agente'
    mod = 'modificar agente'
    qry = 'informe del agente en la terminal de comandos'
    pdf = 'genera reporte del agente en formato pdf'
    lst = 'imprime lista de agentes guardados'
    qt = 'quitar programa'
    sayit = f"""
    Introduzca un comando para lanzar el asistente:
    {keyword.add}: {add}
    {keyword.mod}: {mod}
    {keyword.rem}: {rem}
    {keyword.qry}: {qry}
    {keyword.pdf}: {pdf}
    {keyword.lst}: {lst}
    {keyword.qt}: {qt}
    """
    ext = 'Saliendo...'
    prompt = '>>> '
    cont_prompt = '... '

    class Add(object):
        err = f'uso: {keyword.add} | {keyword.add} <alias> <ip> <snmp version> <comunidad> <puerto>'

    alias_err = 'inserte un nombre de alias válido; [a-zA-Z0-9_-]{1,255}'
    ipv4_err = 'inserte una ipv4 válida...'
    snmp_v_err = 'inserte una versión snmp válida; versiones posibles 1,2,3'
    com_err = 'inserte un nombre de comunidad válido; [a-zA-Z0-9_-]{1,255}'
    ports_err = 'inserte un puerto válido; (0-65535)'
    correct_err = 'corrija las entradas e intente de nuevo...'

    exists_err = 'ya existe un agente con el mismo alias, utilice otro'
    vals_err = 'ya existe un agente con mismos: ip, version snmp, comunidad y puerto, cambie al menos un valor'

    not_exists_err = 'no existe un agente con ese nombre'

    unknown_cmd_err = 'comando inexistente'

class checks(object):
    alias = re.compile(r'^[a-zA-Z0-9_]{1,255}$')
    ipv4 = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')
    snmp_v = re.compile(r'1|2|3')
    com_nm = re.compile(r'^[a-zA-Z0-9_-]{1,255}$')
    ports = re.compile(r'([1-9]\d{0,3}|0|[1-9]\d{0,4}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])')

    oss = [
        'Fedora.png', 'Ubuntu.jpg', 'Windows.png'
    ]

    oss_rgx = [
        re.compile(r'Fedora'), re.compile(r'Ubuntu'), re.compile(r'Windows')
    ]
        

class monitor(object):
    ifno_attr = 'numero de interfaces'
    ifs = 'interfaces'
    attr = {
        'sistema': '1.3.6.1.2.1.1.1.0', 
        'dispositivo': '1.3.6.1.2.1.1.5.0', 
        'contacto': '1.3.6.1.2.1.1.4.0', 
        'ubicacion': '1.3.6.1.2.1.1.6.0', 
        ifno_attr: '1.3.6.1.2.1.2.1.0',
    }

    ifnm = '1.3.6.1.2.1.2.2.1.2.'
    ifst = '1.3.6.1.2.1.2.2.1.7.'
    

class dir(object):
    src = './src'
    wd = './data'
    cache = 'cache.json'
    data = 'data.json'
    

class keys(object):
    alias = 'alias'
    ip = 'ip'
    ver = 'snmp version -v'
    com = 'community -c'
    port = 'port'

