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
*Write the reflection about getting the small groups in the minimum number of iterations, etc.*


