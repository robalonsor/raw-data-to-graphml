# this script transforms the original eopinions dataset to 
# a graphml format
# First, consider the format of eopinions
# 1 2 -1 979081200
# first number is node ID
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

	nodes.add(node1)
	nodes.add(node2)
	#if not node1 in nodes:
	#	nodes.append(node1)
	#if not node2 in nodes:
	#	nodes.append(node2)
f.close()

#print "x"
#exit()
nodes = list(nodes)

globalEdges = list(edges)

#print "x"
sNodes = ""
for i in range(0,len(nodes)):
	sNodes+='<node id="'+str(i)+'"/>\n'

# first, att1 = positive trust  att2 = negative trust. 
# s=""
# for i in range(0,len(typeEdges)):
# 	if edges[i] == -1:
# 		#print "position ", i, "no longer valid"
# 		continue
# 	s+='<edge source="'+edges[i][0]+'" target="'+edges[i][1]+'" '
# 	#print edges[i]
# 	indices = findOcurrences(edges[i],edges,1)
# 	#print indices
# 	#print edges

# 	posFlag = 0
# 	negFlag = 0

# 	for index in indices:
# 		if typeEdges[index] == "1" and not posFlag:
# 			s+='att1=10 '
# 			posFlag = 1
# 		if typeEdges[index] == "-1" and not negFlag:
# 			s+='att2=20 '
# 			negFlag = 1

# 	s+='/>\n'
# 	#print s
# 	#exit()

# f.close()

# f = open("dataSetsEopinions/eopinions_PosToNeg.graphml","w")
# f.write(sInitial+sNodes+s+sFinal)
# f.close()
# print edges



# second, att1= positive trust in some period of time   att2 = positive trust wrt to the rest of time

#third att1 = positive trust in some period of time att2 = negative trust wrt to all the time (incluidng the one form att1)

#fourht att1 = negattive trust in some period of time att2 = positive trust wrt to some period of time

#fourht att1 = negattive trust in some period of time att2 = positive trust wrt to all the time (incluid the one from att1)

#fifth att1= negative trust in some period of time att2 = positive trust wrt to some period of time

#sixth att1= positive trust in some period of time att2 = positive trust wrt to a set of timestamps


s = ""
#setTimestampG1 = ["979081200"] # set of timestamps to construct graph 1
#setTimestampG1 = ["982623600","984092400","984178800","1006297200","1003701600"] # set of timestamps to construct graph 1
#setTimestampG2 = ["1060639200","1044745200","1028930400","1021327200","1021240800"] # set of timestamps to construct graph 2
setTimestampG1 = 982623600
setTimestampG2 = 987638400

tm = 987724800
tm2 = 992995200
setEdgesG1 = []
setEdgesG2 = []

for i in range(len(timestamps)):

	# if timestamps[i] in setTimestampG1 and typeEdges[i] == "1": # if the timestamp is for graph 1
	# 	setEdgesG1.append(edges[i])
	# if timestamps[i] in setTimestampG2 and typeEdges[i] == "1":
	# 	setEdgesG2.append(edges[i])
	#print timestamps[i], setEdgesG1

	if int(timestamps[i]) >= setTimestampG1 and int(timestamps[i])<= setTimestampG2 and typeEdges[i] == "1": # if the timestamp is for graph 1
		setEdgesG1.append(edges[i])
		#print "adasd"
	if int(timestamps[i]) >= tm and int(timestamps[i])<= tm2 and typeEdges[i] == "1": # if the timestamp is for graph 1
		setEdgesG2.append(edges[i])
	#if timestamps[i] in setTimestampG2 and typeEdges[i] == "1":
	#	setEdgesG2.append(edges[i])

print len(setEdgesG1)
print len(setEdgesG2)
#exit()

nodes = set()

while len(setEdgesG1) >0:
	e = setEdgesG1.pop()
	# print "->",e
	# #print setEdgesG2
	# print "-"
	nodes.add(e[0])
	nodes.add(e[1])
	s+='<edge source="'+e[0]+'" target="'+e[1]+'" '
	s+='g1="10" '
	posFlag = 0
	negFlag = 0

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
		else:
			if [e[1],e[0]] == setEdgesG2[j]:
				# print [e[1],e[0]],"/"
				if posFlag == 0:
					s+='g2="20" '
					posFlag = 1
				setEdgesG2.pop(j)
				j-=1

		j+=1
		if j >= len(setEdgesG2):
			flagExit=1
	
	s+='/>\n'
	deleteOcurrences(e,setEdgesG1)
	# print setEdgesG2
	# print "-end"
	#exit()
	pass

# for i in range(len(setEdgesG1)):
# 	if setEdgesG1[i] == -1:
# 		#print "position ", i, "no longer valid"
# 		continue
# 	s+='<edge source="'+setEdgesG1[i][0]+'" target="'+setEdgesG1[i][1]+'" '
# 	s+='g1=10 '
# 	posFlag = 0
# 	negFlag = 0

# 	for j in range(len(setEdgesG2)):
# 		if setEdgesG2[j] == -1:
# 			continue
# 		if [setEdgesG1[i][0],setEdgesG1[i][1]] == setEdgesG2[j]:
# 			if not posFlag:
# 				s+='g2=20 '
# 				posFlag = 1
# 			setEdgesG2[j] = -1

# 		if [setEdgesG1[i][1],setEdgesG1[i][0]] == setEdgesG2[j]:
# 			if not negFlag:
# 				s+='g2=20 '
# 				negFlag = 1
# 			setEdgesG2[j] = -1
	
# 	s+='/>\n'
# 	findOcurrences(setEdgesG1[i],setEdgesG1)

# appending remaning edges

#print "inserting remaning edges"

for i in range(len(setEdgesG2)):
	if setEdgesG2[i] == -1:
		continue
	s+='<edge source="'+setEdgesG2[i][0]+'" target="'+setEdgesG2[i][1]+'" '
	s+='g2="20" '
	s+='/>\n'
	nodes.add(setEdgesG2[i][0])
	nodes.add(setEdgesG2[i][1])
	# print setEdgesG2[i][0],setEdgesG2[i][1]
	findOcurrences(setEdgesG2[i],setEdgesG2,1)

#print s
nodes = list(nodes)
sNodes = ""
for i in range(0,len(nodes)):
	sNodes+='<node id="'+str(i)+'"/>\n'
	

#f = open("dataSetsEopinions/eopinions_PosToPos_t1_t2.graphml","w")
f = open("dataSetsEopinions/"+fOut+".graphml","w")

f.write(sInitial+sNodes+s+sFinal)
f.close()
#print edges

#import operator

#sorted_tstamp = sorted(tstamp.items(), key=operator.itemgetter(1))
#print sorted_tstamp	
