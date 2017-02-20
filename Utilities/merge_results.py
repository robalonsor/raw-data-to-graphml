#!/usr/bin python3

# Delete after use


import numpy as np


def get_data(f_name_d):
    global quality
    global size
    global visited_nodes
    global time
    file_dim1 = open(f_name_d)
    for line in file_dim1:
        if 'dimensions' not in line and 'visited' not in line and 'cluster' not in line and \
                        'sum' not in line and 'time' not in line:
            quality.append(float(line.split()[0]))
            size.append(float(line.split()[3]))
        else:
            if 'visited' in line:
                visited_nodes += int(line.split()[-1])
            if 'time' in line:
                time += int(line.split()[-1])

    file_dim1.close()

def get_structural_data(info):
    f = open(info)
    counter = 0
    nodes = ''
    edges_dim1 = ''
    edges_dim2 = ''
    for line in f:
        if counter >=4:
            break
        if 'Nodes' in line:
            nodes = line.split()[2]
        if 'Dimension 1' in line:
            edges_dim1 = line.split()[5]
        elif 'Dimension 2' in line:
            edges_dim2 = line.split()[5]
        counter += 1
        print(line)
    f.close()
    if nodes == '' or edges_dim1 == '' or edges_dim2 == '':
        print("Erorr trying to get structural prop. of the graph")
        exit()

    return nodes, edges_dim1, edges_dim2
for params in ['g5_n4', 'g5_n8', 'g7_n4', 'g7_n8']:
    output_str = ''
    for num_clusters in range(10, 600, 25):
        output_list = []
        quality = [0]
        size = [0]
        visited_nodes = 0
        sum_q = 0
        time = 0

        f_name_d1 = "V_c"+str(num_clusters)+"_"+params+"_d1_cd2.mimag.found"
        f_name_d2 = "V_c"+str(num_clusters)+"_"+params+"_d2_cd1.mimag.found"

        get_data(f_name_d1)
        get_data(f_name_d2)
        #
        n, e1, e2 = get_structural_data("V_c"+str(num_clusters)+".info")
        #
        # storing resutls for parameters <params>
        output_list.append(num_clusters)
        #
        output_list.append(n)
        output_list.append(e1)
        output_list.append(e2)
        #
        output_list.append(visited_nodes)
        #output_list.append(np.min(size))
        output_list.append(round(np.mean(size),3))
        output_list.append(np.max(size))
        #output_list.append(np.min(quality))
        output_list.append(round(np.mean(quality),3))
        output_list.append(np.max(quality))
        output_list.append(np.sum(quality)) #sum of quality
        output_list.append(time/1000) # in seconds
        output_list.append(len(quality)-1)
        output_list = map(str, output_list)
        output_str += ' '.join(output_list)
        output_str += "\n"
    f = open("Syn_comp_"+params+'.txt',"w")
    f.write(output_str)
    f.close()
print("Done!")
#print(max(quality), max(size), round(np.sum(quality), 3), time, visited_nodes)
