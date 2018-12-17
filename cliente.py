import socket
import threading
import glob

#conexao ao DNS
UDP_IP = "localhost"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sUdp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

class threadFile(threading.Thread):
	def __init__(self,threadName,hostFile,portFile,address):
		threading.Thread.__init__(self)
		self.threadName = threadName
		self.hostFile = hostFile
		self.portFile = portFile
		self.address = address
	def run(self):
		print("Starting: "+self.threadName)
		fileTransfer(self.threadName,self.hostFile,self.portFile,self.address)

def fileTransfer(threadName,hostFile,portFile,address):
	
	print("fileTransfer Client TCP")
	#arq = open('arquivo/picture.png','wb')
	dist = 'arquivo/'
	while  True:
		digit = input("Digite 1 para download, 2 para listar file, 3 para fechar conection ")
		sUdp.sendto(digit.encode("UTF-8"),(hostFile,int(portFile)))	
		if(digit=="1"):
			digito2 = input("Digite o nome do arquivo: ")
			dist2 = dist + digito2
			sUdp.sendto(digito2.encode("UTF-8"),(hostFile,int(portFile)))
			#print(dist2)
			arq = open(dist2,'wb')
			while True:
				dados, addr = sUdp.recvfrom(4096) #recebe file
				arq.write(dados)
				#print(dados)
				
				dados2, addr2 = sUdp.recvfrom(4096) # recebe sequence
				seq = dados2.decode()
				print("sequence: "+seq)
				Ack = seq
				sUdp.sendto(Ack.encode("UTF-8"),(hostFile,int(portFile)))#envia Ack
						
		elif(digit=="2"):
			while True:
				rec, addr2 = sUdp.recvfrom(4096) #recebe lista
				resp = rec.decode()
				print (resp)
				if (resp == 'fim'):
					print("saiu")
					digit=="0"
					break
				dados2, addr2 = sUdp.recvfrom(4096) #recebe sequence
				seq = dados2.decode()
				#print("sequence: "+seq)
				Ack = seq
				sUdp.sendto(Ack.encode("UTF-8"),(hostFile,int(portFile))) #envia ack
				#print(resp)
				
		elif(digit=="3"):
			sUdp.sendto(digit.encode("UTF-8"),(hostFile,int(portFile)))
			sUdp.close()
			break
	

class myThread (threading.Thread):
	def __init__(self,threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName
	def run(self):
		print("Starting "+self.threadName)
		client_dns(self.threadName)

def client_dns(threadName):
	dominio = input('Entre com um dominio: ')
	sock.sendto(dominio.encode("UTF-8"),(UDP_IP,UDP_PORT))
	while True:
		dados, addr = sock.recvfrom(1024)
		dados2, addr = sock.recvfrom(1024)
		thread_file = threadFile("Thread-1-TCP",dados.decode(),dados2.decode(),addr)
		thread_file.start()
		thread_file.join()
		break
				
			
thread_udp = myThread("Thread-1-UDP")

thread_udp.start()

thread_udp.join()

print ("Exiting Main Thread")
