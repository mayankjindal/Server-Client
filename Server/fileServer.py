import socket
import threading
import os

def Download(name, sock):
	filen = str(sock.recv(1024).decode('utf-8'))
	if(os.path.isfile(filen)):
		
		sock.send("EXISTS ".encode('utf-8') + str(os.path.getsize(filen)).encode('utf-8'))
		userResponse = sock.recv(1024).decode('utf-8')
		if(userResponse[:2] == 'OK'):
			with open(filen, 'rb') as f:
				bytesToSend = f.read(1024)
				filesize = os.path.getsize(filen)
				TotalSend = len(bytesToSend)
				sock.send(bytesToSend)
				while(TotalSend < filesize):
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
					TotalSend += len(bytesToSend)

					
		else:
			sock.sendto("ERR".encode('utf-8'), ('10.7.3.94', 5000))
	print("Done")
	sock.close()

def Upload(name, sock):

	filen = str(sock.recv(1024).decode('utf-8'))
	print(filen)
	filename = ''
	temp = ''
	for i in range(len(filen)-1, 0, -1):
		if filen[i] == '/':
			break
		temp += filen[i]
	for i in range(len(temp)-1, -1, -1):
		filename += temp[i]

	filesize = str(sock.recv(1024).decode('utf-8'))
	print(filesize)
	#userResponse = str(sock.recv(1024).decode('utf-8'))
	if(filesize[-2:] == 'OK'):
		f = open('new_' + filename, 'wb')
		data = sock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while(totalRecv < int(filesize[:-2])):
			data = sock.recv(1024)
			totalRecv += len(data)
			f.write(data)
		f.close()
	sock.close()


def Main():
	host = '10.7.3.94'
	port = 5000
	s = socket.socket()
	s.bind((host, port))

	s.listen(5)

	print("Server Started.")
	while True:
		c, addr = s.accept()
		print("Client connected ip:<" + str(addr) + ">")
		reply = str(c.recv(1024).decode('utf-8'))
		if reply == 'D' or reply == 'd':		
			t = threading.Thread(target=Download, args=("DownThread", c))
			t.start()
		if reply == 'U' or reply == 'u':
			t = threading.Thread(target=Upload, args=("UpThread", c))
			t.start()
	s.close()

if __name__ == '__main__':
	Main()
