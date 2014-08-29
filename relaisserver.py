#!/bin/python3

import relaiscommands as rc
import serial
import time

DEVICE='/dev/ttyUSB0'

ser = serial.Serial(DEVICE, 19200, timeout=2)

cards=rc.setup(ser)

print("Detected boards:")
for card in cards:
    print("Found card "+str(card['address'])+" with firmware version "+str(card['firmware'])+". Checksum correct?: "+str(card['xorok']))
          



(res,msg,state)=rc.getPortState(cards,ser)
if not res:
    print("Error getting state"+str(msg))
else:
    print("Ports "+str(state))

for i in range(0,16):
    (res,msg)=rc.relaisOn(i,ser)
    #print("Result "+str(res)+": "+msg)
    print("State "+str(rc.getPortState(cards,ser)[2]))
    time.sleep(0.5)


(res,msg,state)=rc.getPortState(cards,ser)
if not res:
    print("Error getting state"+str(msg))
else:
    print("Ports "+str(state))

for i in range(0,16):
    (res,msg)=rc.relaisOff(i,ser)
    print("Result "+str(res)+": "+msg)
    time.sleep(0.5)


(res,msg,state)=rc.getPortState(cards,ser)
if not res:
    print("Error getting state"+str(msg))
else:
    print("Ports "+str(state))

#(res,msg)=rc.relaisOff(0,ser)
#print("Result "+str(res)+": "+msg)

#(res,msg)=rc.relaisOn(0,ser)
#print("Result "+str(res)+": "+msg)



