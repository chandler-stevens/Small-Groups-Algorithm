# Filename: Small-Group.py
# Title: Small Group Allocation Algorithm Project
# Description: Generates list of lists of all Bible study small groups
#              necessary for all members to visit every other member's
#              home in the minimum number of nights as possible with a
#              time complexity of O(n^3).
# Contributors: Elizabeth Myers and Chandler Stevens
# Last Updated: 3/11/2020
# GitHub Repository:
#     https://github.com/chandler-stevens/Small-Groups-Algorithm
#
# Empiric runtime performance of each data file with m = 4 with animation:
# group1.txt runtime = 33 seconds
# group2.txt runtime = 247 seconds = 4 minutes 7 seconds
# group3.txt runtime = 443 seconds = 7 minutes 23 seconds

# OS library for installing Requirements and checking if file exists
from os import system, path

# Install Requirements, if necessary
system("pip install -r ./Requirements.txt --user")

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

    # Notify user of the list of names retrieved from data file
    print("People retrieved from " + filename + ":")
    print(list(peopleNumbers.keys()), "\n")

    # Get ideal group size from user
    m = RequestIdealGroupSize(n)

    # Ask the user if they would like to display the graph animation
    # The small groups can be modeled as a directed graph structure
    #     and displayed in an animated window; however, animating this
    #     takes substantially more empiric time. Therefore, if the user
    #     simply wants to run the algorithm, they have the option to
    #     do so, being that it can massively bring the runtime down.
    # For example, running the algorithm with n = 34 and m = 4:
    #     - With animation took 443 seconds or a little over 7 minutes.
    #     - Without animation took less than one second.
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
        # Remove leading and trailing whitespace
        line = line.strip()
        # If line is not a blank line
        if len(line) > 0:
            # If there is a comma
            if "," in line:
                # Then, add a married couple
                commaIndex = line.index(",")
                # Remove leading and trailing whitespace
                firstName = line[:commaIndex].strip()
                # Remove leading comma(s)
                # # Remove leading and trailing whitespace
                secondName = line[commaIndex:].lstrip(",").strip()
                # Format names to be separated by plus rather than comma
                name = firstName + " + " + secondName
                individuals = 2
            # Otherwise,
            else:
                # Add a single, unmarried person
                name = line
                individuals = 1

            # Test if a duplicate name was found
            if name in peopleOccurrences:
                # Then, increment histogram value
                peopleOccurrences[name] += 1
                # And append "(#)" to name for differentiation
                name += " (" + str(peopleOccurrences[name]) + ")"
            # Otherwise,
            else:
                # Add this name to histogram
                peopleOccurrences[name] = 1

            # Add team to maps
            peopleNumbers[name] = individuals
            peopleUnvisited[name] = []
            # Increment n, by number of individuals added
            n += individuals
            # Add node to graph
            G.add_node(name)
            # Increment number of teams
            teamCount += 1

    # Close input file stream
    fin.close()

    # Check if there were duplicates based on histogram values
    for team in peopleOccurrences:
        if peopleOccurrences[team] > 1:
            # Append "(1)" identifier to name of first team with that name
            peopleNumbers[team + " (1)"] = peopleNumbers.pop(team)
            peopleUnvisited[team + " (1)"] = peopleUnvisited.pop(team)

    # Perform an O(n^2) population of peopleUnvisited map that
    #     adds every name to value of person, except themselves
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

    # Set maximum group size to whichever is smaller, n or MAXIMUM_M constant
    if n < MAXIMUM_M:
        maxSize = n
    else:
        maxSize = MAXIMUM_M

    # While m value provided by user is invalid
    while not validM:
        # Notify user of invalid input for m
        if m < 2:
            print("Small groups should have at least 2 people.")
        elif m > maxSize:
            print("Group size cannot exceed number of people (" +
                  str(maxSize) + ").")

        try:
            # Ask user for m value input
            m = int(input("Please enter the ideal group size: "))
            # Valid m input value
            if 2 <= m <= maxSize:
                validM = True
        # If user did not enter a number
        except ValueError:
            # Then regard as invalid input, then ask again
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
#             pos represents the positions of the graph nodes
#             guest represents the vertex to draw arrow from
#             host represents the vertex to draw arrow to
# Returns: Nothing
def AnimateEdge(G, pos, guest, host):
    # *NOTE* Unfortunately, this function calls library package methods
    #            that add a very substantial amount of empirical time
    #            since it must draw an edge to an animated graph
    #        If the user does not care to see an animated graph,
    #            then the user can choose not to do so when prompted
    #            upon running the program.

    # Add an edge to the directed graph data structure
    G.add_edge(host, guest)
    # Draw a green arrow for that edge on the animation window
    nx.draw_networkx_edges(G, pos, edgelist=[(host, guest)],
                           edge_color='g')
    # Provide negligible delay of 1 picosecond so that
    #     animation window can be displayed
    plt.pause(0.000000000001)


# Purpose: Allocate teams to small groups in which every team visits every team
# Parameters: G represents the directed graph data structure
#             n represents the number of individuals
#             teamCount represents the number of teams
#             m represents the ideal group size
#             showAnimation represents whether to display graph
#             peopleNumbers represents size of each team
#             peopleUnvisited represents teams that have not visited each team
# Returns: superList represents a list of lists of all small groups
def AllocateSmallGroups(G, n, teamCount, m, showAnimation,
                        peopleNumbers, peopleUnvisited):
    # Setup graph animation window

    # Display all nodes in a circular layout with labels
    pos = nx.circular_layout(G)
    if showAnimation:
        pylab.show()
        nx.draw_circular(G, with_labels=True)

    # Determine the number of edges will present in the clique
    #     by taking the number of teams and multiplying it by
    #     one less of itself
    cliqueEdges = teamCount * (teamCount - 1)

    # Determine the likely number of groups that will be allocated
    #     for each night by doing integer division with n divided by m
    # Sometimes, there will be less groups due to edge cases where a
    #     group would only have had one person
    numGroups = n // m

    # Create a list to contain the lists of each group for each night
    superList = []
    # Start a counter for the number of nights
    nightNum = 0
    # Create a list of the teams that were hosts the last night
    previousHosts = []

    # While there are still teams who have not visited a different team
    #     (Alternatively, if there are still edges missing to form a clique)
    while len(sum(list(peopleUnvisited.values()), [])) > 0:
        # Make a deep copy of the peopleUnvisited map as it currently is
        people = deepcopy(peopleUnvisited)
        # Create a list to hold the groups for this night
        # Create a list within this that will hold the number of individuals
        #     assigned to each group of this night
        night = [[]]
        # Create a list of the teams that are hosts for this night
        hostNames = []

        # Create the expected number of groups
        for i in range(numGroups):
            # Retrieve the list of unassigned teams
            peopleList = list(people.keys())
            peopleNum = len(peopleList)
            # If there is only one unassigned team, do not create a new
            #     group, but let the remainingGuests list allocate
            #     this team to an existing group
            if peopleNum == 1:
                break

            # Create a map for teams that could be a host for this group
            potentialHosts = {}
            # Populate the map with unassigned teams that
            #     were not hosts last night
            for person in Difference(peopleList, previousHosts):
                potentialHosts[person] = people[person]

            # If there are potential hosts for this group
            if len(potentialHosts) > 0:
                # Select the host that has been visited least, which
                #     is the same as host with most unvisited teams
                #     (Alternatively, node of smallest degree)
                host = max(potentialHosts, key=lambda k: len(potentialHosts[k]))

                # Find the unassigned teams that were hosts last night, but
                #     are not hosts for this night
                previousHostOptions = Intersection(
                    peopleList, Difference(previousHosts, hostNames))
                if len(previousHostOptions) > 0:
                    # Reset the map to store possible hosts from last night
                    potentialHosts = {}
                    for person in previousHostOptions:
                        potentialHosts[person] = peopleUnvisited[person]
                    # Find the host that has been visited least, which
                    #     was a host last night, but not tonight
                    prevHost = max(potentialHosts,
                                   key=lambda k: len(potentialHosts[k]))
                    # If the host from last night has been visited less
                    #     than the host selected at the moment, then
                    #     select the host from last night instead
                    if (len(peopleUnvisited[host]) <
                            len(peopleUnvisited[prevHost])):
                        host = prevHost
            # Otherwise, if there are no unassigned teams that
            #     that were not hosts last night
            else:
                # Find the unassigned teams that were hosts last night, but
                #     are not hosts for this night
                previousHostOptions = Intersection(
                    peopleList, Difference(previousHosts, hostNames))
                if len(previousHostOptions) > 0:
                    # Reset the map to store possible hosts from last night
                    potentialHosts = {}
                    for person in previousHostOptions:
                        potentialHosts[person] = peopleUnvisited[person]
                    # Select the host that has been visited least, which
                    #     was a host last night, but not tonight
                    host = max(potentialHosts,
                               key=lambda k: len(potentialHosts[k]))
                # Otherwise, if there is no unassigned teams that could
                #     be hosts for this night, then do not create
                #     a group and just add any unassigned people
                #     using remainingGuests
                else:
                    break

            # Create a list for a new group for this night,
            #     starting with the selected host
            group = [host]
            # Initialize the initial list of the night list
            #     by setting the current size of this group
            #     to the number of individuals the host
            night[0].append(peopleNumbers[host])
            hostNames.append(host)
            # Since the host has been assigned to a group, remove them from map
            del people[host]

            # If the host already fills up the group
            if peopleNumbers[host] >= m:
                # Find any unassigned guests who have not yet visited this host
                potentialGuests = Intersection(peopleUnvisited[host],
                                               list(people.keys()))
                if len(potentialGuests) > 0:
                    # Add a guest anyway to this group, so that
                    #     this edge case is resolved by allowing teams
                    #     to visit this host, even though group is filled
                    guestToAdd = potentialGuests[0]
                    group.append(guestToAdd)
                    if showAnimation:
                        AnimateEdge(G, pos, guestToAdd, host)
                    # Increment group size by number of individuals of guest
                    night[0][i] += peopleNumbers[guestToAdd]
                    # Denote guest as assigned by removing from map
                    del people[guestToAdd]
                    # Remove guest from univisited list of host
                    peopleUnvisited[host].remove(guestToAdd)

            # While this group is not filled and there are unassigned guests
            while night[0][i] < m and len(list(people.keys())) > 0:
                guestToAdd = None
                peopleList = list(people.keys())
                peopleNum = len(peopleList)
                # Find any unassigned guests who have not yet visited this host
                potentialGuests = Intersection(peopleUnvisited[host],
                                               peopleList)
                potentialNum = len(potentialGuests)

                # If adding any guest at any point will overflow for this host
                if peopleNumbers[host] + 2 > m:
                    # Then add a guest anyway with preference toward unvisited
                    if potentialNum > 0:
                        guestToAdd = potentialGuests[0]
                    else:
                        guestToAdd = peopleList[0]
                
                # If there are potential guests but still no guest selected 
                if potentialNum > 0 and guestToAdd is None:
                    # If a couple can fit
                    if night[0][i] + 2 <= m:
                        # Then add a couple, if one is available
                        for guest in potentialGuests:
                            if peopleNumbers[guest] == 2:
                                guestToAdd = guest
                                break

                    # Otherwise, if still no guest selected and
                    #     if a single can fit 
                    if guestToAdd is None and night[0][i] + 1 <= m:
                        for guest in potentialGuests:
                            # Then add a single, if one is available
                            if peopleNumbers[guest] == 1:
                                guestToAdd = guest
                                break

                    # Otherwise, stop attempting to add guests to this group and
                    # simply allow the remainingGuests list to fill this group
                    if guestToAdd is None:
                        break
                # Otherwise, if there are, in fact, no potential guests and
                #     still no guest selected but there are unassigned guests
                elif potentialNum == 0 and guestToAdd is None and peopleNum > 0:
                    # Then add a guest anyway 
                    guestToAdd = peopleList[0]
                    potentialIndex = 1
                    # Try the next guest if the current one will not fit
                    while (potentialIndex < peopleNum and
                           peopleNumbers[guestToAdd] + night[0][i] > m):
                        guestToAdd = peopleList[potentialIndex]
                        potentialIndex += 1
                    
                # If there is a guest selected
                if guestToAdd is not None:
                    # Add the guest to this group
                    group.append(guestToAdd)
                    if showAnimation:
                        AnimateEdge(G, pos, guestToAdd, host)
                    # Increment group size by number of individuals of guest
                    night[0][i] += peopleNumbers[guestToAdd]
                    # Denote guest as assigned by removing from map
                    del people[guestToAdd]
                    # Remove guest from univisited list of host, if the
                    #     guest is still in that list
                    if guestToAdd in peopleUnvisited[host]:
                        peopleUnvisited[host].remove(guestToAdd)

            # Add this group to the current night
            night.append(group)

        # As a catch-all, compile a list of any guests that were not assigned
        #     in the current night
        remainingGuests = list(people.keys())
        # If there were any extra unassigned guests
        if len(remainingGuests) > 0:
            # Sort them with couples at the beginning
            sortedRemainingGuests = []
            for guest in remainingGuests:
                if peopleNumbers[guest] == 2:
                    sortedRemainingGuests.insert(0, guest)
                else:
                    sortedRemainingGuests.append(guest)
            # Add each guest to the smallest group
            for guest in sortedRemainingGuests:
                # Find the group with least number of individuals
                smallestGroupIndex = night[0].index(min(night[0]))
                # Find who the host is for that group
                host = night[smallestGroupIndex + 1][0]
                # Add the guest to that group
                night[smallestGroupIndex + 1].append(guest)
                if showAnimation:
                    AnimateEdge(G, pos, guest, host)
                # Increment group size by number of individuals of extra guest
                night[0][smallestGroupIndex] += peopleNumbers[guest]
                # Remove guest from univisited list of host, if the
                #     guest is still in that list
                if guest in peopleUnvisited[host]:
                    peopleUnvisited[host].remove(guest)

        # Add this filled night list to the list of lists
        superList.append(night)

        # Set the list of current hosts as the previous hosts for the next night
        previousHosts = hostNames

        # Increment the night counter
        nightNum += 1

        # Print out the details for the night, including the
        #     size of each group and the groups themselves
        print("Night #", nightNum)
        print("Group sizes are =", night[0])
        for j, group in enumerate(night[1:], start=1):
            print("Group #", j, "=", night[j])

        # Determine how much progress has been made on forming a clique
        if showAnimation:
            edges = G.number_of_edges()
        else:
            edges = cliqueEdges - len(sum(list(peopleUnvisited.values()), []))

        # Print out progress of algorithm as a percentage, which is
        #     how many edges have been added so far divided by
        #     the total number of edges required to form a clique
        print("Clique is", int(100 * (edges / cliqueEdges)),
              "% complete (" + str(edges), "of",
              str(cliqueEdges) + " edges).\n")

    return superList


# Call main function to begin program
try:
    Main()
# Gracefully close program upon any exceptions
except Exception as error:
    print("Error: " + str(error))
    input("\n\nPress the Enter key to exit . . .")
    exit(1)
