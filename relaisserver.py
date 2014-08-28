#!/bin/python3

import relaiscommands as rc
import serial
import time

DEVICE='/dev/ttyUSB0'

ser = serial.Serial(DEVICE, 19200, timeout=2)

setupcmd=rc.setup()
print(str(setupcmd))

ser.write(setupcmd)

cards=rc.parseSetup(ser)

print("Detected boards:")
for card in cards:
    print("Found card "+str(card['address'])+" with firmware version "+str(card['firmware'])+". Checksum correct?: "+str(card['xorok']))
          


for i in range(0,7):
    (res,msg)=rc.relaisOn(i,ser)
    print("Result "+str(res)+": "+msg)
    time.sleep(0.5)
    
for i in range(0,7):
    (res,msg)=rc.relaisOff(i,ser)
    print("Result "+str(res)+": "+msg)
    time.sleep(0.5)

#(res,msg)=rc.relaisOff(0,ser)
#print("Result "+str(res)+": "+msg)

#(res,msg)=rc.relaisOn(0,ser)
#print("Result "+str(res)+": "+msg)



