import simpy
import random
import networkx as nx
from distsim import * 
import matplotlib.pyplot as plt
import time

messageCount = 0
firstTime = None
lastTime = 0
ST = nx.Graph()


class FNode(Node):
	def __init__(self,*args):
		Node.__init__(self, *args)
		self.msgSent = False #msg sent diye bir değişken oluşturuyoruz. class içerisindeki obje.
		self.parent= None
		self.childs=[] # node çocuklerını tutacak
		self.others=[] # node çocuğu olmayan diğer nodeları tutacak.
		global ST
		ST.add_node(self.id)
		#mesaage type PROBE, ACK, REJECT 
	
	

	def run(self): # node çalıştığında neler yapacak burada belirtiyoruz.
		global messageCount
		global firstTime
		global lastTime
		global ST

		if self.id == 0:
			self.setTimer('timer1',2)

		while True:
			yield self.mailbox.get(1) #mailbox kontrol ediliyor.
			msg = self.receiveMessage()
			print('%d: %s received from %d at time %d' % (self.id,msg['type'],msg['sender'],self.env.now))
			if firstTime == None:
				firstTime = self.env.now
			lastTime = self.env.now
			if msg['type'] == "PROBE" :
				if self.parent == None: #parent tanımlanmamış ise.
					data = msg['data']

					self.parent = int(msg['sender'])
					ST.add_edge(self.parent,self.id)
					#print( '%d nin parentı %d' % (self.id, self.parent))
					for key in self.neighbors:
						if key == self.parent:
							self.neighbors[key] = 'parent'
						else:
							self.neighbors[key] = 'others'
					
					#print (self.neighbors)

					if not self.msgSent:
						self.sendMessageTo(msg['sender'],{'type':'ACK'}) #parentına ack gönderiyor.
						messageCount = messageCount + 1
						for key in self.neighbors:
							if self.neighbors[key] != 'parent':
								self.sendMessageTo(key,{'type':'PROBE','data':data})
								messageCount = messageCount +1
						self.msgSent = True 
					    
				else: 
					self.sendMessageTo(msg['sender'],{'type':'REJECT'})
					messageCount = messageCount +1

			elif msg['type'] == 'ACK':
				self.childs.append(msg['sender'])

			elif msg['type'] == 'REJECT':
				self.others.append(msg['sender'])

			elif msg['type'] == 'TIMEOUT':
				if msg['name'] == 'timer1':
					if self.id == 0:  # burada kontrol yapmamıza gerek yok.
						self.sendMessage({'type':'PROBE','data':5})
						messageCount = messageCount + len(self.neighbors)
 						#print( '%d nin parentı %d' % (self.id, self.parent))
						self.msgSent = True
		
	


			

#G = nx.path_graph(5)

def test(nodeCount):
	global messageCount
	global firstTime
	global lastTime
	global ST

	messageCount = 0
	firstTime = None
	lastTime = 0
	ST = nx.Graph()
	G = nx.watts_strogatz_graph(nodeCount,4,0.9)
	sys = System(FNode,nxGraph=G) 
	sys.env.run(1000)
	
	return messageCount, lastTime - firstTime, nx.diameter(ST)