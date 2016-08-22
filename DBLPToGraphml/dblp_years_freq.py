# Given a set of conferences in dblp-format, construct a graph
# G1 according to the years given in the list yearGraph1
# a second graph G2 is constructed in the same way except that
# it considers the years in the list yearGraph2
# Lastly, a variable 'frequency' should be given to filter collaborations
# in terms of this variable. So, if two authors collaborate 
# at least 'frequency' times in the years 'yearGraph1' in 'conferences'
# an edge is drawn.

import tempfile
import os
import sys
from operator import itemgetter

if len(sys.argv) < 3:
    sys.exit('Usage: %s    dblp-file    output_file_name' % sys.argv[0])

fDBLP = sys.argv[1]
fOut = sys.argv[2]

_file = open(fDBLP)

conferences = ["conf/kdd/","conf/icdm/", "conf/vldb/","conf/icml/","conf/www/","conf/pakdd/"]
yearGraph1 = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007"]
yearGraph2 = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]
frequency = 2

sG1 = ""
sG2 = ""
flag = 0
authors = []
s = ""
for line in _file:
    if flag and ('<author>' in line or '<year>' in line):
        s += line

    if '<inproceedings' in line or '<proceedings' in line:
        flag = 1
        s += line
    if ('</inproceedings' in line or '</proceedings' in line) and flag:
        flag = 0
        s += line
        f = 0
        # print s
        for c in conferences:
            if c in s:
                f = 1
        if f == 0:
            s = ""
            continue
        f = 0

        for y in yearGraph1:
            if '<year>' + y in s:
                f = 1
                break
        if f == 1:  # ie this year is in the string
            sG1 += s
            s = ""
            continue
        f = 0
        for y in yearGraph2:
            if '<year>' + y in s:
                f = 1
                break
        if f == 1:
            sG2 += s
            s = ""
            continue
        # exit()
        s = ""

_file.close()

f1 = open("test1.txt", "w")
f2 = open("test2.txt", "w")

f1.write(sG1)
f2.write(sG2)
f1.close()
f2.close()

fileGraph1 = open("test1.txt")
s = ""
flag = 0
edgesG1 = []
authorsG1 = []

for line in fileGraph1:
    if '<inproceedings' in line or '<proceedings' in line:
        flag = 1
        authorsG1 = []
    if '<author>' in line:
        auth = line.replace('<author>', "").replace('</author>', "")
        if auth not in authors:
            authors.append(auth)
        if auth not in authorsG1:
            authorsG1.append(auth)
    if ('</inproceedings' in line or '</proceedings' in line) and flag == 1:
        flag = 0
        l = list(authorsG1)

        for i in range(0, len(l)):
            for j in range(i + 1, len(l)):
                edge = [l[i], l[j]]
                if l[i] == l[j]:
                    print "error", l[i], l[j]
                    exit()
                if edge not in edgesG1 or [l[j], l[i]] not in edgesG1:
                    edgesG1.append(edge)
fileGraph1.close()
os.remove("test1.txt")
##

fileGraph2 = open("test2.txt")
s = ""
flag = 0
edgesG2 = []
authorsG2 = []

for line in fileGraph2:
    if '<inproceedings' in line or '<proceedings' in line:
        flag = 1
        authorsG2 = []
    if '<author>' in line:
        auth = line.replace('<author>', "").replace('</author>', "")
        if auth not in authors:
            authors.append(auth)
        if auth not in authorsG2:
            authorsG2.append(auth)
    if ('</inproceedings' in line or '</proceedings' in line) and flag == 1:
        flag = 0
        l = list(authorsG2)

        for i in range(0, len(l)):
            for j in range(i + 1, len(l)):
                edge = [l[i], l[j]]
                if l[i] == l[j]:
                    print "error", l[i], l[j]
                    exit()
                # print# edge
                if edge not in edgesG2 or [l[j], l[i]] not in edgesG2:
                    edgesG2.append(edge)

fileGraph2.close()
os.remove("test2.txt")

i = 0
while i < len(edgesG1):
    edgeFreq = 1
    j = i+1
    for j in range(i+1, len(edgesG1)):
        if edgeFreq >= frequency:
            break
        if edgesG1[i] == edgesG1[j]:
            edgeFreq += 1
    if edgeFreq < frequency:
        # delete all frequencies of the edge since
        # it is not as frequent as expected
        toDelete = edgesG1.pop(i)
        i -= 1
        # now deleting occurrences in other parts of list
        j = i+1
        while j < len(edgesG1):
            if toDelete == edgesG1[j]:
                edgesG1.pop(j)
                j -= 1
            j += 1
    i += 1

print len(edgesG2)
i = 0
while i < len(edgesG2):
    edgeFreq = 1
    j = i+1
    for j in range(i+1, len(edgesG2)):
        if edgeFreq >= frequency:
            break
        if edgesG2[i] == edgesG2[j]:
            edgeFreq += 1
    if edgeFreq < frequency:
        # delete all frequencies of the edge since
        # it is not as frequent as expected
        toDelete = edgesG2.pop(i)
        i -= 1
        # now deleting occurrences in other parts of list
        j = i+1
        while j < len(edgesG2):
            if toDelete == edgesG2[j]:
                edgesG2.pop(j)
                j -= 1
            j += 1
    i += 1
print len(edgesG2)
# TODO :Delete exit
# exit()

nodeList = []
edgeListG1 = []
edgeListG2 = []

s = ""
j = 0
for i in authors:
    if i not in nodeList:
        nodeList.append(i)
        s += str(j) + "," + i
        j += 1

f = open("dictionary" + fOut + ".txt", "w")
f.write(s)
f.close()
##
for e in edgesG1:
    u = nodeList.index(e[0])
    v = nodeList.index(e[1])
    if u < v:
        if [u, v] not in edgeListG1:
            edgeListG1.append([u, v])
    if v < u:
        if [v, u] not in edgeListG1:
            edgeListG1.append([v, u])
    if u == v:
        print "Error", e[0], e[1]
        exit()

for e in edgesG2:
    u = nodeList.index(e[0])
    v = nodeList.index(e[1])
    if u < v:
        if [u, v] not in edgeListG2:
            edgeListG2.append([u, v])
    if v < u:
        if [v, u] not in edgeListG2:
            edgeListG2.append([v, u])
    if u == v:
        print "Error", e[0], e[1]
        exit()

intersectionEdges = []  # collaborations in both conferences

for e in edgeListG1:
    if e in edgeListG2:
        intersectionEdges.append(e)

for e in intersectionEdges:
    edgeListG1.remove(e)
    edgeListG2.remove(e)

##

s = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
for i in range(len(nodeList)):
    s += '<node id="' + str(i) + '"/>\n'

for i in range(len(edgeListG1)):
    s += '<edge source="' + str(edgeListG1[i][0]) + '" target="' + str(edgeListG1[i][1]) + '" g1="10"/>\n'

for i in range(len(edgeListG2)):
    s += '<edge source="' + str(edgeListG2[i][0]) + '" target="' + str(edgeListG2[i][1]) + '" g2="20"/>\n'
for i in range(len(intersectionEdges)):
    s += '<edge source="' + str(intersectionEdges[i][0]) + '" target="' + str(
        intersectionEdges[i][1]) + '" g1="10" g2="20"/>\n'

s += '</graph>\n</graphml>'

f = open(fOut + ".graphml", "w")
f.write(s)
f.close()
