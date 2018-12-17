import socket
import threading

UDP_IP = ""
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))


class myThread (threading.Thread):
	def __init__(self,threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName
	def run(self):
		print ("Starting "+self.threadName)
		server_dns (self.threadName)

def server_dns(threadName):	
	while True:
		data, addr = sock.recvfrom(1024)
		dominioDNS = data
		print(dominioDNS)
		sock.sendto(dominioDNS,addr)

		data1, addr1 = sock.recvfrom(1024)
		hostDNS = data1
		print(hostDNS)
		sock.sendto(hostDNS,addr1)

		data2, addr2 = sock.recvfrom(1024)
		portaDNS = data2
		print(portaDNS)
		sock.sendto(portaDNS,addr2)
		
		data3, addr3 = sock.recvfrom(1024)
		if (data3==dominioDNS):
			sock.sendto(hostDNS,addr3)
			sock.sendto(portaDNS,addr3)
		break


thread_dns_udp = myThread("Thread-1")
thread_dns_udp.start()
thread_dns_udp.join()
print("Exiting Main Thread")