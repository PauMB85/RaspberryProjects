#-*- coding: utf-8 -*-                                                          

'''                                                                             
Author: PauMB                                                                   
Program: Motion sensor, if it detec moves in the room, the firts time send      
         an email, the 20th send sms with Carriots plataform                    
Date: 08/09/14                                                                  
Company: HedaSoft                                                               
'''

#importing libreries                                                            
import RPi.GPIO as GPIO
import time
import sys
import smtplib
from email.mime.text import MIMEText
import signal

#values                                                                         
lastStatus = 1   #inicilize in 0, (0 no move, 1 move)                           
n_Moves = -1     #number the moves detected     

#data mail                                                                                              
From = 'paumb85@gmail.com'
To = 'paumb85@gmail.com'
Subject = 'Prueba Mail'
Text = 'Contenido del mail a enviar'

#names of gpio                                                                  
motion = 17		 #GPIO 17                                                                                
ledGreen = 23            #GPIO 23                                                                                
ledRed = 24              #GPIO 24

def signal_handler(signal,frame):
    '''Close the program with ^C'''

    print ""
    GPIO.cleanup()
    print "Close the program"
    sys.exit(0)

def setup():
    '''Setup'''

    #initialize GPIO                                                          
    GPIO.setmode(GPIO.BCM)         #set up GPIO using BCM numbering             
    GPIO.setup(motion, GPIO.IN)    #control motion sensor with GPIO 17          
    GPIO.setup(ledGreen, GPIO.OUT) #control ledGreen                            
    GPIO.setup(ledRed, GPIO.OUT)   #control ledRed                              

    #initialize Leds                                                           
    GPIO.output(ledGreen,True)     #turn ledGreen on                          
    GPIO.output(ledRed,True)       #turn ledRed off                              

    signal.signal(signal.SIGINT, signal_handler)

    #Motion Sensor begin in...                                                  
    print("The Motion Sensor begins in:")
    for i in range (5,0,-1):
      print(i)
      time.sleep(1)

def tiempo(tiempoCapturado):
    '''From a capture time, in miliseconds,                                                                      
       get the hour and minutes'''
       
    hour = tiempoCapturado[3]
    minute = tiempoCapturado[4]
    return hour,minute

def envioMail(sendFrom,sendTo,sendSubject,sendText,hora,minuto):
    '''Send a mail'''

    #Body missage                                                                           
    msg = MIMEText(sendText)

    #Connection with the server
    msg['Subject'] = sendSubject
    msg['From'] = sendFrom
    msg['To'] = sendTo

    #Credentials                                                                                 
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login("YourMail@gmail.com","password")
    #send mail ('from', 'to')                                                                         
    mailServer.sendmail(sendFrom, sendTo, msg.as_string())
    #close                                                                            
    mailServer.close()
    
def sendStream():
    ''' Send a stream from carriots plataform and send you a sms'''

    data = {"protocol": "v2", "device": device, "at": timestamp, "data": dict(
            motionSend=("ON" if lastStatus is 0 on else "OFF"))}
    carriots_response = client_carriots.send(data)
    print carriots_response.read()
    
    
def main():
    '''Main'''

    #initialize the program                                                                      
    setup()

    global n_Moves, lastStatus
    while True:
        #Are there moving???                                           
                                                                                         
        if GPIO.input(motion) == GPIO.HIGH and lastStatus == 0:
            print "the are moving"
            lastStatus = 1
            n_Moves += 1
            GPIO.output(ledRed,True)
            GPIO.output(ledGreen,False)
            if n_Moves%5 == 0 :
            	#if detected 5 movings, send an email
                t_CapturaSeg = time.time()
                t_Captura = time.localtime(t_CapturaSeg)
                hour, minute = tiempo(t_Captura)
		envioMail(From,To,Subject,Text,hour,minute)
                print "Send Mail"
            elif n_Moves%17 == 0 :
                #if detected 17 movings, send a sms
                sendStream()
                n_Moves = 0
                print "Send a SMS"
        elif GPIO.input(motion) == GPIO.LOW and lastStatus == 1:
            print "There aren't moving"
            lastStatus = 0
            GPIO.output(ledRed,False)
            GPIO.output(ledGreen,True)

if __name__ == '__main__':
    main()
