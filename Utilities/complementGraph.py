#!/usr/bin python3

# This script creates the complement graph of an input graph
# if the input graph contains multiple dimension
# the scripts creates the complement for each dimension

# Note: As of Jan 2017 only works for one dimension

# TODO: Add support for multiple dimensions

import itertools

file_name = 'numV_c10_50.graphml'
dimension = 'att1'

E = set()  # set of edges in dimension <dimension>
V = set()  # set of vertices in dimension <dimension>

f = open(file_name)
for line in f:
    if dimension in line and '<edge source' in line:
        vertex1 = int(line.split('"')[1])
        vertex2 = int(line.split('"')[3])
        temp = sorted([vertex1,vertex2])
        E.add(tuple(temp))
        V.add(int(vertex1))
        V.add(int(vertex2))
f.close()
if len(E) <=0 or len(V) <=0:
    print("Not a valid dimension.")
    exit(1)
print(E)
print(V)

counter = 0
new_edges = []

for vertex in itertools.combinations(V, 2):
    if vertex in E:
        new_edges.append('<edge source="%s" target="%s" %s="1"/>' % (vertex[0],vertex[1],dimension))
    else:
        new_edges.append('<edge source="%s" target="%s" c_%s="1"/>' % (vertex[0], vertex[1], dimension))
    counter += 1


first_lines = '<?xml version="1.0" encoding="UTF-8"?>\n'\
              '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" ' \
              'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
              'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns ' \
              'http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n' \
              '<graph id="G" edgedefault="undirected">'
nodes_line = ''
for v in V:
    nodes_line += '<node id="%s"/>\n' % v
edges_line = '\n'.join(new_edges)
final_lines = '</graph>\n</graphml>'

f = open('complement_'+file_name,'w')
f.write(first_lines+'\n'+nodes_line+'\n'+edges_line+'\n'+final_lines)
f.close()
# print('\n'.join(new_edges))
# print("\nNumber of edges in dimension-> %s = %s" %(dimension, counter))

