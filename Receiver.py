## Photonic Device Research Group
## University of Illinois at Urbana-Champaign
## IEEE Photonics Society
## Spring 2015

#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15

def signal_handler(signal, frame):
        print '\nStopping\n'
	#print h_max
	adc.stopContinuousConversion()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C to exit'

ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

# Select the gain
# gain = 6144  # +/- 6.144V
# gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
#sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
# sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
sps = 860  # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)

adc.startContinuousConversion(0, gain, sps)
start_time = time.time()

debug = False 	# Make "True" for verbose mode (prints binary ASCII)

#setup
baseline = adc.getLastConversionResults()/1000
h_counter = 0
l_counter = 0
h_max = 0
threshold = 0.1
header = False
footer = False
header_sig = True
footer_sig = True
header_count = 0
signal = False
signal_ready = False
bit_ready = False
wait = -1
bit_time = 0
bit = int('0',2)
letter = int('00000000',2)
bit_position = 8
complete = 0

while True:
	volts = adc.getLastConversionResults()/1000
	cur_time = time.time()-start_time
	#print "%.6f" % (volts),cur_time
	time.sleep(1/(float(sps)))
	#start_time = start_time+1/float(sps) 
	if volts > (baseline+threshold):
		l_counter = 0   #reset low_counter on high signal
		h_counter = h_counter+1
		if h_counter >= h_max*0.95:
			if h_counter > h_max:
				h_max = h_counter
			header = True
			signal = False
			signal_ready = False
			#print "long high"
			header_count = 0
	else:
		h_counter = 0	#reset high_counter on low signal
		l_counter = l_counter+1
		if l_counter >= h_max*1.1:
			if signal:
				if debug:
					print "\nConnection Interrupted"
				else:
					print "\n\nConnection Interrupted"
				complete = 0
				signal = False
				signal_ready = False
				wait = -1
				letter = int('00000000',2)
				bit_position = 8
		if l_counter >= h_max*0.90:
			footer = True
			footer_count = 0

	#look for header
	if header:
		if volts < (baseline+threshold):
			header_sig = False
		else:
			if header_sig == False:
				header_count = header_count+1
				header_sig = True
		if l_counter >= h_max*0.95:
			#print "long low"
			if header_count == 11:
				if debug:
					print "\nHeader Received...\n"
				else:
					print "\n",
				complete = 1
				header = False
				header_count = 0
				signal = True
				footer = False
				wait = -1
			else:
				header = False
				header_count = 0
				signal = False

	#look for footer
	if footer:
		if volts > (baseline+threshold):
			footer_sig = False
		else:
			if footer_sig == False:
				footer_count = footer_count+1
				footer_sig = True
		if h_counter >= h_max*0.90:
			#print "long low"
			if footer_count == 13:
				if debug:
					print "\n...Footer Received\n"
				else:
					print "\n"
				footer = False
				footer_count = 0
				if complete == 1:
					if debug:
						print "Successful Transmission!\n"
					break
			else:
				footer = False
				footer_count = 0


	#decode signal after header passes
	if signal:
		if (wait == -1) and (h_counter > 0):
			signal_ready = True
			bit_time = 0
			wait = -3
		if signal_ready:
			bit_time = bit_time + 1
			if l_counter > 0:
				wait = -2
				signal_ready = False
		if wait == -2:
			#wait for bit to finish if it is high
			if l_counter > 0:
				wait = 2*bit_time
		if wait > 0:
			if h_counter > 0:
				bit_ready = True
			if bit_ready:
				wait = wait-1
		if wait == 0:
			bit_ready = False
			if volts > (baseline+threshold):
				bit = int('1',2)
			else:
				bit = int('0',2)
			#print bit
			wait = -2
			letter = letter<<1	# leftshift by 1
			letter = letter|bit	# bitwise OR
			bit_position = bit_position-1
			if bit_position == 0:
				if letter >= 3:
					if debug:
						print "{0:08b} --> ".format(letter),
						print chr(letter)
					else:
						sys.stdout.write('%s' % chr(letter))	# print ASCII char
						sys.stdout.flush()
					bit_position = 8
					letter = int('00000000',2)
			



# Read channel 0 in single-ended mode using the settings above
# volts = adc.readADCSingleEnded(0, gain, sps) / 1000

# To read channel 3 in single-ended mode, +/- 1.024V, 860 sps use:
# volts = adc.readADCSingleEnded(3, 1024, 860)

#print "%.6f" % (volts)

#startContinuousConversion(self, channel=0, pga=6144, sps=250): 
#  "Starts the continuous conversion mode and returns the first ADC reading \
# in mV from the specified channel. \
#The sps controls the sample rate. \
#The pga must be given in mV, see datasheet page 13 for the supported values. \
#Use getLastConversionResults() to read the next values and \
#stopContinuousConversion() to stop converting."
