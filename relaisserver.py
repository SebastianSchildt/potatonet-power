#!/bin/python3

import relaiscommands as rc
import serial
import time
import socketserver

DEVICE='/dev/ttyUSB0'





class RelaisRequestHandler(socketserver.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        print('New Request Handler')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        print('Waiting for data...')

        # Echo the back to the client
        while True:
            data=self.rfile.readline().strip()
            if len(data) == 0:
                break

            print("recv *"+str(data)+"*")
            if data == bytes("quit","utf-8"):
                self.request.send(bytes('Bye\n',"utf-8"))
                break
            print('recv()->"%s"', data)
            self.request.send(data)
            self.request.send(bytes('\n',"utf-8"))
            
            
        return

    def finish(self):
        print('Request Handler finish')
        return socketserver.BaseRequestHandler.finish(self)


class RelaisServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    
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


ser = serial.Serial(DEVICE, 19200, timeout=2)

cards=rc.setup(ser)

print("Detected boards:")
for card in cards:
    print("Found card "+str(card['address'])+" with firmware version "+str(card['firmware'])+". Checksum correct?: "+str(card['xorok']))
          


print("Starting server")
address = ('localhost', 2222) # let the kernel give us a port
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



