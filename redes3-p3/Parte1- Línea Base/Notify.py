import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import time
import sys

from filelock import FileLock

filename = 'last-sent-email_timestamp.txt'
wait_policy = 60

def have_to_wait():
    global filename
    lock_filename = "timestamp.lock"

    lock = FileLock(lock_filename, timeout=10)

    with lock:
        if os.path.exists(filename):
            # If the file exists, read the timestamp value into an integer
            with open(filename, 'r') as file:
                stored_timestamp = int(file.read())

            # Calculate the time difference between the current and stored timestamps
            current_timestamp = int(time.time())
            difference = current_timestamp - stored_timestamp

            return wait_policy-difference

def ami_allowed_to_send_email(isCritical:bool):
    # Get the current timestamp and format the filename
    global filename
    current_timestamp = int(time.time())
    lock_filename = "timestamp.lock"

    lock = FileLock(lock_filename, timeout=10)

    with lock:
        if not os.path.exists(filename):
            # If the file does not exist, create it and write the timestamp
            with open(filename, 'w') as file:
                file.write(str(current_timestamp))
            return True
        else:
            # If the file exists, read the timestamp value into an integer
            with open(filename, 'r') as file:
                stored_timestamp = int(file.read())

            # Check if the current timestamp is greater by wait_policy seconds
            if current_timestamp - stored_timestamp >= wait_policy or isCritical==True:
                # Update the file with the current timestamp
                with open(filename, 'w') as file:
                    file.write(str(current_timestamp))
                return True
            else:
                return False

COMMASPACE = ', '
# Define params

mailsender = "dummycuenta3@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'mxrfalaydmgolvaq'

def mail_send(SUBJECT:str, DST:str, BODY:str, IMGPATH:str):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = mailsender
    msg['To'] = DST

    txt = MIMEText(BODY)
    msg.attach(txt)

    fp = open(IMGPATH, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    s = smtplib.SMTP(mailserver)
    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, DST, msg.as_string())
    s.quit()

def send_alert_attached(SUBJECT:str, DST:str, BODY:str, IMGPATH:str, isCritical:bool):

    logged = False
    while ami_allowed_to_send_email(isCritical) == False:
        if logged == False:
            print('El mensaje se agregó a la fila, espere unos momentos...')
            logged = True
        print(f'Espere APROX {have_to_wait()} segundos (proceso {os.getpid()})')
        time.sleep(3)
    
    mail_send(SUBJECT, DST, BODY, IMGPATH)
    print('Email enviado!')

if __name__=='__main__':
    argv = sys.argv
    if len(argv) != 6:
        exit("""
        llame el programa con los siguientes argumentos en orden:
        SUBJECT:str
        DST:str
        BODY:str
        IMGPATH:str
        isCritical:bool
        """)
    send_alert_attached(argv[1], argv[2], argv[3], argv[4], bool(int(argv[5])))