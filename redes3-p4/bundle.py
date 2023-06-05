# ASCII color codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def red(text):
    return f"{RED}{text}{RESET}"

def green(text):
    return f"{GREEN}{text}{RESET}"

def yellow(text):
    return f"{YELLOW}{text}{RESET}"

def blue(text):
    return f"{BLUE}{text}{RESET}"

def magenta(text):
    return f"{MAGENTA}{text}{RESET}"

def cyan(text):
    return f"{CYAN}{text}{RESET}"

def white(text):
    return f"{WHITE}{text}{RESET}"


class text:
    
    eol = b"\r\n"
    ascii = "ascii"
    prompt_ip = magenta("rcp ip >>> ")

    import_ = 'importar archivo'
    extract = 'extraer archivo'
    generate = 'generar archivo'
    title_import = blue(f'**{import_}**')
    title_extract = blue(f'**{extract}**')
    title_generate = blue(f'**{generate}**')

    import_succ = cyan('archivo importado con exito')
    extract_succ = cyan('archivo extraido con exito')
    generate_succ = cyan('archivo generado con exito')

    options = yellow("\n".join([
        "'generate': Generar el archivo de configuración",
        "'extract': Extraer el archivo de configuración",
        "'import': Importar el archivo de configuración",
        "'cip': Cambiar la ip de router con la que se esta trabajando",
        "'exit': Salir del programa"
    ]))

    prompt = magenta(">>> ")

    err_ipv4_regex = red('Introduzca una ipv4 valida')
    fine_ipv4 = white('ip actual es: ')
    none_ipv4 = white('sin ipv4 actual')

class telnet:
    user_prompt = b"User: "
    pass_prompt = b"Password: "

class rcp:
    enable = b"en" + text.eol
    config = b"config" + text.eol
    cpy_run_str = b"copy run start" + text.eol
    exit = b"exit" + text.eol

