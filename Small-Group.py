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
# Empiric runtime performance of each data file with m = 4 with animation:
# group1.txt runtime = 35 seconds
# group2.txt runtime = 230 seconds = 3 minutes 50 seconds
# group3.txt runtime = 505 seconds = 8 minutes 25 seconds

# OS library for installing Requirements and checking if file exists
from os import system, path

# Install Requirements, if necessary
system("pip install -r ./Requirements.txt")

# Python Standard Library

# Deepcopy to generate deep copy of maps
from copy import deepcopy
# Timeit to measure empiric time performance
import timeit

# Override Timeit Template to return the return value of function call
new_template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret_val = {stmt}
    _t1 = _timer()
    return _t1 - _t0, ret_val
"""
timeit.template = new_template

# Requirements

# Networkx for directed graph data structure
from networkx import nx
# Matplotlib Pyplot Pause for controlling animation speed for human convenience
from matplotlib import pyplot as plt
# Matplotlib Pylab Show for drawing animation
from matplotlib import pylab

# Constant for maximum allowed size m for a small group
MAXIMUM_M = 10


# Purpose: Ask user for file, ideal group size, and then generate small groups
# Parameters: None
# Returns: Nothing
def Main():
    print("\nFinished installing all necessary Requirements.\n")
    
    # Ask user for input file until given file exists
    filename = input("Please enter the filename: ")
    while not path.isfile(filename):
        print("File", filename, "not found.")
        filename = input("Please enter the filename: ")

    print("\nOpening", filename, " . . .\n")

    # Parse file and generate n, teamCount and peopleUnvisited
    G, n, teamCount, peopleNumbers, peopleUnvisited = ParseTeamsFile(filename)

    print("People retrieved from " + filename + ":")
    print(list(peopleNumbers.keys()), "\n")

    # Get ideal group size from user
    m = RequestIdealGroupSize(n)

    showAnimation = False
    choice = input("\nWould you like to see an animated graph? (y/n) ").lower()
    if choice == "y":
        showAnimation = True

    print("\nInitiating Small Group Allocation Algorithm . . .\n")

    # Generate list of lists while also measuring the runtime performance
    runtime, superList = timeit.timeit(
        lambda: AllocateSmallGroups(G, n, teamCount, m, showAnimation,
                                    peopleNumbers, peopleUnvisited),
        number=1)

    # Print runtime performance
    print("Allocated all small groups with n =", n, "and m =", m, "in",
          int(runtime), "seconds.")

    # Print list of lists
    print("\n\nPrinting entire list of lists of all small groups . . . \n")
    print("[")
    for index, night in enumerate(superList):
        if index < len(superList) - 1:
            print(str(night) + ",")
        else:
            print(night)
    print("]")

    input("\n\nPress the Enter key to exit . . .")


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
    # Initialize map as histogram of teams as to handle duplicates
    peopleOccurrences = {}

    # Iterate through file and parse each team
    for line in fin:
        line = line.strip()
        if len(line) > 0:
            if "," in line:
                commaIndex = line.index(",")
                firstName = line[:commaIndex].strip()
                secondName = line[commaIndex:].lstrip(",").strip()
                name = firstName + " + " + secondName
                individuals = 2
            else:
                name = line
                individuals = 1

            if name in peopleOccurrences:
                peopleOccurrences[name] += 1
                name += " (" + str(peopleOccurrences[name]) + ")"
            else:
                peopleOccurrences[name] = 1
            peopleNumbers[name] = individuals
            n += individuals
            peopleUnvisited[name] = []
            G.add_node(name)
            teamCount += 1

    fin.close()

    for team in peopleOccurrences:
        if peopleOccurrences[team] > 1:
            peopleNumbers[team + " (1)"] = peopleNumbers.pop(team)
            peopleUnvisited[team + " (1)"] = peopleUnvisited.pop(team)

    for host in peopleNumbers:
        for guest in peopleNumbers:
            if host != guest:
                peopleUnvisited[host].append(guest)

    return G, n, teamCount, peopleNumbers, peopleUnvisited


# Purpose: Ask user for valid ideal group size
# Parameters: n represents the number of individuals
# Returns: m represents ideal group size greater than 1
#              and less than or equal to (n or MAXIMUM_M, whichever is smaller)
def RequestIdealGroupSize(n):
    validM = False
    # Minimum group size is two
    m = 2

    if n < MAXIMUM_M:
        maxSize = n
    else:
        maxSize = MAXIMUM_M

    while not validM:
        if m < 2:
            print("Small groups should have at least 2 people.")
        elif m > maxSize:
            print("Group size cannot exceed number of people (" +
                  str(maxSize) + ").")

        try:
            m = int(input("Please enter the ideal group size: "))
            if 2 <= m <= maxSize:
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
    G.add_edge(host, guest)
    nx.draw_networkx_edges(G, pos, edgelist=[(host, guest)],
                           edge_color='g')
    plt.pause(0.000000000001)


# Purpose: Allocate teams to small groups in which every team visits every team
# Parameters: G represents the directed graph data structure
#             n represents the number of individuals
#             teamCount represents the number of teams
#             m represents the ideal group size
#             peopleNumbers represents size of each team
#             peopleUnvisited represents teams that have not visited each team
# Returns: Nothing
def AllocateSmallGroups(G, n, teamCount, m, showAnimation,
                        peopleNumbers, peopleUnvisited):
    pos = nx.circular_layout(G)
    pylab.show()
    fig = pylab.figure()
    nx.draw_circular(G, with_labels=True)
    
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
                    if showAnimation:
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
                    elif (guestToAdd == "" and
                          peopleNumbers[guest] + night[0][i] <= m):
                        guestToAdd = guest

                if guestToAdd == "":
                    for guest in potentialGuests:
                        if peopleNumbers[guest] + night[0][i] <= m:
                            guestToAdd = guest
                            break
                        else:
                            guestQueue.append(guest)
                            del people[guest]

                if guestToAdd == "":
                    if (noSingles and len(potentialGuests) > 0 and
                        i == numGroups - 1):
                        guestToAdd = potentialGuests[0]
                        if guestToAdd in guestQueue:
                            guestQueue.remove(guestToAdd)
                            people[guestToAdd] = []
                    elif (len(potentialGuests) == 0 and len(list(people.keys())) > 0):
                        guestToAdd = list(people.keys())[0]
                        potentialIndex = 1
                        while (potentialIndex < len(list(people.keys())) and
                               peopleNumbers[guestToAdd] + night[0][i] > m):
                            guestToAdd = list(people.keys())[potentialIndex]
                            potentialIndex += 1

                if guestToAdd != "":
                    group.append(guestToAdd)
                    if showAnimation:
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
                host = night[smallestGroupIndex + 1][0]
                night[smallestGroupIndex + 1].append(guest)
                if showAnimation:
                    AnimateEdge(G, fig, pos, guest, host)
                night[0][smallestGroupIndex] += peopleNumbers[guest]
                if guest in peopleUnvisited[host]:
                    peopleUnvisited[host].remove(guest)

        superList.append(night)

        previousHosts = hostNames

        nightNum += 1

        print("Night #", nightNum)
        print("Group sizes are =", night[0])
        for j, group in enumerate(night[1:], start=1):
            print("Group #", j, "=", night[j])

        if showAnimation:
            edges = G.number_of_edges()
        else:
            edges = cliqueEdges - len(sum(list(peopleUnvisited.values()), []))

        print("Clique is", int(100 * (edges / cliqueEdges)),
              "% complete (" + str(edges), "of",
              str(cliqueEdges) + " edges).\n")

    return superList


try:
    Main()
except Exception as error:
    print("Error: " + str(error))
    input("\n\nPress the Enter key to exit . . .")
    exit(1)
