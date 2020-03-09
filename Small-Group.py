# Filename: Small-Group.py
# Title: Small Group Allocation Algorithm Project
# Description: Generates list of lists of all Bible study small groups
#              necessary for all members to visit every other member's
#              home in the minimum number of nights as possible with a
#              time complexity of O(n^3).
# Contributors: Elizabeth Myers and Chandler Stevens
# Last Updated: 3/9/2020
# GitHub Classroom Private Repository:
#     https://github.com/csc3430-winter2020/community-small-groups-palpateam
#
# Runtime of each data file with m = 4:
# group1.txt runtime = 144 seconds = 2 minutes 24 seconds
# group2.txt runtime = 958 seconds = 15 minutes 58 seconds
# group3.txt runtime =  seconds =  minutes  seconds

# OS library for installing Requirements and checking if file exists
from os import system, path

# Install Requirements, if necessary
system("pip install -r ./Requirements.txt")

# Python Standard Library

# System library for printing exception error message
from sys import exc_info
# Deepcopy to generate deep copy of maps
from copy import deepcopy
# Timeit Timeit to measure empiric time performance
from timeit import timeit

# Override Timeit Template to return the return value of function call
timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

# Requirements

# Networkx for directed graph data structure
from networkx import nx
# Matplotlib Pyplot Pause for controlling animation speed for human convenience
from matplotlib import pyplot as plt
# Matplotlib Pylab Show for drawing animation
from matplotlib import pylab


# Purpose: Ask user for file, ideal group size, and then generate small groups
# Parameters: None
# Returns: Nothing
def Main():
    # Ask user for input file until given file exists
    filename = input("Please enter the filename: ")
    while not path.isfile(filename):
        print("File", filename, "not found.")
        filename = input("Please enter the filename: ")

    print("\nOpening", filename, " . . .\n")

    # Parse file and generate n, teamCount and peopleUnvisited
    G, n, teamCount, peopleNumbers, peopleUnvisited = ParseTeamsFile(filename)

    # Get ideal group size from user
    m = RequestIdealGroupSize(n)

    print("\nInitiating Small Group Allocation Algorithm . . .\n")

    # Generate list of lists while also measuring the runtime performance
    runtime, superList = timeit(lambda:
                                AllocateSmallGroups(G, n, teamCount, m,
                                                    peopleNumbers,
                                                    peopleUnvisited),
                                number=1)

    # Print runtime performance
    print("Allocated all small groups with n =", n, "and m =", m, "in",
          runtime, "seconds.")

    # Print list of lists
    print("\n\nPrinting entire list of lists of all small groups . . . \n\n")
    print(superList)

    input("\n\nPress any key to exit . . .")


# Purpose: Parse compatible data file and generate graph and metadata
# Parameters: filename represents the name of the file provided by user
# Returns: G represents the directed graph data structure
#          n represents the number of individuals
#          teamCount represents the number of teams
#          peopleNumbers represents size of each team
#          peopleUnvisited represents teams that have not visited each team
def ParseTeamsFile(filename):
    # Open file stream using provided filename
    fin = open(filename)

    # Initialize directed graph data structure
    G = nx.DiGraph()

    # Initialize number of people to zero
    n = 0
    # Get number of teams (n, but with each couple consolidated into one)
    teamCount = 0

    # Initialize map for team sizes with value 1 for single or 2 for a couple
    peopleNumbers = {}
    # Initialize map for list of teams who have not visited each team
    peopleUnvisited = {}

    # Iterate through file and parse each team
    for line in fin:
        try:
            if "," in line:
                commaIndex = line.index(",")
                name = line[:commaIndex] + " + " + line[commaIndex + 1:-1]
                peopleNumbers[name] = 2
                n += 2
            else:
                name = line[:-1]
                peopleNumbers[name] = 1
                n += 1

            peopleUnvisited[name] = []
            G.add_node(name)
            teamCount += 1
        except:
            print("File Read Error: ", exc_info()[0])
            input("Press any key to exit . . .")
            exit(1)

    fin.close()

    for host in peopleNumbers:
        for guest in peopleNumbers:
            if host != guest:
                peopleUnvisited[host].append(guest)

    return G, n, teamCount, peopleNumbers, peopleUnvisited


# Purpose: Ask user for valid ideal group size
# Parameters: n represents the number of individuals
# Returns: m represents ideal group size greater than 1
#              and less than or equal to n
def RequestIdealGroupSize(n):
    validM = False
    # Minimum group size is two
    m = 2

    while not validM:
        if m < 2:
            print("Small groups should have at least 2 people.")
        elif m > n:
            print("Group size cannot exceed number of people (" + str(n) + ").")

        try:
            m = int(input("Please enter the ideal group size: "))
            if 2 <= m <= n:
                validM = True
        except ValueError:
            print("Please enter an integer for the ideal group size.")

    return m


# Purpose: Determine intersection of two lists
# Parameters: lst1 represents the first list
#             lst2 represents the second list
# Returns: A list of elements from lst1 that also exist in lst2
def Intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


# Purpose: Determine values unique to a list
# Parameters: src represents the source list
#             blacklist represents the blacklist of unwanted elements
# Returns: A list of elements from src that do not exist in blacklist
def Difference(src, blk):
    return list(set(src) - set(blk))


# Purpose: Adds an edge to a graph and updates animation
# Parameters: G represents the directed graph data structure
#             fig represents the animation canvas figure
#             pos represents the
#             guest represents the vertex to draw arrow from
#             host represents the vertex to draw arrow to
# Returns: Nothing
def AnimateEdge(G, fig, pos, guest, host):
    fig.clear()
    G.add_edge(host, guest)
    nx.draw_circular(G, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(host, guest)],
                           edge_color='g', width=5)
    fig.canvas.draw()
    pylab.draw()
    plt.pause(0.1)


# Purpose: Allocate teams to small groups in which every team visits every team
# Parameters: G represents the directed graph data structure
#             n represents the number of individuals
#             teamCount represents the number of teams
#             m represents the ideal group size
#             peopleNumbers represents size of each team
#             peopleUnvisited represents teams that have not visited each team
# Returns: Nothing
def AllocateSmallGroups(G, n, teamCount, m, peopleNumbers, peopleUnvisited):
    pos = nx.circular_layout(G)
    pylab.show()
    fig = pylab.figure()

    cliqueEdges = teamCount * (teamCount - 1)

    numGroups = n // m

    superList = []
    nightNum = 0
    previousHosts = []
    while len(sum(list(peopleUnvisited.values()), [])) > 0:
        people = deepcopy(peopleUnvisited)
        night = [[]]
        guestQueue = []
        hostNames = []

        for i in range(numGroups):
            group = []
            potentialHosts = {}
            for person in Difference(list(people.keys()), previousHosts):
                potentialHosts[person] = people[person]

            if len(potentialHosts) > 0:
                host = max(potentialHosts, key=lambda k: len(potentialHosts[k]))
                del people[host]
            else:
                if len(guestQueue) > 0:
                    host = guestQueue.pop()
                else:
                    host = Intersection(list(people.keys()),
                                        Difference(previousHosts, hostNames))[0]
                    del people[host]

            group.append(host)
            night[0].append(peopleNumbers[host])
            hostNames.append(host)

            for guest in guestQueue:
                if peopleNumbers[guest] + night[0][i] <= m:
                    group.append(guest)
                    AnimateEdge(G, fig, pos, guest, host)
                    night[0][i] += peopleNumbers[guest]
                    if guest in peopleUnvisited[host]:
                        peopleUnvisited[host].remove(guest)
                    guestQueue.remove(guest)
                    break

            while night[0][i] < m and len(list(people.keys())) > 0:
                guestToAdd = ""
                potentialGuests = Intersection(peopleUnvisited[host],
                                               list(people.keys()))
                noSingles = True
                for guest in potentialGuests:
                    if peopleNumbers[guest] == 1:
                        noSingles = False
                    if peopleNumbers[guest] + night[0][i] <= m:
                        guestToAdd = guest
                        break
                    else:
                        guestQueue.append(guest)
                        del people[guest]

                if guestToAdd == "" and noSingles and len(potentialGuests) > 0:
                    guestToAdd = potentialGuests[0]
                    if guestToAdd in guestQueue:
                        guestQueue.remove(guestToAdd)
                        people[guestToAdd] = []
                elif len(potentialGuests) == 0 and len(list(people.keys())) > 0:
                    guestToAdd = list(people.keys())[0]
                    potentialIndex = 1
                    while (potentialIndex < len(list(people.keys())) and
                           peopleNumbers[guestToAdd] + night[0][i] > m):
                        guestToAdd = list(people.keys())[potentialIndex]
                        potentialIndex += 1

                if guestToAdd != "":
                    group.append(guestToAdd)
                    AnimateEdge(G, fig, pos, guestToAdd, host)
                    night[0][i] += peopleNumbers[guestToAdd]
                    del people[guestToAdd]
                    if guestToAdd in peopleUnvisited[host]:
                        peopleUnvisited[host].remove(guestToAdd)

            night.append(group)

        for guest in guestQueue:
            people[guest] = []

        remainingGuests = list(people.keys())
        if len(remainingGuests) > 0:
            sortedRemainingGuests = []
            for guest in remainingGuests:
                if peopleNumbers[guest] == 2:
                    sortedRemainingGuests.insert(0, guest)
                else:
                    sortedRemainingGuests.append(guest)
            for guest in sortedRemainingGuests:
                smallestGroupIndex = night[0].index(min(night[0]))
                night[smallestGroupIndex + 1].append(guest)
                night[0][smallestGroupIndex] += peopleNumbers[guest]

        superList.append(night)

        previousHosts = hostNames

        nightNum += 1

        edges = G.number_of_edges()

        print("Night #", nightNum)
        print("Group sizes are =", night[0])
        for j, group in enumerate(night[1:], start=1):
            print("Group #", j, "=", night[j])

        print("Clique is", int(100 * (edges / cliqueEdges)),
              "% complete (" + str(edges), "of",
              str(cliqueEdges) + " edges).\n")

    return superList


Main()
