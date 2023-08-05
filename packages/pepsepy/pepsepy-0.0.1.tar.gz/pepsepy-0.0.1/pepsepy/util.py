import csv
import time
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psutil
import pybps
import configparser
import requests
#--------------------------------------------------------------------------------------#

def get_owm_api_key(parameter_list):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    r = requests.get(url)
    return r.json()

def sendgmail(from_addr, to_addr_list, subject, message,
                login, password, att_file=None, smtpserver='smtp.gmail.com:587'):

    # Build message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr_list)
    msg.attach( MIMEText(message) )

    # Attach file
    if att_file is not None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(att_file, 'rb').read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(att_file))
        msg.attach(part)

    # Send email
    server = smtplib.SMTP(smtpserver.split(':')[0],smtpserver.split(':')[1])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login,password)
    try:
        server.sendmail(from_addr, to_addr_list, msg.as_string())
        print ('email sent')
    except:
        print ('error sending mail')
    server.quit()