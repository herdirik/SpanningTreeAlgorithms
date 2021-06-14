import simpy
import random
import networkx as nx
from distsim import * 
import matplotlib.pyplot as plt

messageCount = 0
firstTime = None
lastTime = 0
ST = nx.Graph()



class FNode(Node):
	def __init__(self,*args):
		Node.__init__(self, *args)
		self.msgSent = False 
		self.parent = None
		self.shouldsent = False
		global ST
		ST.add_node(self.id)

	def run(self): # node çalıştığında neler yapacak burada belirtiyoruz.
		global messageCount
		global firstTime
		global lastTime
		global ST
		
		if self.id == 0:
			self.setTimer('timer1',2)

		for key in self.neighbors: # ilk olarak komşuları ziyaret edilmemiş olarak tanımlıyoruz.
			self.neighbors[key] = False
			

		while True :
			yield self.mailbox.get(1) #mailbox kontrol ediliyor.
			msg = self.receiveMessage()
			print('%d: %s received from %d at time %d' % (self.id,msg['type'],msg['sender'],self.env.now))
			if firstTime == None:
				firstTime = self.env.now
			lastTime = self.env.now
			if msg['type'] == "TOKEN":
				data = msg['data']

				if self.parent == None: 
					self.parent = int(msg ['sender'])
					ST.add_edge(self.parent,self.id)
					self.neighbors[self.parent] = None #en son parenta TOKEN göndermesi icin parentı None yapıyoruz.
				
				for key in self.neighbors: 
					if self.neighbors[key] == False: #ziyaret edilmemis komşuya TOKEN gonderiyoruz.
						self.sendMessageTo(key,{'type':'TOKEN','data': data})
						messageCount = messageCount +1
						self.neighbors[key] = True 
						self.shouldsent = False
						break
					self.shouldsent = True

				if self.shouldsent == True: #Tüm komşuları ziyaret etmiş ise.
					if self.id != 0:
						self.neighbors[self.parent] = True
						self.sendMessageTo(self.parent,{'type':'TOKEN','data': data}) #en son parentına TOKEN gönderiyor.
						messageCount  = messageCount + 1
						self.msgSent = True
						
					else:
						self.msgSent = True

				if self.msgSent == True :
					break

					

			elif msg['type'] == "TIMEOUT":  
				if msg['name'] == 'timer1':
					if self.id == 0:
						self.parent = self.id
						for key in self.neighbors:
							if self.neighbors[key] == False:
								self.sendMessageTo(key,{'type':'TOKEN','data':5})
								messageCount = messageCount + 1
								self.neighbors[key] = True
								break
						

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
