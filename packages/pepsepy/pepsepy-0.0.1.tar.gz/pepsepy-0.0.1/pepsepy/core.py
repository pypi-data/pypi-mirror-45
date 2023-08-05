import csv
import time
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psutil
import subprocess
from datetime import datetime
###################################### FUNCTIONS ######################################
def time_str():
        return str(datetime.now().date()).replace("-","")+"_"+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second)

def datetime_slash():
        return str(datetime.now().year)+'/'+str(datetime.now().month)+'/'+str(datetime.now().day)+' '+str(datetime.now().time())

# source :https://medium.com/@bakiiii/automatic-e-mail-sending-with-python-eb41855119e1
def sendEmail(server_str,server_port, userid, pdw, subject, message,receivers):
        """source :https://medium.com/@bakiiii/automatic-e-mail-sending-with-python-eb41855119e1"""
        server = smtplib.SMTP(server_str, server_port)
        server.starttls()
        server.login(userid, pdw)
        sender = 'pepse@gmail.com'
        server.sendmail(sender, receivers, message)

def isresponding(name):
        """check if the program is running, not responding"""
        os.system('tasklist /FI "IMAGENAME eq %s" /FI "STATUS eq NOT RESPONDING" > tmp.txt' % name)
        tmp = open('tmp.txt', 'r')
        a = tmp.readlines()
        tmp.close()
        if a[-1].split()[0] == name:
                return True
        else:
                return False

def isrespondingPID(PID):
    os.system('tasklist /FI "PID eq %d" /FI "STATUS eq running" > tmp.txt' % PID)
    tmp = open('tmp.txt', 'r')
    a = tmp.readlines()
    tmp.close()
    if int(a[-1].split()[1]) == PID:
        return True
    else:
        return False

def kill_by_process_name(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            print("Killing process: " + name)
            if(check_process_exist_by_name(name)):
                print("Killing process: " + name + " sucess")
            else:
                print("Killing process: " + name + " failed")
            return
 
    print("Not found process: " + name)
 
def check_process_exist_by_name(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            return True
 
    return False

def check_process_exist_by_pid(pid):
    for proc in psutil.process_iter():
        if proc.pid == pid:
            return True
 
    return False

def simulState(path):
        with open(path,'r') as f:
                if "end of the simulation" in f.read().lower():
                        state = 'FIN'
                else:
                        state = 'UNKNOWN'
        return state

def read_last_line_csv(filename,sep = '\t',Dict = True):
    """Read last line"""
    with open(filename, newline = '') as csv_file:
        if Dict == True:
            csv_reader = list(csv.DictReader(csv_file, delimiter=sep)) # convertir into list object
        else:
            csv_reader = list(csv.reader(csv_file, delimiter=sep))     # convertir into list object
        return csv_reader[-1]

def write2csv(filename,mode ='w',sep = '\t',**kwargs):
        """
	filename	: filename including its location
	mode		: mode 	
	sep			: delimiter
	fields		: fields
	"""
        fields = kwargs
        fieldnames = []
        for fieldname in fields:
                fieldnames.append(fieldname)
        
        file_exists = os.path.isfile(filename)
        with open(filename,mode,newline='') as f:
                writer = csv.DictWriter(f,delimiter=sep, fieldnames=fieldnames)
                if not file_exists:
                        writer.writeheader()
                if 'a' not in mode:
                        writer.writeheader()
                writer.writerow(fields)

