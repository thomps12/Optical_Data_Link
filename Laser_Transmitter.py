## Photonic Device Research Group
## University of Illinois at Urbana-Champaign
## IEEE Photonics Society
## Spring 2015


# import modules
import RPi.GPIO as GPIO
import time


# declare variables
led = 37		# GPIO pin to drive laser
bit_time = 0.04; 	# bitrate in seconds
			# actual bitrate is twice as long because of encoding scheme
#phrase = "Hello World!"	# Word or phrase to send over laser
phrase = raw_input("Enter phrase for transmission: ")
#loop = 3		# Number of times to loop the signal
loop = input("Enter the number of times to loop the transmission: ")


# prepare GPIO
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led, GPIO.OUT)


# setup bit mask, used to send 8 bit ASCII characters
mask = [0]*8
mask[0] = int('10000000',2)
for i in range (7):
	mask[i+1] = mask[i]>>1	


# function to send individual letters to laser
def send_letter(letter):
	for x in range (8):
		if letter&mask[x]:
			GPIO.output(led, 0)	# For Edge detection
			time.sleep(bit_time/2)	#
			GPIO.output(led, 1)	#
			time.sleep(bit_time/2)	#
			GPIO.output(led, 1)	
			time.sleep(bit_time)
			GPIO.output(led, 0)
		else:
			GPIO.output(led, 0)	# For Edge detection
			time.sleep(bit_time/2)	#
			GPIO.output(led, 1)	#
			time.sleep(bit_time/2)	#
			GPIO.output(led, 0)
			time.sleep(bit_time)


# function to send header signal
def header():	
	GPIO.output(led, 1)
	time.sleep(bit_time*10)
	for x in range(11):
		GPIO.output(led, 0)		# 11 Edges for Header
		time.sleep(bit_time/2)		#
		GPIO.output(led, 1)		#
		time.sleep(bit_time/2)		#
	GPIO.output(led, 0)
	time.sleep(bit_time*10)
	GPIO.output(led, 0)
	time.sleep(bit_time/2)
	GPIO.output(led, 1)
	time.sleep(bit_time/2)


# function to send footer signal
def footer():
	GPIO.output(led, 0)
	time.sleep(bit_time*10)
	for x in range(13):
		GPIO.output(led, 1)		# 13 Edges for Footer
		time.sleep(bit_time/2)		#
		GPIO.output(led, 0)		#
		time.sleep(bit_time/2)		#
	GPIO.output(led, 1)
	time.sleep(bit_time*10)
	GPIO.output(led, 0)
	time.sleep(bit_time*10)


# loop laser output for a specified number of times
for x in range(loop):

	# send phrase over laser, letter by letter
	header()
	for letter in range (len(phrase)):
		send_letter(ord(phrase[letter]))
	footer()
		
	
# finish GPIO
GPIO.cleanup()

