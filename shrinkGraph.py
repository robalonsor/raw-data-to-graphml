import random

fileName = raw_input("Name of input file:   ")
fGraph = open(fileName)
outputFile = raw_input("Name of the output file:    ")
per = float(raw_input("percentage to remove (0.9-0.1)"))
#removing edges
sEdges = ""
sNodes = ""
#toRemove = 0.3 # 10% of the edges
toRemove = per
totalEdges = 0
for line in fGraph:
	if '<node' in line:
		sNodes+=line
	if '<edge' in line:
		totalEdges+=1
		sEdges+=line

fGraph.close()

listOfEdges = sEdges.split("\n")[:-1]
edgesToDel = int(totalEdges*toRemove)

print "Number of edges in the graph  ",len(listOfEdges)
print "Total edges to remove from graph  ", edgesToDel
totalNei =0
while edgesToDel > 0 and len(listOfEdges)>0:
	nR = random.randrange(0,len(listOfEdges)) # random number
	
	edge = listOfEdges[nR]
	listOfEdges.pop(nR)
	edgesToDel-=1

	# deleting some of the neighbors of node source and target
	numNeighbors = random.randrange(1,2)

	source = edge.split()[1].split("=")[1].replace('"','')
	target = edge.split()[2].split("=")[1].replace('"','')
	#print source, target	

	for j in range(0,numNeighbors):
		for i in range(len(listOfEdges)):
			if 'source="'+source+'"' in listOfEdges[i] or 'target="'+target+'"' in listOfEdges[i]:
				# neighbor of node source
				if (random.randrange(1,55) > 50):
					# delete neighbor
					listOfEdges.pop(i)
					edgesToDel-=1
					totalNei+=1
					#print "out"
					break


print "Number of edges after deleting  ", len(listOfEdges)
print "Total neighboors deleted  ", totalNei

sInitial = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
sFinal = '</graph>\n</graphml>'
sEdges = ""
for item in listOfEdges:
	sEdges+=item+"\n"

out = open(outputFile,"w")
out.write(sInitial+sNodes+sEdges+sFinal)
out.close()
