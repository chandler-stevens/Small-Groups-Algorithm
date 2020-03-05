#from os import system

#system("pip install -r .\Requirements.txt")

# Python Standard Library
from collections import OrderedDict
from copy import deepcopy

# Requirements
from networkx import nx
import matplotlib.pyplot as plt
from matplotlib import pylab

#filename = input("Please enter the filename: ")
#fin = open(filename)
fin = open("group1.txt")

peopleNumbers = OrderedDict()
peopleUnvisited = OrderedDict()
n = 0

#m = int(input("Please enter the ideal group size: "))

m = 4

G = nx.DiGraph()
labels = {}
nodeIndex = 0

for line in fin:
    if "," in line:
        commaIndex = line.index(",")
        nameCouple = line[:commaIndex] + " + " + line[commaIndex + 1:-1]
        peopleNumbers[nameCouple] = 2
        peopleUnvisited[nameCouple] = []
        # Place couples at beginning
        peopleNumbers.move_to_end(nameCouple, False)
        G.add_node(nameCouple)
        labels[nodeIndex] = nameCouple
        n += 2
    else:
        nameSingle = line[:-1]
        peopleNumbers[nameSingle] = 1
        peopleUnvisited[nameSingle] = []
        G.add_node(nameSingle)
        labels[nodeIndex] = nameSingle
        n += 1
    nodeIndex += 1

for persons in peopleNumbers:
    for person in peopleNumbers:
        if persons != person:
            peopleUnvisited[persons].append(person)

pos = nx.circular_layout(G)
pylab.show()
fig = pylab.figure()

def animate_edge(host, guest):
    fig.clear()
    G.add_edge(host, guest)
    nx.draw_circular(G, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(host, guest)],
                           edge_color='g', width=5,
                           node_color=range(24), cmap=plt.cm.Blues)
    print(G.number_of_edges())
    fig.canvas.draw()
    pylab.draw()
    #plt.pause(0.1)

numGroups = n // m

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

superList = []

hostNames = []
for i in range(numGroups):
    hostNames.append("")

nightNum = 0
while len(sum(list(peopleUnvisited.values()), [])) > 0:
    people = deepcopy(peopleUnvisited)
    night = [[]]
    guestQueue = []
    
    for i in range(numGroups):
        group = []
        host = max(people, key=lambda k: people[k])
        previousHosts = []
        while host in hostNames:
            previousHosts.append(host)
            del people[host]
            host = max(people, key=lambda k: people[k])
        del people[host]
        group.append(host)
        night[0].append(peopleNumbers[host])
        hostNames[i] = host

        for prevHost in previousHosts:
            people[prevHost] = []
        
        guestToAdd = ""
        for guest in guestQueue:
            if peopleNumbers[guest] + night[0][i] <= m:
                guestToAdd = guest
                break
                
        if guestToAdd != "":
            group.append(guestToAdd)
            animate_edge(host, guestToAdd)
            night[0][i] += peopleNumbers[guestToAdd]
            if guestToAdd in peopleUnvisited[host]:
                peopleUnvisited[host].remove(guestToAdd)
            guestQueue.remove(guestToAdd)
        
        while night[0][i] < m:
            guestToAdd = ""
            potentialGuests = intersection(peopleUnvisited[host],
                                           list(people.keys()))
            for guest in potentialGuests:
                if peopleNumbers[guest] + night[0][i] <= m:
                    guestToAdd = guest
                    break
                else:
                    guestQueue.append(guest)
                    del people[guest]

            #print(host, potentialGuests)
            if (len(potentialGuests) == 0 and
                len(list(people.keys())) > 0):                
                guestToAdd = list(people.keys())[0]
                potentialIndex = 1
                while (potentialIndex < len(list(people.keys())) and
                       peopleNumbers[guestToAdd] + night[0][i] > m):                    
                    guestToAdd = list(people.keys())[potentialIndex]
                    potentialIndex += 1
                    
            #print(host, guestToAdd)
            if guestToAdd != "":
                group.append(guestToAdd)
                animate_edge(host, guestToAdd)
                night[0][i] += peopleNumbers[guestToAdd]
                del people[guestToAdd]
                if guestToAdd in peopleUnvisited[host]:
                    peopleUnvisited[host].remove(guestToAdd)

        night.append(group)

    if len(list(people.keys())) > 0:
        remainingGuests = list(people.keys())
        for index, guest in enumerate(remainingGuests):
                night[(index % numGroups) + 1].append(guest)
                night[0][index % numGroups] += peopleNumbers[guest]

    superList.append(night)

    del people

    nightNum += 1
    
    print("Night #", nightNum)
    print("Group sizes are =", night[0])
    for j, group in enumerate(night[1:], start=1):
        print("Group #", j, "=", night[j])
    print()

input()
