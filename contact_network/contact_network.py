#!/usr/bin python3
sInitial = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
sFinal = '</graph>\n</graphml>'
sNodes = ""
s = ''

f_name = 'datasets/Facebook-known-pairs_data_2013.csv'
target_w = '1'

f = open(f_name)
edges_graph1 = []
for line in f:
	data = line.split()
	if data[2] == '0':
		continue
	edge = [data[0],data[1]]
	edge.sort()
	edges_graph1.append(edge)
f.close()

f_name = 'datasets/Friendship-network_data_2013.csv'
f = open(f_name)
edges_graph2 = []
for line in f:
	data = line.split()
	edge = [data[0],data[1]]
	edge.sort()
	edges_graph2.append(data)
f.close()
nodes = set()
for i in range(len(edges_graph1)):
		s+='<edge source="'+str(edges_graph1[i][0])+'" target="'+str(edges_graph1[i][1])+'" '
		s+='facebook="1" '
		if edges_graph1[i] in edges_graph2:
			s+='friends="1" '
			edges_graph2.pop(edges_graph2.index(edges_graph1[i]))
		s+='/>\n'
		nodes.add(edges_graph1[i][0])
		nodes.add(edges_graph1[i][1])

for i in range(len(edges_graph2)):
	s+='<edge source="'+str(edges_graph2[i][0])+'" target="'+str(edges_graph2[i][1])+'" '
	s+='friends="1" '
	s+='/>\n'
	
	nodes.add(edges_graph2[i][0])
	nodes.add(edges_graph2[i][1])

for i in range(0,len(nodes)):
		sNodes+='<node id="'+str(i)+'"/>\n'

f = open('contact_face_vs_friend.graphml','w')
f.write(sInitial+sNodes+s+sFinal)
f.close()
