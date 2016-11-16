# this script transforms the original eopinions dataset to 
# a graphml format
# First, consider the format of eopinions
# 1 2 -1 979081200
# first number is node ID of a user
# second number is node ID  (both nodes ID correspond to an edge)
# the third value is the trust(+1) or distrust (-1)
# the forth value is the timestamp
import sys

def deleteOcurrences(target,listOf):
	indices = []

	target1 = [target[0],target[1]]
	target2 = [target[1],target[0]]
	flag = 1
	i=0
	while flag==1 and i < len(listOf):
		#print len(listOf)
		#print i
		#print "-"
		if target1 == listOf[i] or target2 == listOf[i]:
			listOf.pop(i)
			i-=1
		i+=1
		if i >= len(listOf):
			flag=0
	
	return 0


def findOcurrences(target,listOf,returnIndex=0):
	indices = []

	target1 = [target[0],target[1]]
	target2 = [target[1],target[0]]


	# print"--"
	# print target1
	# print target2
	# print "=="
	for i in range(0,len(listOf)):
		if target1 == listOf[i]:
			if returnIndex:
				indices.append(i)
		if target2 == listOf[i]:
			if returnIndex:
				indices.append(i)

	for i in indices:
		listOf[i] = -1
	return indices

if len(sys.argv) < 3:
        sys.exit('Usage: %s    input.epinions    output.graphml' % sys.argv[0])

fEpinions = sys.argv[1]
fOut = sys.argv[2]

f = open(fEpinions)
sInitial = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
sFinal = '</graph>\n</graphml>'

from sets import Set
tstamp = {}
nodes = set()
edges = []
globalEdges = []
timestamps = []
typeEdges = []

for line in f:

	if not line.split()[3] in tstamp:
		tstamp[line.split()[3]] = 1
	else:
		tstamp[line.split()[3]] += 1
	data = line.split()
	node1 = data[0]
	node2 = data[1]
	

	if node1 == node2: # deleting the loops
		continue
	edge = [node1,node2]
	typeEdges.append(data[2])
	edges.append(edge)
	timestamps.append(line.split()[3])
	if node1 == "98305" or node2 == "98305":
		print "Found", edge

	nodes.add(node1)
	nodes.add(node2)
	#if not node1 in nodes:
	#	nodes.append(node1)
	#if not node2 in nodes:
	#	nodes.append(node2)
f.close()

nodes = list(nodes)
globalEdges = list(edges)


# second, att1= positive trust in some period of time   att2 = positive trust wrt to the rest of time

#third att1 = positive trust in some period of time att2 = negative trust wrt to all the time (incluidng the one form att1)

#fourht att1 = negattive trust in some period of time att2 = positive trust wrt to some period of time

#fourht att1 = negattive trust in some period of time att2 = positive trust wrt to all the time (incluid the one from att1)

#fifth att1= negative trust in some period of time att2 = positive trust wrt to some period of time

#sixth att1= positive trust in some period of time att2 = positive trust wrt to a set of timestamps


s = ""

# setTimestamp1 = 979081200 
# setTimestamp2 = 991346400

setTimestamp1 = 980987708 # feb-01-2001  
setTimestamp2 = 988675148 # apr-30-2001
tmG2_1 = 988675208 # may-01-2001
#tmG2_2 = 996623948 # jul-31-2001
tmG2_2 = 1009843200 # jan-01-2002 00:00:00.00 hrs

# tmG2_1 = 991432800
# tmG2_2 = 1009753200
setEdgesG1 = set()
setEdgesG2 = set()

for i in range(len(timestamps)):

	# if timestamps[i] in setTimestamp1 and typeEdges[i] == "1": # if the timestamp is for graph 1
	# 	setEdgesG1.append(edges[i])
	# if timestamps[i] in setTimestamp2 and typeEdges[i] == "1":
	# 	setEdgesG2.append(edges[i])
	#print timestamps[i], setEdgesG1

	if int(timestamps[i]) >= setTimestamp1 and int(timestamps[i])<= setTimestamp2 and typeEdges[i] == "1": # if the timestamp is for graph 1
		# setEdgesG1.append(edges[i])
		setEdgesG1.add((edges[i][0],edges[i][1]))
		if edges[i][0] == "98305" or  edges[i][1] == "98305":
			print edges[i][0],  "98305"
			print edges[i][1],  "98305"
			print edges[i]

		continue
		#print "adasd"
	if int(timestamps[i]) >= tmG2_1 and int(timestamps[i])<= tmG2_2 and typeEdges[i] == "-1": # if the timestamp is for graph 2
		# setEdgesG2.append(edges[i])
		setEdgesG2.add((edges[i][0],edges[i][1]))

	#if timestamps[i] in setTimestamp2 and typeEdges[i] == "1":
	#	setEdgesG2.append(edges[i])

print len(setEdgesG1)
print len(setEdgesG2)

#exit()
nodes = set()

while len(setEdgesG1) >0:
	e = setEdgesG1.pop()
	# print "->",e
	# print setEdgesG2
	# print "-"
	if e[0] == "98305" or e[1] == "98305":
		print " ----- "
		print "XXXX"
		print e
	nodes.add(e[0])
	nodes.add(e[1])
	s+='<edge source="'+e[0]+'" target="'+e[1]+'" '
	s+='g1="10" '
	posFlag = 0
	negFlag = 0

	if (e[0],e[1]) in setEdgesG2 or (e[1],e[0]) in setEdgesG2:
		s+='g2="20"'
		setEdgesG2.discard((e[0],e[1]))
		setEdgesG2.discard((e[1],e[0]))
	s+='/>\n'	
	pass

# for i in range(len(setEdgesG2)):
for item in setEdgesG2:
	
	s+='<edge source="'+item[0]+'" target="'+item[1]+'" '
	s+='g2="20" '
	s+='/>\n'
	nodes.add(item[0])
	nodes.add(item[1])
	# print setEdgesG2[i][0],setEdgesG2[i][1]
	# findOcurrences(setEdgesG2[i],setEdgesG2,1)

#print s
nodes = list(nodes)
sNodes = ""
#for i in range(0,len(nodes)):
for i in nodes:
	sNodes+='<node id="'+str(i)+'"/>\n'
	

#f = open("dataSetsEopinions/eopinions_PosToPos_t1_t2.graphml","w")
f = open(fOut+".graphml","w")

f.write(sInitial+sNodes+s+sFinal)
f.close()
#print edges

#import operator

#sorted_tstamp = sorted(tstamp.items(), key=operator.itemgetter(1))
#print sorted_tstamp	
