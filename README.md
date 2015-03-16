# Optical_Data_Link
Use a raspberry pi and a laser pointer to send data (text) over a laser! This was made as a demonstration, so anyone can visualize digital data being transmitted.

**Parts List:**
* Raspberry Pi
* Laser Pointer
* 3 AAA batteries
* Solar Cell
* ADC (We used http://www.adafruit.com/product/1085, but it's a little overkill for this project)
* Transistor (We used an IRF520, also overkill for the power needed to drive a laser.
* Wires to hook everything up!

We used part from a Spectra sound kit (http://www.adafruit.com/product/1085), which is an analog version of this digital project. That kit allows you to send music over a laser, and doesn't use any digital signals.

**Raspberry Pi downloads:**
* sudo apt-get update
* sudo apt-get install python-dev
* sudo apt-get install python-rpi.gpio
* Also enable I2C to use the ADC, follow ADAfruit lesson 4 (https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

Run the reciever and laser_transmitter code in two terminals (or use two raspberry pis!)
* "sudo python Laser_Transmitter.py"
* "sudo python Receiver.py"

**Feel free to ask for more information!**
