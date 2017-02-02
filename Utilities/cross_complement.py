#!/usr/bin python3

# This script deletes random vertices from a graphml file
# along with the associated edges
# then it create the complement for each dimension
# then it creates two files 1) file containing a graph with G1 and G'2
# and 2) file containing a graph with G2 and G'1
# February 2017

import itertools

file_name = input('Name of input file: ')
percentage_to_delete = float(input('Percentage to delete (0.9-0.1): '))
dimension1 = input('Name of dimension 1: ')
dimension2 = input('Name of dimension 2: ')

E_dimension1 = set()  # set of edges in dimension 1
E_dimension2 = set() # set of edges in dimension 2

V = set()  # set of vertices in the graph

f = open(file_name)
first_edge = True
total_v_to_delete = 0

for line in f:
    if 'node id=' in line:
        V.add(int(line.split('"')[1]))
        continue

    if '<edge source' in line:
        if first_edge:
            # Deleting random vertices to filter associated edges
            print("Originaly the graph had: %s ", len(V))
            first_edge = False
            total_v_to_delete = int(len(V)*percentage_to_delete)
            for i in range(total_v_to_delete):
                V.pop()
        vertex1 = int(line.split('"')[1])
        vertex2 = int(line.split('"')[3])
        temp = sorted([vertex1, vertex2])
        if vertex1 in V and vertex2 in V:
            if dimension1 in line:
                E_dimension1.add(tuple(temp))
            if dimension2 in line:
                E_dimension2.add(tuple(temp))

        # V.add(int(vertex1))
        # V.add(int(vertex2))

f.close()
if len(E_dimension1) <=0 or len(V) <=0 or len(E_dimension2) <= 0:
    print("Not a valid dimension.")
    exit(0)
# print(E)
print('New vertices in the graph', len(V))

counter = 0
new_edges_d1_comp_d2 = []
new_edges_d2_comp_d1 = []
for edge in itertools.combinations(V, 2):
    if edge in E_dimension1 and edge not in E_dimension2:
        new_edges_d1_comp_d2.append('<edge source="%s" target="%s" %s="1" c_%s="2"/>' % (edge[0], edge[1], dimension1, dimension2))
    elif edge in E_dimension2 and edge not in E_dimension1:
        new_edges_d2_comp_d1.append('<edge source="%s" target="%s" %s="2" c_%s="1"/>' % (edge[0], edge[1], dimension2, dimension1))
    else:
        if edge in E_dimension1:
            new_edges_d1_comp_d2.append('<edge source="%s" target="%s" %s="1"/>' % (edge[0], edge[1], dimension1))
        if edge in E_dimension2:
            new_edges_d2_comp_d1.append('<edge source="%s" target="%s" %s="1"/>' % (edge[0], edge[1], dimension2))
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

edges_line_g1 = '\n'.join(new_edges_d1_comp_d2)
edges_line_g2 = '\n'.join(new_edges_d2_comp_d1)
final_lines = '</graph>\n</graphml>'

f = open('comp_d1_comp_d2'+file_name, 'w')
f.write(first_lines+'\n'+nodes_line+'\n'+edges_line_g1+'\n'+final_lines)
f.close()

f = open('comp_d2_comp_d1'+file_name, 'w')
f.write(first_lines+'\n'+nodes_line+'\n'+edges_line_g2+'\n'+final_lines)
f.close()
# print('\n'.join(new_edges))
# print("\nNumber of edges in dimension-> %s = %s" %(dimension, counter))

