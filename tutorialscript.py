#! /usr/bin/python
import ibmiotf.device
import RPi.GPIO as GPIO
import time
co = {
	"org": "<Your organisation>",
	"type": "<Your device type>",
	"id" : "<Your device ID>",
	"auth-method": "token",
	"auth-token": "<Your auth-token>",
	"clean-session": "true"
}
client = ibmiotf.device.Client(co)
client.connect() #connect to broker
TrigGPIO = #The GPIO pin that your TRIG pin is connected to
EchoGPIO = #The GPIO pin that your ECHO pin is connected to
RedGPIO = #The GPIO pin that your Red LED is connected to
GreenGPIO = #The GPIO pin that your Green LED pin is connected to
YellowGPIO = #The GPIO pin that your Yellow LED pin is connected to
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RedGPIO, GPIO.OUT)
GPIO.setup(GreenGPIO, GPIO.OUT)
GPIO.setup(YellowGPIO, GPIO.OUT)
GPIO.setup(TrigGPIO, GPIO.OUT)
GPIO.setup(EchoGPIO, GPIO.IN)
print("setup completed")
output = "empty"
counter = 0
def ledChoose(str):
	led = str
	if led == "red":
		GPIO.output(RedGPIO, True)
		GPIO.output(GreenGPIO, False)
		GPIO.output(YellowGPIO, False)
	elif led == "green":
		GPIO.output(RedGPIO, False)
		GPIO.output(GreenGPIO, True)
		GPIO.output(YellowGPIO, False)
	elif led == "yellow":
		GPIO.output(RedGPIO, False)
		GPIO.output(GreenGPIO, False)
		GPIO.output(YellowGPIO, True)
	elif led == "all":
		GPIO.output(RedGPIO, True)
		GPIO.output(GreenGPIO, True)
		GPIO.output(YellowGPIO, True)
	elif led == "off":
		GPIO.output(RedGPIO, False)
		GPIO.output(GreenGPIO, False)
		GPIO.output(YellowGPIO, False)
try:
	while True:
		GPIO.output(TrigGPIO, False)
		time.sleep(1)
		GPIO.output(TrigGPIO, True)
		time.sleep(0.001)
		GPIO.output(TrigGPIO, False)
		while GPIO.input(EchoGPIO)==0:
			pulse_start = time.time()
		while GPIO.input(EchoGPIO)==1:
			pulse_end = time.time()
		duration = pulse_end - pulse_start
		print("Duration for sensor 1 was: ", round(duration*1000),"milliseconds")
		distance = duration * 17150
		distance = round(distance,2)
		print ("Distance for sensor 1 was: ",distance,"cm")
		if(distance < 30):
			ledChoose("green")
			output = "empty"
		elif(distance > 30):
			ledChoose("red")
			output = "occupied"
		time.sleep(0.5)
		print("sensor 1 done")
		Data = {'serial': counter, 'name' : 'distance', 'data' : distance, 'state': output, 'id': <your-device-id>}
		client.publishEvent("status" , "json", Data )#Publish event to cloud
		counter += 1
finally:
	client.disconnect()
	ledChoose("off")
	GPIO.cleanup()
