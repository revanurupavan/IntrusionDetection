 #!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import os
import smtplib
import picamera                             #library for camera

jpg="jpg"

#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/IoT/shadow/update/accepted", qos=0)
        mqttc.publish("$aws/things/IoT/shadow/update",'{"state":{"reported":{"color":"Pavan"}}}')
        #The names of these topics start with $aws/things/thingName/shadow."
        

    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="cgao")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/home/pi/team/rootCA.pem.crt",
	      certfile="/home/pi/team/b66fe63d7f-certificate.pem.crt",
	      keyfile="/home/pi/team/b66fe63d7f-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("a2g7dmnujp6p9v.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

#automatically handles reconnecting
mqttc.loop_start()

#GPIO Input Output declarations
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(11, GPIO.IN)                         #PIR sensor
	

	
	


                                          

camera image settings
camera=picamera.PiCamera()                      #camera module
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

                
try:

        while True:
               PIR_Status=GPIO.input(11)                #PIR status
               if PIR_Status==1:                        #If motion detected
                     print "Motion Detected."
             
                     if (True): 
                                mqttc.publish("$aws/things/IoT/shadow/update",'{"state":{"reported":{"motion":"detected"}}}')
                                #Turn on LED 1
				GPIO.output(3,1)
				#Get current timestamp
                                time_stamp=time.ctime()                                                                        
                                time_stamp=(time_stamp, jpg)
                                s = "."
                                time_stamp=s.join(time_stamp)
                                time_stamp = time_stamp.replace(' ', '-')
                                #Capture the image with current timestamp
				camera.capture(time_stamp)                                                                    
				#os.system('fswebcam ' + time_stamp) "This can be used to caputre image with web camera
				print time_stamp
				server = smtplib.SMTP('smtp.gmail.com', 587)
	  			server.starttls()
	  			#Removed maildId and passWd from code due to privacy purposes.
				server.login(mailId, passWd)
				msg = "ALERT!! Intruder detected. Please check your Dropbox for the image."
				#Message is sent to user saying there is an intrusion
				#mailId is sender's email and vText is receiver's email
				server.sendmail(mailId, vText, msg)
				server.quit()
				print "SMS Alert sent!!"
				os.system('/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/' + time_stamp + ' /test')	
				time.sleep(1)
               
                         
except KeyboardInterrupt:
                print("Program exiting")
                GPIO.cleanup()



                        







