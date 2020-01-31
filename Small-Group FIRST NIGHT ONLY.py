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

idealSize = n // m
superList = []
queue = []

queueIndex = idealSize
overflow = False

# Initialize hosts
iteration = [[]]
superList.append(iteration)
for i in range(idealSize):
    host = list(people.items())[i]
    hostName = host[0]
    hostNumber = host[1]
    iteration.append([hostName])
    # Initialize group sizes to zero
    iteration[0].append(hostNumber)

# Add guests
nextGuestIndex = idealSize
# While there are still unmatched guests
while nextGuestIndex < len(people):
    # Select next guest
    guest = list(people.items())[nextGuestIndex]
    guestName = guest[0]
    guestNumber = guest[1]
    # Determine smallest group so far
    smallestGroupIndex = iteration[0].index(min(iteration[0]))
    # Add guest to smallest group
    iteration[smallestGroupIndex + 1].append(guestName)
    # Increment size of group
    iteration[0][smallestGroupIndex] += 1
    # Add edge to graph
    hostName = iteration[smallestGroupIndex + 1][0]
    animate_edge(hostName, guestName)
    nextGuestIndex += 1

print(superList)
