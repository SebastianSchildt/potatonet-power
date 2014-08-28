#!/bin/python3


#initialize and scan for cards
# 1 Addr x XOR
#always use bcast addr
def setup():
    command=1
    addr=1
    data =0

    xor=command^addr^data
    return bytes([command, addr, data, xor])

#switch relais on
# 6 Addr data XOR
# function does not take board address, but instead numbers relais starting
# from 0 accross all boards
# data is a bitmask for all relais to be switched on, but we only support
# switching one relais at a time
def relaisOn(num,ser):
    command=6
    addr=int((int(num)/8)+1)
    bit=int(num)%8
    data= 1 << bit
    xor=command^addr^data

    toSend=bytes([command, addr, data, xor])
    print("relais on :"+str(toSend))
    ser.write(toSend)
    
    data=ser.read(4)
    if len(data)==0:
        return(False,"Communication Error")

    if data[0] == 0xff:
        return(False,"Command Error")

    if not data[0] == 249:
        return(False,"Unknown response: "+str(data))

    return (True, "OK")

#switch relais off
# 6 Addr data XOR
# function does not take board address, but instead numbers relais starting
# from 0 accross all boards
# data is a bitmask for all relais to be switched on, but we only support
# switching one relais at a time
def relaisOff(num,ser):
    command=7
    addr=int((int(num)/8)+1)
    bit=int(num)%8
    data= 1 << bit
    xor=command^addr^data

    toSend=bytes([command, addr, data, xor])
    print("relais off :"+str(toSend))
    ser.write(toSend)
    
    data=ser.read(4)
    if len(data)==0:
        return(False,"Communication Error")

    if data[0] == 0xff:
        return(False,"Command Error")

    if not data[0] == 248:
        return(False,"Unknown response: "+str(data))

    return (True, "OK")




    



#parse response after setup, return card structure
def parseSetup(ser):
    cards=[]
    currAddr=1
    while True:
        card={}
        data=ser.read(4)
        
        if len(data)==0:
            print("All boards found")
            break
        
        if data[0] == 1: #last card broadcasting back to server
            print("Last board in chain reached")
            #could break, but for safety read again
            continue

        

        print("Found board")
        card['address']=currAddr
        card['firmware']=data[2]
        card['xorok']= ( data[3]==(data[0]^data[1]^data[2]))
        cards.append(card)
        currAdr=+1

    return cards

                            

    
