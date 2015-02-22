#!/bin/python3


#initialize and scan for cards
# 1 Addr x XOR
#always use bcast addr
def setup(ser):
    print("Setup: Emptying card buffers")
    readanddiscard(ser)
    command=1
    addr=1
    data =0

    xor=command^addr^data
    toSend= bytes([command, addr, data, xor])
    ser.write(toSend)
    return parseSetup(ser)

#switch relais on
# 6 Addr data XOR
# function does not take board address, but instead numbers relais starting
# from 0 accross all boards
# data is a bitmask for all relais to be switched on, but we only support
# switching one relais at a time
def relaisOn(num,cards,ser):
    command=6
    addr=int((int(num)/8)+1)
    bit=int(num)%8
    data= 1 << bit
    xor=command^addr^data

    if addr < 1 or addr > len(cards):
        return(False,"No such port. "+str(num)+" requested, max is "+str(len(cards)*8-1))


    toSend=bytes([command, addr, data, xor])
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
def relaisOff(num, cards, ser):
    command=7
    addr=int((int(num)/8)+1)
    bit=int(num)%8
    data= 1 << bit
    xor=command^addr^data

    if addr < 1 or addr > len(cards):
        return(False,"No such port. "+str(num)+" requested, max is "+str(len(cards)*8-1))


    toSend=bytes([command, addr, data, xor])
    ser.write(toSend)
    
    data=ser.read(4)
    if len(data)==0:
        return(False,"Communication Error")

    if data[0] == 0xff:
        return(False,"Command Error")

    if not data[0] == 248:
        return(False,"Unknown response: "+str(data))

    return (True, "OK")


#Get current port state from all cards in cards. Ports in sorder of cards
# 2 Addr x XOR
def getPortState(cards, ser):
    ports=[]
    for card in cards:
        command=2
        addr=int(card['address'])
        data=0
        xor=command^addr^data
        toSend=bytes([command, addr, data, xor])
        #print("Query port :"+str(toSend))
        ser.write(toSend)
    
        data=ser.read(4)
        if len(data)==0:
            return(False,"Communication Error", ports)

        if data[0] == 0xff:
            return(False,"Command Error", ports)

        if not data[0] == 253:
            return(False,"Unknown response: "+str(data),ports)

        if not xorok(data):
            return(False,"Checksum wrong",ports)
        
        boardports=data[2]
        for i in range(0,8):
            ports.append( (boardports>>i)&0x01 )
        


    return(True, "OK", ports)

    



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

        print("Got SETUP answer:", end="")
        for byte in data:
            print(""+format(byte, '02x'), end="")
        print("") 
      
        if len(data) != 4:
            print("Short read. Expected 4 got "+str(len(data)))
            continue
 
        if data[0] == 1: #last card broadcasting back to server
            print("Last board in chain reached")
            #could break, but for safety read again
            continue

        if data[0] != 254:
            print("Unknown SETUP response: "+str(data[0]))
            continue
        
        if xorok(data):
            print("Found board")
            card['address']=currAddr
            card['firmware']=data[2]
            card['xorok']= xorok(data)
            cards.append(card)
            currAddr=currAddr+1
        else:
            print("Checksum error in MSG: ", end="")

    return cards

# In case of a failure read and discard data until no more data comming from relais
# read at most 1024 bytes (256 msgs)
def readanddiscard(ser):
    command=0
    addr=0
    data =0

    xor=command^addr^data
    toSend= bytes([command, addr, data, xor])
    ser.write(toSend)

    data=ser.read(1024)
    print("Ignored "+str(len(data))+" bytes from relaiscard")


                            
def xorok(data):
    return  ( data[3]==(data[0]^data[1]^data[2]))
    
