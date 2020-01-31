from collections import OrderedDict
from networkx import nx
import matplotlib.pyplot as plt
import pylab

fin = open("GroupSW.txt")

peopleNumbers = OrderedDict()
peopleUnvisited = OrderedDict()
n = 0
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
    G.add_edge(hostName, guestName)
    nx.draw_circular(G, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(host, guest)], edge_color='g', width=5)
    fig.canvas.draw()
    pylab.draw()
    plt.pause(1)

numGroups = n // m
superList = []
hostOffset = 0
hostNames = []

# Run first iteration
iteration = [[]]
superList.append(iteration)
for j in range(numGroups):
    hostIndex = j
    host = list(peopleNumbers.items())[hostIndex]
    hostName = host[0]
    hostNumber = host[1]
    iteration.append([hostName])
    # Initialize group sizes to zero
    iteration[0].append(hostNumber)

# Add guests
nextGuestIndex = numGroups

# While there are still unmatched guests
while nextGuestIndex < len(list(peopleNumbers.items())):
    # Select next guest
    guest = list(peopleNumbers.items())[nextGuestIndex]
    guestName = guest[0]
    guestNumber = guest[1]
    # Determine smallest group so far
    smallestGroupIndex = iteration[0].index(min(iteration[0]))
    # Add guest to smallest group
    iteration[smallestGroupIndex + 1].append(guestName)
    # Increment size of group
    iteration[0][smallestGroupIndex] += guestNumber
    # Add edge to graph
    hostName = iteration[smallestGroupIndex + 1][0]
    if guestName in peopleUnvisited[hostName]:
        peopleUnvisited[hostName].remove(guestName)
    animate_edge(hostName, guestName)
    nextGuestIndex += 1

hostOffset = numGroups

blueprint = []
hostList = []
for group in superList[0][1:]:
    hostList.append(group[0])

for k in range(numGroups):
    if k == 0:
        hostIndex = 1
        for index, host in enumerate(hostList):
            guests = superList[0][index + 1][1:]
            blueprint.append([host] + guests)
    else:
        hostIndex = 0
        hostList.append(hostList.pop(0))
        blueprint = []
        for index, host in enumerate(hostList):
            guests = superList[0][index + 1][1:]
            blueprint.append([host] + guests)
    print(blueprint)
    biggestGroupSize = m
    i = 1
    while i < biggestGroupSize:
        # Initialize hosts
        iteration = [[]]
        superList.append(iteration)
        for j in range(numGroups):
            hostName = blueprint[j][hostIndex]
            hostNumber = peopleNumbers[hostName]
            iteration.append([hostName])
            # Initialize group sizes to zero
            iteration[0].append(hostNumber)
            # Add guests
            for index, guest in enumerate(blueprint[j]):
                if guest != hostName:
                    guestNumber = peopleNumbers[guest]
                    iteration[j + 1].append(guest)
                    # Increment size of group
                    iteration[0][j] += guestNumber
                    # Add edge to graph
                    if guest in peopleUnvisited[hostName]:
                        peopleUnvisited[hostName].remove(guest)
                    animate_edge(hostName, guestName)
        hostIndex += 1
        biggestGroupSize = len(iteration[1])
        i += 1


# Rotate

# Run first iteration
hostNames = []
rotationIndex = len(superList)
iteration = [[]]
superList.append(iteration)
groupSize = len(superList[0][1])
groupIndex = 1
for j in range(numGroups):
    if j == groupSize:
        groupIndex += 1
        groupSize = len(superList[0][groupIndex])
    hostName = superList[0][groupIndex][j]
    hostNames.append(hostName)
    hostNumber = peopleNumbers[hostName]
    iteration.append([hostName])
    # Initialize group sizes to zero
    iteration[0].append(hostNumber)
    for i in range(1, numGroups):
        iteration[i].append(superList[0][i + 1][0])
print("Heyo", iteration)
##
### Add guests
##nextGuestIndex = 0
##
### While there are still unmatched guests
##while nextGuestIndex < len(list(peopleNumbers.items())):
##    # Select next guest
##    guest = list(peopleNumbers.items())[nextGuestIndex]
##    guestName = guest[0]
##    if guestName not in hostNames:
##        guestNumber = guest[1]
##        # Determine smallest group so far
##        smallestGroupIndex = iteration[0].index(min(iteration[0]))
##        # Add guest to smallest group
##        iteration[smallestGroupIndex + 1].append(guestName)
##        # Increment size of group
##        iteration[0][smallestGroupIndex] += guestNumber
##        # Add edge to graph
##        hostName = iteration[smallestGroupIndex + 1][0]
##        if guestName in peopleUnvisited[hostName]:
##            peopleUnvisited[hostName].remove(guestName)
##        animate_edge(hostName, guestName)
##    nextGuestIndex += 1

hostOffset = numGroups

blueprint = []
hostList = []
j = 1
for i in range(numGroups):
    if j == len(superList[0][j]):
        j += 1
    hostList.append(superList[0][j][i])

for k in range(numGroups):
    if k == 0:
        hostIndex = 1
        for index, host in enumerate(hostList):
            guests = superList[rotationIndex][index + 1][1:]
            blueprint.append([host] + guests)
    else:
        hostIndex = 0
        hostList.append(hostList.pop(0))
        blueprint = []
        for index, host in enumerate(hostList):
            guests = superList[rotationIndex][index + 1][1:]
            blueprint.append([host] + guests)
    print(blueprint)
    biggestGroupSize = m
    i = 1
    while i < biggestGroupSize:
        # Initialize hosts
        iteration = [[]]
        superList.append(iteration)
        for j in range(numGroups):
            hostName = blueprint[j][hostIndex]
            hostNumber = peopleNumbers[hostName]
            iteration.append([hostName])
            # Initialize group sizes to zero
            iteration[0].append(hostNumber)
            # Add guests
            for index, guest in enumerate(blueprint[j]):
                if guest != hostName:
                    guestNumber = peopleNumbers[guest]
                    iteration[j + 1].append(guest)
                    # Increment size of group
                    iteration[0][j] += guestNumber
                    # Add edge to graph
                    if guest in peopleUnvisited[hostName]:
                        peopleUnvisited[hostName].remove(guest)
                    animate_edge(hostName, guestName)
        hostIndex += 1
        biggestGroupSize = len(iteration[1])
        i += 1

print("\n\n")
for team in peopleUnvisited:
    print(team, peopleUnvisited[team])
print("\n\n")

for i, subparList in enumerate(superList, start=1):
    print("Night #", i)
    print("Group sizes are =", subparList[0])
    for j, group in enumerate(subparList[1:], start=1):
        print("Group #", j, "=", subparList[j])
    print()
