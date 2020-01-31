from collections import OrderedDict
from networkx import nx
import matplotlib.pyplot as plt
import pylab

fin = open("GroupSW.txt")

people = OrderedDict()
n = 0
m = 4

G = nx.DiGraph()
labels = {}
nodeIndex = 0

for line in fin:
    if "," in line:
        commaIndex = line.index(",")
        nameCouple = line[:commaIndex] + " + " + line[commaIndex + 1:-1]
        people[nameCouple] = 2
        # Place couples at beginning
        people.move_to_end(nameCouple, False)
        G.add_node(nameCouple)
        labels[nodeIndex] = nameCouple
        n += 2
    else:
        nameSingle = line[:-1]
        people[nameSingle] = 1
        G.add_node(nameSingle)
        labels[nodeIndex] = nameSingle
        n += 1
    nodeIndex += 1

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
    host = list(people.items())[hostIndex]
    hostName = host[0]
    hostNumber = host[1]
    iteration.append([hostName])
    # Initialize group sizes to zero
    iteration[0].append(hostNumber)

# Add guests
nextGuestIndex = numGroups

# While there are still unmatched guests
while nextGuestIndex < len(list(people.items())):
    # Select next guest
    guest = list(people.items())[nextGuestIndex]
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
    animate_edge(hostName, guestName)
    nextGuestIndex += 1

hostOffset = numGroups

for k in range(numGroups):
    if k == 0:
        peopleList = list(people.items())
    else:
        for q in range(1, numGroups + 1):
            current = peopleList.pop((q * numGroups) - 1)
            newIndex = (q - 1) * numGroups
            peopleList.insert(newIndex, current)
    print(peopleList)
    biggestGroupSize = m
    i = 0
    while i < biggestGroupSize:
        print(i, biggestGroupSize)
        # Initialize hosts
        iteration = [[]]
        superList.append(iteration)
        if hostOffset >= len(people):
            hostOffset = 0
        for j in range(numGroups):
            hostIndex = j + hostOffset
            host = list(people.items())[hostIndex]
            hostName = host[0]
            hostNumber = host[1]
            iteration.append([hostName])
            # Initialize group sizes to zero
            iteration[0].append(hostNumber)
            hostNames.append(hostName)
        
        # Add guests
        nextGuestIndex = 0

        # While there are still unmatched guests
        while nextGuestIndex < len(peopleList):
            if peopleList[nextGuestIndex][0] in hostNames:
                nextGuestIndex += numGroups
                continue
            # Select next guest
            guest = peopleList[nextGuestIndex]
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
            animate_edge(hostName, guestName)
            nextGuestIndex += 1
        hostNames = []
        hostOffset += numGroups
        biggestGroupSize = len(iteration[1])
        i += 1

for i, subparList in enumerate(superList, start=1):
    print("Night #", i)
    print("Group sizes are =", subparList[0])
    for j, group in enumerate(subparList[1:], start=1):
        print("Group #", j, "=", subparList[j])
    print()

nx.draw(G, with_labels = True)
plt.show()
