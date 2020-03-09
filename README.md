# Creating Community Small Groups
A work by: Dr. Carlos Arias, Elizabeth Myers, and Chandler Stevens

Algorithm for allocating church members to small groups for CSC 3430 Algorithm Design and Analysis.

## Description
A church community would like to form small groups of people for Bible studies. These Bible studies will serve to explore and share
deep theological discussions between community members. In order to facilitate relational connections between all members of this
community, every person should visit every other member's house. Each person hosting a small group meeting at their house is 
considered a host. 

The purpose of this project is to allocate people within a church community into ideally sized small groups. The program created for
this project will read a list of people from a text file and assign these people to groups of the desired size. The output of this 
project is a list of lists. Each list will have a list of that night's hosts and their guests. An additional constraint
of this project is that if a person is married, then that person must always be placed in the same small group that their spouse is 
placed in. 

In the text file each individual person is followed by a new line and each married couple is joined with a comma and
followed by a new line.

The programming langauge that we utilize for our project is Python 3. We chose this language because it has supported graph libraries
(such as networkx) and our group decided we wanted to familiarize ourselves more with a scripting language.

## Requirements
The required Python version for our program is Python 3.7 or up. 

The required Python libraries for our program include: 
- networkx (utilized to create graph data structures)
- matplotlib (utilized to display and animate graphs in our program)
- numpy (utilized to support matplotlib)


## User Manual
*Once a person clones this into their computer how the person is supposed to run the program, add screenshots showing how your program works, also add here the link to the Youtube video showing the program running*
1. Once you have cloned the repo, unzip or extract the files as necessary.
2. Then, inside the folder, double-click the "Small-Group.py" file to run the program.
3. The program will prompt you for a filename, so enter a group textfile (e.g. "group1.txt").
4. Next, the program will prompt you for a ideal group size, which should be positive integer.
5. Then, the program will immediately began the algorithm while displaying its progress on the graph animation window.
6. Finally, once the program has completed, the set of sets of each group for each night will be displayed.

## Reflection
*The difficulties you faced during this assignment and how you prevailed. Add screenshots of your 
program running, and add the set of sets for each file. 
A link to a YouTube video showing your program running with an explanation
of the steps that you are taking*

In order to find the set of sets of teams in the minimum amount of iterations, we implemented an algorithm that runs in O(n^3) time.
We initialize the algorithm in the following way: We read the text file and for each team, we added them to a map _peopleNumbers_ with
the values being 1 if it is a single person and 2 if there is a married couple. We then made another map _peopleUnivisited_ that
generates a list of all the people who have not visited each host. We also created a directed graph initialized with the number of
teams, so each team had their own node. We determined how many groups there should be by doing integer division between _n_ (the number
of individuals) divided by _m_ (the ideal group size entered by the user). We also initialized a list _superList_ that will contain 
all of the sub-lists, which will be returned as the results to be outputted. The last items we set up was a list of hosts _hostNames_
who hosted the previous night. 
The algorithm follows the following logic:
while there are still people who have not visited every host's house (there are still values in _peopleUnvisited_) O(n)
  Make a deep copy of the map of unvisited people called _people_ O(n)
  Initialize a sublist to store the groups for this night called _night_
  Initialize a queue _guestQueue_ in case a team doesn't fit in a group and goes above the ideal group size _m_
  for each group to meet at a host's house (counter-controlled loop from i=0 to i=_n/m_-1)  O(n)
    Initialize a list called _group_ for that group
    Select a host based on which team has been visited the least as long as they aren't in the _hostNames_ list O(n)
    Add host to _group_ and to _hostNames_
    Iterate through _guestQueue_ and add a teams from it if, when added, they will fit the ideal group size _m_ 
      if a team was added from _guestQueue_, draw an edge from that guest node to the host node they were added to
    while _group_ is not filled and less than the ideal group size _m_   
      find the intersection between _peopleUnvisited_ of that host and the _people_ who have not visited that host O(n)
      select a guest that will fit in _group_, but if one does not fit then they are added to the _guestQueue_ 
      if there is no one from _people_ who has also not visited, still add a team to fill the group O(n)
      add a team to _group_ and remove them from _peopleUnvisited_ of their host and _people_
      if a team was added, draw an edge from that guest node to the host node they were added to
    add the now filled _group_ to _night_ 
   if there is anyone left in _people_, distribute them across all the groups so each _group_ is balanced O(m)
   add that _night_ to _superList_
   
   
The time complexity of this algorithm that runs the minimum amount of iterations is O(n^3), which is the time complexity of our 
algorithm. When we generate the _peopleUnvisited_ map values, this takes O(n^2) time. After finding the approximate time complexity 
of each nested loop, we are left with the time complexity of O(n^3 + n^2m + nm + m) which is then reduced to O(n^3) at worst. 

We ran into several difficulties when creating the algorithm for this project. Our first attempt at an algorithm was too focused on
representing the data conceptually as a matrix rather than a map. Because of this, we attampted to manipulate the matrix and have
each team visit each host through a process of picking a host and having the subsequent created groups iterate, shift, and rotate 
to visit each host. However, this was both far too complex and failed to generate a full clique. After realizing that manipulating a
conceptual matrix of the data would be both inefficient as well as incomplete, we decided to represent the data with maps and queues.
By utilizing these data structures and looking for intersectios between maps, we managed to generate a full clique efficiently. We 
still ran into several difficulties during our revised approach, particularly involving changes to the ideal group size. COME BACK TO
THIS SECTION :)

The following are screenshots of our program running:

The following is a link to a YouTube video of our program running:

The following are the set of sets created by our program for each file:
group1.txt:


group2.txt:


group3.txt:


    
