#!/usr/bin/python

import sys, getopt
from collections import OrderedDict
	
class Node:
		def init(self, name, parent, cost):
			self.name = name
			self.parent = parent
			self.cost = cost
			self.color = "white"
			
		def update(self, parent, cost):
			self.parent = parent
			self.cost = cost + parent.cost 
			

class GraphInfo:
	
	def init(self, sourceNode, destNode, pathGraph, nodes, time):
		self.sourceNode = sourceNode
		self.destNode = destNode
		self.pathGraph = pathGraph
		self.nodes = nodes
		self.time = time
		
	def BFS(self, time):
		
		queue = []
		queue.append(self.nodes[self.sourceNode[0]])
		self.nodes[self.sourceNode[0]].cost = time
		
		while queue:
			parent = queue[0]
			parentName = parent.name
			del queue[0]
			if parentName in self.destNode:
				return(parentName + " " + str(parent.cost % 24))
				break
			children = []
			for child in self.pathGraph[parent.name]:
				if self.nodes[child].color != "black" and self.nodes[child].color != "grey":
					children.append(child)
			children.sort()
			while children:
				child = children[0]
				del children[0]
				self.nodes[child].update(parent, 1)
				self.nodes[child].color = "grey"
				queue.append(self.nodes[child])
			parent.color = "black"
		return("None")
	
	def UpdateNodes(self, queue, parent):
		#sort for faster exec
		for key, value in queue.items()	:
			if key.parent == parent:
				key.update(parent, pathGraph[parent][key][0] )
				value = self.nodes[key].cost
		
		
	def UCS(self, time):
			
		queue = {}
		self.nodes[self.sourceNode[0]].cost = time
		queue[self.nodes[self.sourceNode[0]]] = time
		costQueue = OrderedDict(sorted(queue.items(), key = lambda t: (t[1],t[0])))
		
		while queue:
			items = list(costQueue.items())
			items.reverse()
			costQueue = OrderedDict(items)
			parentNode = costQueue.popitem()
			parent = parentNode[0]
			parentName = parentNode[0].name
			parentCost = parentNode[0].cost
			del queue[parent]
				
			if parentName in self.destNode:
				return(parentName + " " + str(parentCost % 24))
				break
			children = []
			for child in self.pathGraph[parentName]:
				if self.nodes[child].color == "grey":
					if parentCost + self.pathGraph[parentName][child][0] <= self.nodes[child].cost:
						if (parentCost % 24) not in self.pathGraph[parentName][child][1]:
							self.nodes[child].update(parent, self.pathGraph[parentName][child][0])
							queue[self.nodes[child]] = self.nodes[child].cost
							self.UpdateNodes(queue, child)
				elif self.nodes[child].color == "white":
					children.append(child)
		
			for child in children:
				if (parentCost % 24) not in self.pathGraph[parentName][child][1]:
					self.nodes[child].update(parent, self.pathGraph[parentName][child][0])
					queue[self.nodes[child]] = self.nodes[child].cost
					self.nodes[child].color = "grey"
			
			costQueue = OrderedDict(sorted(queue.items(), key = lambda t: (t[1],t[0].name)))
			parent.color = "black"
			
		return("None")
		
	def DFS(self, time):
			
		queue = []
		self.nodes[self.sourceNode[0]].cost = time
		queue.append(self.nodes[self.sourceNode[0]])
			
		while queue:
			
			parent = queue.pop()
			if parent.color == "black":
				while parent.color != "black":
					parent = queue.pop()
			parentName = parent.name
			if parentName in self.destNode:
				return(parentName + " " + str(parent.cost % 24))
				break
			children = []
			for child in self.pathGraph[parentName]:
				if self.nodes[child].color != "black":
					children.append(child)
			children.sort()
			while children:
				child = children.pop()
				self.nodes[child].update(parent, 1)
				queue.append(self.nodes[child])
			parent.color = "black"	
		return("None")	
			
			
	
		
				
def parsePath(paths, allNodes):
	pipeGraph = {}
	for node in allNodes:
		pipeGraph[node] = {}
	for path in paths:
		pipe = path.split()
		
		cost = int(pipe[2])
		pipeGraph[pipe[0]][pipe[1]] = [cost]
		list = []
		for i in range(0,int(pipe[3])):
			z = 4 + i
			offset1, offset2 = map(int,pipe[z].split('-'))
			for y in range(offset1,offset2+1): #consider time = 24 cases
				list.append(y)
		pipeGraph[pipe[0]][pipe[1]].append(list)	
	return pipeGraph
	

	
def main(argv):
	inputFile = ""
	outputFile = "output.txt"
	
	#parsing the arguements for input file name
	opts, args = getopt.getopt(argv,'i:')
	for opt, arg in opts:
		if opt == '-i':
			inputFile = arg
	
	#opening the file for read
	txt = open(inputFile)
	outTxt = open(outputFile, "w")
	t = int(txt.readline())
	
	while t:
		pathGraph = {}
		sourceNode = []
		paths = []
		destNodes = []
		middleNodes = []
		noPipes = 0
		
		task = txt.readline().rstrip()
		sourceNode = txt.readline().split()
		destNodes = txt.readline().split()
		middleNodes = txt.readline().split()
		noPipes = int(txt.readline())
		for i in range(0,noPipes):
			paths.append(txt.readline().rstrip())
		
		noNodes = len(destNodes) + len(middleNodes) + 1
		allNodes = sourceNode + middleNodes + destNodes
		nodeList = {}		
		
		pathGraph = parsePath(paths, allNodes)
	
		time = int(txt.readline())
		
		for node in allNodes:
			x = Node()
			x.init(node, '', 0)
			nodeList[node] = x 
		g = GraphInfo()
		g.init(sourceNode, destNodes, pathGraph, nodeList, time)
		if task == "BFS":
			outTxt.write(g.BFS(time) + '\n')
		elif task == "DFS":
			outTxt.write(g.DFS(time) + '\n')
		elif task == "UCS":
			outTxt.write(g.UCS(time) + '\n')
		txt.readline() #for the delimiter between two test cases; to be reviewed for last input
		t -= 1
	txt.close()
	outTxt.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])
	