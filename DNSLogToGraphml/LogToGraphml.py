#january 21th 2016
#this script constructs a Q matrix from a DNS log
#then it computes QQT, QTQ, Heuristic
#and format output for classification purposes


import time
import numpy, scipy.io
import sys
import datetime
import os
import networkx as nx, numpy as np
from networkx.algorithms import bipartite
from scipy.sparse import csc_matrix

from networkx.drawing.nx_agraph import graphviz_layout


import matplotlib.pyplot as plt



def lookFor(string,Dict):
	index = 0
   
	#global ipIndex, ipDict
	if stringIP not in ipDict:
		ipDict[stringIP] = ipIndex
		index = ipIndex
		ipIndex+=1
		#print "Sumando"
		#print ipIndex
		#exit()
	else:
		index = ipDict[stringIP]
	return index,ipIndex
def lookForIP(stringIP,ipDict,ipIndex):
	index = 0
   
	#global ipIndex, ipDict
	if stringIP not in ipDict:
		ipDict[stringIP] = ipIndex
		index = ipIndex
		ipIndex+=1
		#print "Sumando"
		#print ipIndex
		#exit()
	else:
		index = ipDict[stringIP]
	return index,ipIndex

def lookForDomain(stringDomain,domainDict,domainIndex):
	index = 0
	#global domainIndex, domainIndex
	if stringDomain not in domainDict:
		domainDict[stringDomain] = domainIndex
		index = domainIndex
		domainIndex+=1
	else:
		index = domainDict[stringDomain]
	return index,domainIndex

def initProgram(logFile,logFile2,out):
	
	#opening file    
	
	nodeIndex = 0
	_output = ""

	f = open(logFile,'r')
	
	nodes = []
	setEdgesG1 = []
	setEdgesG2 = []
	listOfNodes = []

	for line in f:
		#print line
	
		ipIndex = -1
		domainIndex = -1

		data = str(line).split(' ') # splitting a log line      
		ipPort = str(data[3]).split('#') #splitting port and ip
		domain = data[7]

		if ipPort[0] not in listOfNodes:
			listOfNodes.append(ipPort[0])
			nodes.append(nodeIndex)
			nodeIndex+=1

		if domain not in listOfNodes:
			listOfNodes.append(domain)
			nodes.append(nodeIndex)
			nodeIndex+=1

		ipIndex = listOfNodes.index(ipPort[0])
		domainIndex = listOfNodes.index(domain)

		if [ipIndex,domainIndex] not in setEdgesG1:
			setEdgesG1.append([ipIndex,domainIndex])

	f.close()
	f = open(logFile2,'r')
	for line in f:
		#print line
	
		ipIndex = -1
		domainIndex = -1

		data = str(line).split(' ') # splitting a log line      
		ipPort = str(data[3]).split('#') #splitting port and ip
		domain = data[7]
		if ipPort[0] not in listOfNodes:
			listOfNodes.append(ipPort[0])
			nodes.append(nodeIndex)
			nodeIndex+=1

		if domain not in listOfNodes:
			listOfNodes.append(domain)
			nodes.append(nodeIndex)
			nodeIndex+=1

		ipIndex = listOfNodes.index(ipPort[0])
		domainIndex = listOfNodes.index(domain)

		if [ipIndex,domainIndex] not in setEdgesG2:
			setEdgesG2.append([ipIndex,domainIndex])

	f.close()
	s = ""
	while len(setEdgesG1) >0:
		e = setEdgesG1.pop()
		s+='<edge source="'+str(e[0])+'" target="'+str(e[1])+'" '
		s+='g1="10" '
		posFlag = 0

		j = 0
		flagExit = 0
		while len(setEdgesG2) > 0 and flagExit == 0:
			# print setEdgesG2[j]
			if [e[0],e[1]] == setEdgesG2[j]:
				# print [e[0],e[1]]
				if posFlag == 0:
					s+='g2="20" '
					posFlag = 1
				setEdgesG2.pop(j)
				j-=1
			j+=1
			if j >= len(setEdgesG2):
				flagExit=1
		s+="/>\n"
	for i in range(len(setEdgesG2)):
		s+='<edge source="'+str(setEdgesG2[i][0])+'" target="'+str(setEdgesG2[i][1])+'" '
		s+='g2="20" '
		s+='/>\n'
	
	sInitial = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
	sFinal = '</graph>\n</graphml>'

	sNodes = ""
	for i in range(0,len(nodes)):
		sNodes+='<node id="'+str(i)+'"/>\n'
	f = open(out+".graphml","w")
	f.write(sInitial+sNodes+s+sFinal)
	f.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.exit('Usage: %s    log-file-1   log-file-1  output-filename' % sys.argv[0])

	logFile = str(sys.argv[1])
	logFile2 = str(sys.argv[2])
	out = str(sys.argv[3])
	
	initProgram(logFile,logFile2,out)


