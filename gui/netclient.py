import socket


HOST, PORT = "localhost", 2222
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init():
	global sock
	try:
		sock.connect((HOST, PORT))
		return True
	except:
		print("Can not open connection")
		return False

def transceive(command):
	global sock
	try:
		sock.sendall(bytes(command+"\n","utf-8"))
		data=readline(sock)
		return data
	except OSError as e:
		print("Communication error: {0}".format(err))
		return("505 ")

def close():
	global sock
	sock.close()

def readline(sock, recv_buffer=4096, delim='\n'):
	buffer = ''
	data = True
	while data:
		data = sock.recv(recv_buffer)
		buffer += data.decode("utf-8")

		if buffer[-1] == '\n':
			return buffer[:-1]
	



