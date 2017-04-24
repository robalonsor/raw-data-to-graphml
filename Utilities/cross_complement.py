#!/usr/bin python3

# This script creates the complement for each graph in graphml format
# then, it creates two property files G1 vs comp_G2 and G2 vs comp_G1, respectively. 
# next, it applies MiMAG to both property files
# next, after MiMAG has finished it merges resutls from both experiments
# the final result is in a *.summary.found file
# For example,
# python bgb_two_att.graphml att2 att34 4 0.5

# will run the complement graph experiment (as described in the paper) considering
# the bgb dataset, the graphs att2 and att34; MiMAG will look for cross-graph quasi-cliques
# of minium size 4 with minium density of 0.5
# April 2017


import itertools
import time  # Only behaves as expected in Linux
import sys
import os
import numpy as np

if len(sys.argv) < 6:
        sys.exit('Usage: %s    input.graphml   edges_graph_1    edges_graph_2     min_size   min_density' % sys.argv[0])

file_name = sys.argv[1]
dimension1 = str(sys.argv[2])
dimension2 = str(sys.argv[3])
n_min = str(sys.argv[4])
min_density = str(sys.argv[5])

def get_data(f_name_d, quality, size, visited_nodes, time, density):
    file_dim1 = open(f_name_d)
    for line in file_dim1:
        if 'graphs' not in line and 'visited' not in line and 'cluster' not in line and \
                        'sum' not in line and 'time' not in line:
            quality.append(float(line.split()[0]))
            size.append(float(line.split()[3]))
            density.append(float(line.split()[-1]))
        else:
            if 'visited' in line:
                visited_nodes += int(line.split()[-1])
            if 'time' in line:
                time += float(line.split()[-1])

    file_dim1.close()
    return quality, size, visited_nodes, time, density

def merge_results(f_name_g1, f_name_g2, file_name):
	output_str = ''
	output_list = []
	quality = []
	size = []
	visited_nodes = 0
	sum_q = 0
	time = 0
	density = []

	quality, size, visited_nodes, time, density = get_data(f_name_g1, quality, size, visited_nodes, time, density)
	quality, size, visited_nodes, time, density = get_data(f_name_g2, quality, size, visited_nodes, time, density)

	output_list.append(round((time/1000),3)) # in seconds
	output_list.append(visited_nodes)
	output_list.append(round(np.mean(quality),3)) if len(quality) > 0 else output_list.append(0)
	output_list.append(np.sum(quality)) if len(quality) > 0 else output_list.append(0)#sum of quality
	output_list.append(len(quality))

	output_list.append(round(np.mean(size),3)) if len(size) > 0 else output_list.append(0)
	output_list.append(round(np.mean(density),3)) if len(density) > 0 else output_list.append(0)
	output_list.append(np.max(size)) if len(size) > 0 else output_list.append(0)   
	output_list.append(np.max(quality)) if len(quality) > 0 else output_list.append(0)

	output_list = map(str, output_list)
	output_str += '\t'.join(output_list)
	output_str += "\n"
	f = open(file_name.split(".")[0]+'.mimag.summary.found',"w")
	f.write(output_str)
	f.write("time\nvisited nodes\navg. quality\nsum of quality\n# patterns found\navg. size\navg. density\nmax. size\nmax. quality")
	f.close()

def construct_graph(file_name):	
	# percentage_to_delete = float(sys.argv[4])
	elapsed_time = time.clock() # Starting timer

	E_dimension1 = set()  # set of edges in dimension 1
	E_dimension2 = set() # set of edges in dimension 2

	V = set()  # set of vertices in the graph

	f = open(file_name)
	first_edge = True
	total_v_to_delete = 0

	for line in f:
	    if '<edge source' in line:
	        vertex1 = int(line.split('"')[1])
	        vertex2 = int(line.split('"')[3])
	        V.add(vertex1) # adding valid vertices
	        V.add(vertex2)
	        temp = sorted([vertex1, vertex2])

	        if vertex1 in V and vertex2 in V:
	            if dimension1 in line:
	                E_dimension1.add(tuple(temp))
	            if dimension2 in line:
	                E_dimension2.add(tuple(temp))

	f.close()
	if len(E_dimension1) <= 0 or len(V) <= 0 or len(E_dimension2) <= 0:
	    print("Not a valid dimension.")
	    exit(0)
	print('New vertices in the graph', len(V))
	V = sorted(list(V))

	counter = 0
	new_edges_d1_comp_d2 = []
	new_edges_d2_comp_d1 = []
	for edge in itertools.combinations(V, 2):
	    if edge in E_dimension1 and edge not in E_dimension2:
	        new_edges_d1_comp_d2.append('<edge source="%s" target="%s" %s="1" c_%s="1"/>' % (edge[0], edge[1], dimension1, dimension2))
	    elif edge in E_dimension2 and edge not in E_dimension1:
	        new_edges_d2_comp_d1.append('<edge source="%s" target="%s" %s="1" c_%s="1"/>' % (edge[0], edge[1], dimension2, dimension1))
	    elif edge in E_dimension1:
	        new_edges_d1_comp_d2.append('<edge source="%s" target="%s" %s="1"/>' % (edge[0], edge[1], dimension1))
	        if edge in E_dimension2:
	        	new_edges_d2_comp_d1.append('<edge source="%s" target="%s" %s="1"/>' % (edge[0], edge[1], dimension2))
	    elif edge in E_dimension2:
	        new_edges_d2_comp_d1.append('<edge source="%s" target="%s" %s="1"/>' % (edge[0], edge[1], dimension2))
	    else:
	        new_edges_d2_comp_d1.append('<edge source="%s" target="%s" c_%s="1"/>' % (edge[0], edge[1], dimension1))
	        new_edges_d1_comp_d2.append('<edge source="%s" target="%s" c_%s="1"/>' % (edge[0], edge[1], dimension2))

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

	file_name = file_name.split(".")[0]
	
	f = open(file_name+"_d1_cd2.graphml", 'w')
	f.write(first_lines+'\n'+nodes_line+'\n'+edges_line_g1+'\n'+final_lines)
	f.close()

	f = open(file_name+"_d2_cd1.graphml", 'w')
	f.write(first_lines+'\n'+nodes_line+'\n'+edges_line_g2+'\n'+final_lines)
	f.close()


	final_time = time.clock()-elapsed_time
	print("Time:  ", final_time) 

	f = open(file_name+".info","a")
	f.write(str("\nTime to cons. complements: %0.2f" % final_time))
	f.close()

	return file_name+"_d1_cd2.graphml", file_name+"_d2_cd1.graphml"

def generate_property_files(file_graph1_comp2, file_graph2_comp1):
	s_init = "graph = %s\nbase_graph = %s\n\n# Cluster model\nn_min = %s\nm_min = 1\ngamma_min = %s\n" % (file_graph1_comp2, file_name, n_min, min_density)
	s_last = "s_min = 2\nw_max = 0.1\n\n# Quality function\na = 1\nb1 = 1\nb2 = 1\n\n# Redundancy model\nr = 0.1\ndelta = 1e-8\nwindow_size = 1e-8\n\n"
	s_last += "# Pruning techniques\npt_similarity = false\npt_diameter = true\npt_indeg_exdeg = true\npt_umse = true\npt_modified_exdeg = true\npt_dimensionality = true\npt_clustering = true\n"
	f = open(file_graph1_comp2.split(".")[0]+".properties","w")
	f.write(s_init+s_last)
	f.close()
	s_init = "graph = %s\nbase_graph = %s\n\n# Cluster model\nn_min = %s\nm_min = 1\ngamma_min = %s\n" % (file_graph2_comp1, file_name, n_min, min_density)
	f = open(file_graph2_comp1.split(".")[0]+".properties", "w")
	f.write(s_init+s_last)
	f.close()
if __name__ == "__main__":
	delete_complement = False
	# First, we generate the complement graphs (G1 vs Comp.G2 and G2 vs Comp. G1)
	file_graph1_comp2, file_graph2_comp1 = construct_graph(file_name)
	# Second, we generate property files
	generate_property_files(file_graph1_comp2, file_graph2_comp1)
	# Third, running MiMAG 
	mimag_sucess = False
	assert os.path.exists("mimag.jar")
	try:
		file_graph1	= file_name.split(".")[0]

		elapsed_time = time.time()
		os.system("java -jar mimag.jar "+file_graph1_comp2.split(".")[0]+".properties mimag")
		if not os.path.exists(file_graph1_comp2.split(".")[0]+".mimag.found"):
			while not os.path.exists(file_graph1_comp2.split(".")[0]+".mimag.found"):
				if time.time() - elapsed_time > 1800: # 30 min
					print("Exceeding 30 min limit. Finishing program without results...")
					raise Exception("Exceeding 30 min limit.")	
		elapsed_time = time.time()
		os.system("java -jar mimag.jar "+file_graph2_comp1.split(".")[0]+".properties mimag")
		if not os.path.exists(file_graph2_comp1+".mimag.found"):
			while not os.path.exists(file_graph2_comp1.split(".")[0]+".mimag.found"):
				if time.time() - elapsed_time > 1800: # 30 min
					print("Exceeding 30 min limit. Finishing program without results...")
					raise Exception("Exceeding 30 min limit.")	
		mimag_sucess = True
	except Exception as e:
		raise
	finally:
		# Deleting temporal files
		os.remove(file_graph1_comp2.split(".")[0]+".properties")
		os.remove(file_graph2_comp1.split(".")[0]+".properties")
		os.remove(file_graph1_comp2)
		os.remove(file_graph2_comp1)
	if not mimag_sucess:
		exit()
	# Fourth, merging results from both experiments
	
	merge_results(file_graph1_comp2.split(".")[0]+".mimag.found", file_graph2_comp1.split(".")[0]+".mimag.found", file_name)
	# os.remove("exp1.found")
	# os.remove("exp2.found")
	print("End of MiMAG Complement Graph experiment...")
