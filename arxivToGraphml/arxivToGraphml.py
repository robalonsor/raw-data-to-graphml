#!/usr/bin/python    
import ConfigParser
import sys,os
import spacy

from sets import Set

def abstrctFromFile(fName,path,listOfPapers,listOfTitles):
	f = open(path+"/"+fName)
	flagTitle = 0
	flagAbstract = 0
	abstract = ""
	#listOfPapers.append(fName.rstrip(".abs")) #storing keys 
	for line in f:
		line = line.rstrip("\n")
		if flagAbstract and '\\\\' in line:
			flagAbstract = 0
			flagTitle = 0
		if flagAbstract:
			abstract+=line+" "

		if "Title:" in line:
			flagTitle = 1
			listOfTitles.append([fName.rstrip(".abs"),line.lstrip("Title: ")])
			listOfPapers.append(fName.rstrip(".abs"))

		if flagTitle and '\\\\' in line:
			flagAbstract = 1

	#print abstract
	#print listOfTitles
	f.close()

	

	return abstract
config = ConfigParser.RawConfigParser()
configFile = "ConfigFile.properties"
config.read(configFile)


#print config.get('DatabaseSection', 'database.dbname');
sys.stderr.write(str("Collecting years from properties file"))

collectionOfYears = []
for y in config.items('YearsSection'):
	collectionOfYears.append(y[1])


fCitations = config.get('FilesSection','citations')
fDates = config.get('FilesSection','dates')

listOfPapers = []
listOfAbstracts = []
listOfTitles = []
for y in collectionOfYears:
	#print y
	for file in os.listdir(y):
	    if file.endswith(".abs"):
	    	#listOfPapers.append(file.rstrip(".abs")) #storing keys 
	    	listOfAbstracts.append(abstrctFromFile(file,y,listOfPapers,listOfTitles))
	    	
#Storing dictionary for later use in MiSPa output to graph
f = open("dictionary_"+configFile.rstrip(".properties")+".txt","w")
paperIndex = 0
for item in listOfTitles:
	f.write(str(paperIndex)+","+item[0]+"-"+item[1]+"\n")
	paperIndex+=1

f.close()

sys.stderr.write(str("\nComputing similarities\n"))
#Computing similarity
en_nlp = spacy.load('en')

list_of_nlp_abs = [en_nlp(abst.decode('utf8')) for abst in listOfAbstracts]

#print listOfAbstracts[0]
#print listOfAbstracts[1]
#print(list_of_nlp_doc[0].similarity(list_of_nlp_doc[1]))

#Adding edges according to treshold
treshold = 0.99
edgesG2 = Set()
#
similarities = []
total = 0
for i in range(0,len(listOfAbstracts)):
	for j in range(i,len(listOfAbstracts)):
		if i == j:
			continue
		sim = list_of_nlp_abs[i].similarity(list_of_nlp_abs[j])
		if sim >= treshold:
			#similarities.append(list_of_nlp_abs[i].similarity(list_of_nlp_abs[j]))
			edgesG2.add((i,j))
			#print "document ",i, "similar to ", j
			total+=1
#print "Total similarity edges... ",total
#for i in similarities:
#	print i

#
#Determining citations, and constructing citation graph


sys.stderr.write(str("Collecting citations for years " + str(collectionOfYears) + "\n"))

setOfPapers = Set(listOfPapers)
edgesG1 = Set()   #dimension 1 = citations

#print setOfPapers
_fileCitations = open(fCitations)
for cite in _fileCitations:
	cite = cite.rstrip("\n")
	
	if cite.split()[0] in setOfPapers and cite.split()[1] in setOfPapers:
		#print cite.split()[0], cite.split()[1]
		edge = (listOfPapers.index(cite.split()[0]),listOfPapers.index(cite.split()[1]))
		edgeInv =(listOfPapers.index(cite.split()[1]),listOfPapers.index(cite.split()[0]))
		if edge not in edgesG1 and edgeInv not in edgesG1:
			#edgesG1.add(edge)
			edgesG1.add(edge)

#print edgesG1

# print edgesG1
sys.stderr.write(str("Constructing graph\n"))

sFirst = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edgedefault="undirected">\n'
sFinal= '</graph>\n</graphml>'
sEdges = "" # edges
sNodes = ""  # sring fro graphml nodes
#Now adding papers (ie nodes) to the graph
for i in range(len(listOfPapers)):
	sNodes+='<node id="'+str(i)+'"/>\n'


intersectionEdges = Set() # citations and similarity

for e in edgesG1:
	if e in edgesG2:
		intersectionEdges.add(e)
		#print "Some intersaction!!" , e

for e in intersectionEdges:
	edgesG1.remove(e)
	edgesG2.remove(e)
	#print "Removing ", e


#for i in range(len(edgesG1)):
while len(edgesG1) > 0:
	#sEdges+='<edge source="'+str(edgesG1[i][0])+'" target="'+str(edgesG1[i][1])+'" citation="10"/>\n'
	e = edgesG1.pop()
	if e[0] != e[1]:
		sEdges+='<edge source="'+str(e[0])+'" target="'+str(e[1])+'" citation="10"/>\n'

while len(edgesG2) > 0:
#for i in range(len(edgesG2)):
	e = edgesG2.pop()
	if e[0] != e[1]:
		sEdges+='<edge source="'+str(e[0])+'" target="'+str(e[1])+'" similar="20"/>\n'
while len(intersectionEdges) > 0:
#for i in range(len(intersectionEdges)):
	e = intersectionEdges.pop()
	if e[0] != e[1]:
		sEdges+='<edge source="'+str(e[0])+'" target="'+str(e[1])+'" citation="10" similar="20"/>\n'

sys.stderr.write("Writing to file...\n")

f = open("Arxiv"+collectionOfYears[0]+"_4morey.graphml","w")
f.write(sFirst+sNodes+sEdges+sFinal)
f.close()

sys.stderr.write("End.")
