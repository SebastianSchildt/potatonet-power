#!/bin/python3

import relaiscommands as rc
import reliablechoice as tplink

import serial
import time
import socketserver
import sys

DEVICE='/dev/ttyS0'

EXPECTED_CARDS=3
EXPECTED_FIRMWARES = [11]



class RelaisRequestHandler(socketserver.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        print('New Request Handler')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        global cards, ser
        print('Waiting for data...')

        while True:
            data=self.rfile.readline().strip()
            if len(data) == 0:
                break

            if data == bytes("quit","utf-8"):
                
                self.request.send(bytes('200 Bye\n',"utf-8"))
                break
            
            cmd=data.decode('utf-8').split()
            if len(cmd) == 0:
                self.request.send(bytes('500 No comand\n',"utf-8"))
                continue

            ########### QUERY STATE
            if cmd[0] == 'state':
                reply="200 "
                (result,msg,state)=rc.getPortState(cards,ser)
                if not result:
                    self.request.send(bytes('400 Error getting port state. '+str(msg)+'\n',"utf-8"))
                    continue
                    
                for port in state:
                    reply+=(str(port)+", ")
                reply=reply[:-2]+'\n'
                self.request.send(bytes(reply,'utf-8'))
                
            ########### SWITCH ON
            elif cmd[0] == 'on':
                if len(cmd) != 2:
                    self.request.send(bytes('500 Wrong numebr of arguments. 1 needed\n',"utf-8"))
                    continue
                try:
                    nr=int(cmd[1])
                except ValueError:
                    self.request.send(bytes('500 Argument must be an int\n',"utf-8"))
                    continue
                    
                (res,msg)=rc.relaisOn(nr,cards, ser)
                if not res:
                    self.request.send(bytes('400 Error switching port on. '+str(msg)+'\n',"utf-8"))
                    continue
                self.request.send(bytes('200 OK\n',"utf-8"))

            ########### SWITCH OFF
            elif cmd[0] == 'off':
                if len(cmd) != 2:
                    self.request.send(bytes('500 Wrong numebr of arguments. 1 needed\n',"utf-8"))
                    continue
                try:
                    nr=int(cmd[1])
                except ValueError:
                    self.request.send(bytes('500 Argument must be an int\n',"utf-8"))
                    continue
                    
                (res,msg)=rc.relaisOff(nr,cards, ser)
                if not res:
                    self.request.send(bytes('400 Error switching port off. '+str(msg)+'\n',"utf-8"))
                    continue
                self.request.send(bytes('200 OK\n',"utf-8"))

            ########### TEST
            elif cmd[0] == 'test':
                for i in range(0,len(cards)*8):
                    (res,msg)=rc.relaisOn(i,cards,ser)
                    if not res:
                        self.request.send(bytes('400 Test failed at '+str(i)+'. '+str(msg)+'\n',"utf-8"))
                        continue
                    time.sleep(0.1)
                
                for i in range(0,len(cards)*8):
                    (res,msg)=rc.relaisOff(i,cards,ser)
                    if not res:
                        self.request.send(bytes('400 Test failed at '+str(i)+'. '+str(msg)+'\n',"utf-8"))
                        continue
                    time.sleep(0.1)
                    
                self.request.send(bytes('200 OK\n',"utf-8"))

	    ########### TPLINK status
            elif cmd[0] == 'tpstate':
                    (enabled,link)=tplink.getState()
		    #unify list: first bit=enabled, second bit=link
                    if len(enabled) == 0 or len(link)==0:
                        self.request.send(bytes('400 Invalid data received','utf-8'))
                        continue
                    print("Enabled: "+str(enabled))
                    print("Link: "+str(link))

                    for port in range(0,len(enabled)):
                       if int(link[port]) != 0:
                          enabled[port]=int(enabled[port])+2

                    reply="200 "
                    for port in enabled:
                       reply+=(str(port)+", ")
                    reply=reply[:-2]+'\n'
                    self.request.send(bytes(reply,'utf-8'))

            ########### SWITCH ON
            elif cmd[0] == 'tpon':
                if len(cmd) != 2:
                    self.request.send(bytes('500 Wrong numebr of arguments. 1 needed\n',"utf-8"))
                    continue
                try:
                    nr=int(cmd[1])
                except ValueError:
                    self.request.send(bytes('500 Argument must be an int\n',"utf-8"))
                    continue
                    
                res=tplink.setPort(nr,True)
                if not res:
                    self.request.send(bytes('400 Error switching port on.\n',"utf-8"))
                    continue
                self.request.send(bytes('200 OK\n',"utf-8"))

            ########### SWITCH OFF
            elif cmd[0] == 'tpoff':
                if len(cmd) != 2:
                    self.request.send(bytes('500 Wrong numebr of arguments. 1 needed\n',"utf-8"))
                    continue
                try:
                    nr=int(cmd[1])
                except ValueError:
                    self.request.send(bytes('500 Argument must be an int\n',"utf-8"))
                    continue
                    
                res=tplink.setPort(nr,False)
                if not res:
                    self.request.send(bytes('400 Error switching port off.\n',"utf-8"))
                    continue
                self.request.send(bytes('200 OK\n',"utf-8"))
		
            ########### UNKNOWN CMD                
            else:
                self.request.send(bytes('500 Unknown comand: '+str(cmd[0])+'\n',"utf-8"))
                
            
            
        return

    def finish(self):
        print('Request Handler finish')
        return socketserver.BaseRequestHandler.finish(self)


class RelaisServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    
    def __init__(self, server_address, handler_class=RelaisRequestHandler):
        print('Init server')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def serve_forever(self):
        print('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def server_close(self):
        print('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        print('finish_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        print('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address)


global ser
ser = serial.Serial(DEVICE, 19200, timeout=2)

global cards
cards=rc.setup(ser)

print("Detected boards:")
for card in cards:
    print("Found card "+str(card['address'])+" with firmware version "+str(card['firmware'])+". Checksum correct?: "+str(card['xorok']))

# Sanity checks, and exit if something is wrong
if len(cards) != EXPECTED_CARDS:
    print("Expected "+str(EXPECTED_CARDS)+" but found "+str(len(cards))+". Exiting.")
    sys.exit(-1)

for card in cards:
    if card['firmware'] not in EXPECTED_FIRMWARES:
        print("Found unexpected firmware "+str(card['firmware'])+". Exiting.")          
        sys.exit(-2)

print("Starting server")
address = ('127.0.0.1', 2222) # let the kernel give us a port
server = RelaisServer(address, RelaisRequestHandler)
server.serve_forever()




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



