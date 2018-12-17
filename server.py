import socket
import threading
import glob
import time

#conexao ao DNS
UDP_IP = "localhost"
UDP_PORT = 5005

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

fim = "fim"
class threadFile(threading.Thread):
	def __init__(self,threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName
	def run(self):
		print("Starting: "+self.threadName)
		fileTransfer(self.threadName)

def fileTransfer(threadName):
	Sequence = 0
	hostFile = 'localhost'
	portFile = 3030
	sUDP.bind((hostFile,portFile))
	relogio = time.localtime()
	#arq = open('picture.png','rb')
	while True:
		client,addr = sUDP.recvfrom(4096)
		dados = client.decode()
		print(dados)
		if(dados=="1"):
			client,addr = sUDP.recvfrom(4096)
			choice = client.decode()
			#print(choice)
			arq=open(str(choice),'rb')
			for i in arq.readlines():
				millis = int (round(time.time()*100) + (relogio.tm_sec)*100)
				timeout = int (round(time.time()*1000) + (relogio.tm_sec)*1000)
				
				sUDP.sendto(i,addr) #envia arquivo
				
				Sequence = Sequence +1
				env = str(Sequence)
				sUDP.sendto(env.encode("UTF-8"),addr) #envia sequence
				#time
				endMillis = int (round(time.time()*100) + (relogio.tm_sec)*100)
				tempo = (endMillis - millis) 

				if(tempo>=timeout):
					sUDP.sendto(i,addr) #retransmite o  arquivo
					Sequence = Sequence-1
					sUDP.sendto(env.encode("UTF-8"),addr) #retransmite o sequence
					
				dataAck ,addr2 = sUDP.recvfrom(4096) #recebe Ack
				resposta = dataAck.decode()
				print("Ack:",resposta)

				if (env != resposta):
					sUDP.sendto(i,addr)# retransmite o arquivo
					Sequence = Sequence -1
					sUDP.sendto(env.encode("UTF-8"),addr)# retransmite o sequence
			sUDP.sendto(fim.encode("UTF-8"),addr)		
			arq.close()
			dados = "0"
		elif(dados=="2"):
			for f in glob.glob('*.*'):
				put = str(f)
				sUDP.sendto(put.encode("UTF-8"),addr)
			sUDP.sendto(fim.encode("UTF-8"),addr)
			dados=="0"
		elif(dados=="3"):
			sUDP.close()
			break

class myThread (threading.Thread):
	def __init__(self,threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName
	def run(self):
		print("Starting "+self.threadName)
		servidor_dns(self.threadName)

def servidor_dns(threadName):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	while True:
		dominio = input('Entre com o dominio: ')
		sock.sendto(dominio.encode("UTF-8"),(UDP_IP,UDP_PORT))
		
		host = input('Entre com o host: ')
		sock.sendto(host.encode("UTF-8"),(UDP_IP,UDP_PORT))
		
		port = input('Entre com a porta: ')
		sock.sendto(port.encode("UTF-8"),(UDP_IP,UDP_PORT))
		sock.close()
		break
		
thread_udp = myThread("Thread-1-UDP")
thread_file = threadFile("Thread-2-File")

thread_udp.start()
thread_file.start()
thread_file.join()
thread_udp.join()
print ("Exiting Main Thread")
