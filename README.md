# Creating Community Small Groups
**A work by: Dr. Carlos Arias, Elizabeth Myers, and Chandler Stevens**

**CSC 3430: Algorithm Analysis and Design**

## Table of Contents  
- [Introduction](https://github.com/csc3430-winter2020/community-small-groups-palpateam#introduction)
- [Description](https://github.com/csc3430-winter2020/community-small-groups-palpateam#description)
- [Requirements](https://github.com/csc3430-winter2020/community-small-groups-palpateam#requirements)
- [User Manual](https://github.com/csc3430-winter2020/community-small-groups-palpateam#user-manual)
- [Reflection](https://github.com/csc3430-winter2020/community-small-groups-palpateam#reflection)

## Introduction

The following information describes our algorithm for allocating church members to small groups. We begin with a description of the problem that we are solving, along with several constraints. Then, we describe the software and package requirements needed to run our program. Next, we provide a user manual that explains how to launch and use the program with example screenshots and a YouTube video tutorial. We include a reflection of the steps we took to determine the ideal algorithm and subsequently the implementation of our algorithm as well as the time complexities of each. We also discuss the challenges we overcame during development. Finally, we include example outputs for each of the three text files provided in this repository. 

## Description

A church community would like to form small groups of people for Bible studies. These Bible studies will serve to explore and share deep theological discussions between community members. In order to facilitate relational connections between all members of this community, every person should visit every other member's house. Each person hosting a small group meeting at their house is  considered a host. 

The purpose of this project is to allocate people within a church community into ideally sized small groups. The program created for this project will read a list of people from a text file and assign these people to groups of the desired size. The output of this  project is a list of lists. Each list will have a list of that night's hosts and their guests. An additional constraint of this project is that if a person is married, then that person must always be placed in the same small group that their spouse is placed in. An additional contraint that we added to our program is minimizing the number of times that a person/couple must host multiple consecutive nights. 

In the text file each individual person is followed by a new line and each married couple is joined with a comma and followed by a new line.

The programming language that we chose for our project was Python 3. We chose this language because it has supported graph libraries (such as networkx) and our group decided we wanted to familiarize ourselves more with a scripting language.


## Requirements
The required Python version for our program is Python 3.7 or up. When installing Python 3, the user must choose to install all the optional features, namely the _pip_ package installer.  

The required Python libraries for our program include: 
- networkx (utilized to create a graph data structure)
- matplotlib (utilized to display and animate a graph in our program)
- numpy (utilized to support matplotlib)

The first step of our program will attempt to install these required Python libraries for the user. Therefore, the user should not need to manually install these requirements and the user should only need to install the Python 3 programming language. 

## User Manual

1. Once you have cloned the repo, unzip or extract the files as necessary.
2. Then, inside the folder, double-click the "Small-Group.py" file to run the program.
3. The program will prompt you for a filename, so enter a group textfile (e.g. "group1.txt").
4. Next, the program will prompt you for an ideal group size, which should be a positive integer.
5. The program will ask if you would like to display the graph animation or simply run the algorithm without an animation.
a. Type and enter "y" to display the graph animation or "n" to **not** display the graph animation
6. Then, the program will immediately begin the algorithm while displaying its progress.
7. Finally, once the program has completed, the set of sets of each group for each night will be displayed.

### The following is a link to a YouTube video tutorial:

_The video walks through the installation process and shows a demo of our program running._

https://youtu.be/KTWziXdUNFM

### The following are screenshots of our program running:

_Click an image to view a close-up, scrollable version._

#### group1.txt with m = 4:

![Group1](/screenshots/Screenshot-group1-4.png)

#### group2.txt with m = 4:

![Group2](/screenshots/Screenshot-group2-4.png)

#### group3.txt with m = 4:

![Group3](/screenshots/Screenshot-group3-4.png)


## Reflection
If we were to find the set of sets of teams in the minimum amount of iterations, the algorithm would only assign people to fill a group if they have never visited that host before. For an example of this, given a list of n=16 people with an ideal group size of m=4, there would be 4 hosts with each host receiving 3 new guests each night. Each night would then have 12 new edges being assigned. The total number of edges in the representational graph would be (n x (n-1)) since each person does not need to visit themselves. In this example, the total number of edges would be 16 x 15 = 240 edges, so for 240 edges with 12 edges added per night, there would be a minimum of 20 iterations/nights. The time complexity of this ideal algorithm, which runs the minimum amount of iterations, would be O(n<sup>2</sup>). This is because for each person n, there must be (n-1) persons assigned to them after the algorithm completes. 

Though the optimal solution for this problem would choose hosts regardless if they have hosted the previous night or not, we decided to be realistic with a real-life situation in our algorithm in which we would not assign people as hosts multiple nights in a row. Thus, we tried to ensure that if people hosted the night before, they are not a host the following night, if possible. This caused our number of iterations to be slightly greater than that of the optimal solution, which has the minimum amout of iterations. In order to find the set of sets of teams in the minimum amount of iterations, we implemented an algorithm that runs in O(n<sup>3</sup>) time.

We initialize the algorithm in the following way: 
1. We read the text file and for each team, we added them to a map _peopleNumbers_ with the values being 1 if it is a single person and 2 if there is a married couple. 
2. We then made another map _peopleUnivisited_ that generates a list of all the people who have not visited each host. 
3. We also created a directed graph initialized with the number of teams, so each team had their own node. 
4. We determined how many groups there should be by doing integer division between _n_ (the number of individuals) divided by _m_ (the ideal group size entered by the user). 
5. We also initialized a list _superList_ that will contain all of the sub-lists, which will be returned as the results to be outputted. 
6. The last items we set up was a list of hosts _hostNames_ who hosted the previous night. 

Our algorithm utilizes the following logic:
```
//team refers to either a couple or a single person to add
while there are still people who have not visited every host's house
  make a deep copy of the map of unvisited people called "people"
  initialize a sublist to store the groups for this night called "night"
  for each group to meet at a host's house (counter-controlled loop from i=0 to i="n/m"-1)
    initialize a list called "group" for that group
    select a host based on which team has been visited the least that is not in "hostNames"
    add host to "group" and to "hostNames"
    find the intersection between "peopleUnvisited" of that host and the "people" who have not been assigned
      if the host fills the ideal group size or the size of the host = "m"
        add a guest anyways and draw an edge
    while "group" is not filled and less than the ideal group size "m" and there are still teams to add 
      find the intersection between "peopleUnvisited" of that host and the "people" who have not been assigned
      if adding a team will overflow a group
        select a team anyway
      if there is a team in the intersection
        select a guest that will fit in "group", trying to add couples first before trying to add singles
      if the intersection is empty but "people" is not empty
        select a team anyways to fill "group"
      if a team was selected
        add the selected team to "group" and remove them from their host's "peopleUnvisited" list and "people"
        draw an edge from that guest node to the host node they were added to
    add the "group" to "night" 
   if there is anyone left in "people"
    distribute them across all the groups so each "group" is balanced
   add that "night" to "superList"
```

When we generate the _peopleUnvisited_ map values, this takes only O(n<sup>2</sup>) time. But after finding the approximate time
complexity for the iterative code segments, we are left with a worst case time complexity reduced to O(n<sup>3</sup>). The iterative
code segments are as follows:
```
1. While there are still teams who have not visited every other team 
    2. While there are still groups to create
        3. Create a group, select a host, and iteratively select guest(s) for that group
```
We ran into several difficulties when creating the algorithm for this project. Our first attempt at an algorithm was too focused on representing the data conceptually as a matrix rather than a map. Because of this, we attempted to manipulate the matrix by having each team visit each host through a process of picking a host and having the subsequent created groups iterate, shift, and rotate to visit each host. However, this was both far too complex and failed to generate a full clique. After realizing that manipulating a conceptual matrix of the data would be both inefficient as well as incomplete, we decided to represent the data with maps. By utilizing these data structures and looking for intersections between sets of the map keys, we managed to generate a full clique efficiently. 

We discovered other difficulties during our revised approach, particularly involving host selection. In order to ensure that a team was not a host two nights in a row, we made a list of the teams who hosted the night before. Then, when picking a new host for the current night, the new host could not be in the previous host list. However, there were still incorrect host selections, so we overcame this  issue by selecting a host from _previousHost_ as necessary as long as that host was not a current host. 

Another issue we ran into was assigning couples to groups that already had the ideal size filled, while not making any of the groups too unbalanced. We prevailed over this difficulty by implementing a 'catch-all' that would iteratively distribute any unassigned  guests to the smallest group, starting with any unassigned couples.

### The following are the set of sets created by our program for each file:

#### group1.txt with m = 4:
```
[
[[4, 4, 4, 4], ['Finn', 'Anakin + Padme', 'Rey'], ['Qui-Gon', 'Leia + Han', 'Jabba'], ['Sidious', 'Poe', 'Zorii', 'C-3PO'], ['R2-D2', 'Ben', 'Yoda', 'BB-8']],
[[4, 4, 4, 4], ['Rey', 'Anakin + Padme', 'Finn'], ['Jabba', 'Leia + Han', 'Qui-Gon'], ['Poe', 'Sidious', 'Zorii', 'C-3PO'], ['Ben', 'R2-D2', 'Yoda', 'BB-8']],
[[4, 4, 4, 4], ['Anakin + Padme', 'Leia + Han'], ['Zorii', 'Finn', 'Rey', 'Qui-Gon'], ['C-3PO', 'Jabba', 'Sidious', 'Poe'], ['Yoda', 'R2-D2', 'Ben', 'BB-8']],
[[4, 4, 4, 4], ['Leia + Han', 'Anakin + Padme'], ['BB-8', 'Finn', 'Rey', 'Qui-Gon'], ['Jabba', 'Sidious', 'Poe', 'Zorii'], ['R2-D2', 'C-3PO', 'Ben', 'Yoda']],
[[4, 4, 4, 4], ['Anakin + Padme', 'Finn', 'Rey'], ['Qui-Gon', 'Sidious', 'Poe', 'Zorii'], ['Ben', 'Leia + Han', 'Jabba'], ['C-3PO', 'R2-D2', 'Yoda', 'BB-8']],
[[4, 4, 4, 4], ['Leia + Han', 'Finn', 'Rey'], ['Sidious', 'Anakin + Padme', 'Qui-Gon'], ['Poe', 'Jabba', 'R2-D2', 'Ben'], ['Zorii', 'C-3PO', 'Yoda', 'BB-8']],
[[4, 4, 4, 4], ['Finn', 'Leia + Han', 'Qui-Gon'], ['Rey', 'Jabba', 'Sidious', 'Poe'], ['Anakin + Padme', 'Zorii', 'C-3PO'], ['Yoda', 'Ben', 'R2-D2', 'BB-8']],
[[4, 4, 4, 4], ['Leia + Han', 'Qui-Gon', 'Jabba'], ['BB-8', 'Anakin + Padme', 'Sidious'], ['R2-D2', 'Poe', 'Zorii', 'Finn'], ['Ben', 'C-3PO', 'Rey', 'Yoda']],
[[4, 4, 4, 4], ['Yoda', 'Anakin + Padme', 'Finn'], ['Rey', 'Leia + Han', 'Qui-Gon'], ['Jabba', 'R2-D2', 'Ben', 'C-3PO'], ['Sidious', 'BB-8', 'Poe', 'Zorii']],
[[4, 4, 4, 4], ['Finn', 'Jabba', 'Sidious', 'Poe'], ['Qui-Gon', 'Anakin + Padme', 'Rey'], ['Leia + Han', 'Zorii', 'C-3PO'], ['BB-8', 'R2-D2', 'Ben', 'Yoda']],
[[4, 4, 4, 4], ['Anakin + Padme', 'Qui-Gon', 'Jabba'], ['Yoda', 'Leia + Han', 'Rey'], ['Sidious', 'R2-D2', 'Ben', 'Finn'], ['Poe', 'BB-8', 'C-3PO', 'Zorii']],
[[4, 4, 4, 4], ['Zorii', 'Anakin + Padme', 'Jabba'], ['C-3PO', 'Leia + Han', 'Qui-Gon'], ['Finn', 'R2-D2', 'Ben', 'Yoda'], ['Rey', 'BB-8', 'Sidious', 'Poe']],
[[4, 4, 4, 4], ['Qui-Gon', 'Finn', 'C-3PO', 'R2-D2'], ['Anakin + Padme', 'Sidious', 'Ben'], ['Leia + Han', 'Poe', 'Yoda'], ['Jabba', 'Rey', 'BB-8', 'Zorii']],
[[4, 4, 4, 4], ['Poe', 'Anakin + Padme', 'Finn'], ['Yoda', 'Qui-Gon', 'Jabba', 'Zorii'], ['R2-D2', 'Leia + Han', 'Sidious'], ['Ben', 'Rey', 'C-3PO', 'BB-8']],
[[4, 4, 4, 4], ['Rey', 'Zorii', 'R2-D2', 'Ben'], ['C-3PO', 'Anakin + Padme', 'Finn'], ['BB-8', 'Leia + Han', 'Jabba'], ['Sidious', 'Yoda', 'Qui-Gon', 'Poe']],
[[4, 4, 4, 4], ['Ben', 'Anakin + Padme', 'Finn'], ['Zorii', 'Leia + Han', 'R2-D2'], ['Poe', 'Qui-Gon', 'Yoda', 'Rey'], ['Jabba', 'Sidious', 'C-3PO', 'BB-8']],
[[4, 4, 4, 4], ['Anakin + Padme', 'R2-D2', 'Poe'], ['Leia + Han', 'Ben', 'Sidious'], ['Finn', 'Zorii', 'C-3PO', 'BB-8'], ['Qui-Gon', 'Yoda', 'Rey', 'Jabba']],
[[4, 4, 4, 4], ['R2-D2', 'Anakin + Padme', 'Qui-Gon'], ['Ben', 'Poe', 'Zorii', 'Sidious'], ['Jabba', 'Yoda', 'Finn', 'Rey'], ['C-3PO', 'Leia + Han', 'BB-8']],
[[4, 4, 4, 4], ['Sidious', 'Leia + Han', 'Jabba'], ['Zorii', 'Ben', 'Poe', 'Rey'], ['Yoda', 'C-3PO', 'Anakin + Padme'], ['BB-8', 'Qui-Gon', 'Finn', 'R2-D2']],
[[4, 4, 4, 4], ['C-3PO', 'Ben', 'Zorii', 'Rey'], ['Qui-Gon', 'BB-8', 'Leia + Han'], ['Anakin + Padme', 'Yoda', 'Sidious'], ['R2-D2', 'Jabba', 'Finn', 'Poe']],
[[4, 4, 4, 4], ['BB-8', 'Poe', 'Zorii', 'C-3PO'], ['Rey', 'Yoda', 'Leia + Han'], ['Ben', 'Qui-Gon', 'Anakin + Padme'], ['Jabba', 'Sidious', 'Finn', 'R2-D2']],
[[4, 4, 4, 4], ['Leia + Han', 'R2-D2', 'BB-8'], ['Yoda', 'Poe', 'Sidious', 'Rey'], ['Qui-Gon', 'Ben', 'Anakin + Padme'], ['Zorii', 'Finn', 'Jabba', 'C-3PO']],
[[4, 4, 4, 4], ['Rey', 'C-3PO', 'Leia + Han'], ['Jabba', 'Anakin + Padme', 'Ben'], ['Sidious', 'Qui-Gon', 'Yoda', 'Finn'], ['R2-D2', 'Poe', 'BB-8', 'Zorii']],
[[4, 4, 4, 4], ['Anakin + Padme', 'BB-8', 'Rey'], ['Poe', 'Leia + Han', 'Ben'], ['Zorii', 'Sidious', 'Qui-Gon', 'Yoda'], ['C-3PO', 'Finn', 'Jabba', 'R2-D2']],
[[4, 4, 4, 4], ['Sidious', 'Rey', 'Leia + Han'], ['R2-D2', 'Anakin + Padme', 'Ben'], ['Finn', 'Qui-Gon', 'Yoda', 'Poe'], ['Jabba', 'C-3PO', 'BB-8', 'Zorii']],
[[4, 4, 4, 4], ['Rey', 'Leia + Han', 'Ben'], ['Qui-Gon', 'Anakin + Padme', 'Yoda'], ['Poe', 'Sidious', 'Finn', 'Jabba'], ['Zorii', 'R2-D2', 'C-3PO', 'BB-8']],
[[4, 4, 4, 4], ['R2-D2', 'Rey', 'Leia + Han'], ['Finn', 'Anakin + Padme', 'Ben'], ['Jabba', 'Qui-Gon', 'Yoda', 'Sidious'], ['C-3PO', 'Poe', 'BB-8', 'Zorii']]
]
```
#### group2.txt with m = 4:
```
[
[[5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Owen + Beru', 'Mace'], ['Obi-Wan', 'Bail + Breha', 'Rey'], ['Hux', 'Anakin + Padme', 'Finn'], ['Yoda', 'Leia + Han', 'R2-D2'], ['Watto', 'Boba', 'Phasma', 'Poe'], ['Qui-Gon', 'Jabba', 'Zorii', 'Jango'], ['Ben', 'C-3PO', 'BB-8', 'Sidious']],
[[5, 4, 4, 4, 4, 4, 4], ['BB-8', 'Shmi + Cliegg', 'Rey', 'Watto'], ['Finn', 'Owen + Beru', 'Sidious'], ['R2-D2', 'Bail + Breha', 'Obi-Wan'], ['Boba', 'Anakin + Padme', 'Hux'], ['Phasma', 'Leia + Han', 'Yoda'], ['Poe', 'Mace', 'Qui-Gon', 'Ben'], ['C-3PO', 'Jabba', 'Zorii', 'Jango']],
[[5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Shmi + Cliegg', 'Ben'], ['Jabba', 'Owen + Beru', 'Rey'], ['Zorii', 'Bail + Breha', 'Finn'], ['Jango', 'Anakin + Padme', 'Obi-Wan'], ['Mace', 'R2-D2', 'Hux', 'Boba'], ['Sidious', 'Phasma', 'Yoda', 'Poe'], ['Watto', 'C-3PO', 'BB-8', 'Qui-Gon']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Shmi + Cliegg', 'Jango'], ['Anakin + Padme', 'Owen + Beru'], ['Rey', 'Leia + Han', 'Finn'], ['Obi-Wan', 'R2-D2', 'Hux', 'Boba'], ['Phasma', 'Poe', 'Qui-Gon', 'Mace'], ['Yoda', 'Jabba', 'Zorii', 'Ben'], ['C-3PO', 'BB-8', 'Sidious', 'Watto']],
[[5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Shmi + Cliegg', 'Watto'], ['Finn', 'Bail + Breha', 'Rey'], ['R2-D2', 'Anakin + Padme', 'Hux'], ['Boba', 'Leia + Han', 'Obi-Wan'], ['Zorii', 'Phasma', 'Yoda', 'Poe'], ['Jabba', 'Mace', 'Qui-Gon', 'Ben'], ['Jango', 'C-3PO', 'BB-8', 'Sidious']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Shmi + Cliegg', 'Watto'], ['Leia + Han', 'Owen + Beru'], ['Hux', 'Bail + Breha', 'Obi-Wan'], ['Rey', 'R2-D2', 'Boba', 'Phasma'], ['Mace', 'Finn', 'Yoda', 'Jabba'], ['Poe', 'Zorii', 'Jango', 'C-3PO'], ['Qui-Gon', 'BB-8', 'Sidious', 'Ben']],
[[5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Bail + Breha', 'Mace'], ['Owen + Beru', 'Anakin + Padme'], ['Ben', 'Leia + Han', 'Finn'], ['Sidious', 'Obi-Wan', 'R2-D2', 'Hux'], ['BB-8', 'Boba', 'Phasma', 'Yoda'], ['Zorii', 'Qui-Gon', 'Jango', 'Watto'], ['Jabba', 'C-3PO', 'Poe', 'Rey']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Owen + Beru', 'BB-8'], ['Leia + Han', 'Anakin + Padme'], ['Finn', 'Shmi + Cliegg', 'Obi-Wan'], ['R2-D2', 'Boba', 'Phasma', 'Yoda'], ['Hux', 'Poe', 'Qui-Gon', 'Mace'], ['Rey', 'Jabba', 'Zorii', 'Ben'], ['Jango', 'Watto', 'Sidious', 'C-3PO']],
[[5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Anakin + Padme', 'BB-8'], ['Owen + Beru', 'Bail + Breha'], ['Boba', 'Finn', 'R2-D2', 'Phasma'], ['Obi-Wan', 'Leia + Han', 'Yoda'], ['Ben', 'Hux', 'Poe', 'Qui-Gon'], ['Watto', 'Zorii', 'Jango', 'Jabba'], ['C-3PO', 'Rey', 'Mace', 'Sidious']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Bail + Breha', 'Ben'], ['Leia + Han', 'Finn', 'Obi-Wan'], ['Phasma', 'Shmi + Cliegg', 'R2-D2'], ['Yoda', 'Owen + Beru', 'Hux'], ['Poe', 'Boba', 'Jabba', 'Rey'], ['Qui-Gon', 'C-3PO', 'Mace', 'Watto'], ['BB-8', 'Zorii', 'Sidious', 'Jango']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Anakin + Padme', 'C-3PO'], ['Owen + Beru', 'Leia + Han'], ['Shmi + Cliegg', 'Finn', 'Obi-Wan'], ['Jango', 'R2-D2', 'Hux', 'Boba'], ['Mace', 'Phasma', 'Poe', 'Qui-Gon'], ['Sidious', 'Zorii', 'Ben', 'Watto'], ['Jabba', 'Yoda', 'BB-8', 'Rey']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Leia + Han', 'Jango'], ['Finn', 'R2-D2', 'Hux', 'Boba'], ['Obi-Wan', 'Shmi + Cliegg', 'Phasma'], ['Yoda', 'Bail + Breha', 'Poe'], ['Zorii', 'Owen + Beru', 'Ben'], ['C-3PO', 'Qui-Gon', 'Rey', 'Mace'], ['BB-8', 'Jabba', 'Sidious', 'Watto']],
[[5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Finn', 'Obi-Wan', 'Watto'], ['Leia + Han', 'Bail + Breha'], ['Shmi + Cliegg', 'R2-D2', 'Hux'], ['Boba', 'Yoda', 'Poe', 'Qui-Gon'], ['Phasma', 'Anakin + Padme', 'Jabba'], ['Ben', 'Zorii', 'Rey', 'Jango'], ['Sidious', 'C-3PO', 'BB-8', 'Mace']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Leia + Han', 'Watto'], ['R2-D2', 'Shmi + Cliegg', 'Finn'], ['Hux', 'Owen + Beru', 'Boba'], ['Anakin + Padme', 'Obi-Wan', 'Phasma'], ['Rey', 'Yoda', 'Poe', 'Qui-Gon'], ['Jango', 'Zorii', 'Jabba', 'Mace'], ['C-3PO', 'Ben', 'Sidious', 'BB-8']],
[[5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'R2-D2', 'Hux', 'BB-8'], ['Owen + Beru', 'Boba', 'Phasma'], ['Shmi + Cliegg', 'Yoda', 'Poe'], ['Finn', 'Anakin + Padme', 'Qui-Gon'], ['Obi-Wan', 'Mace', 'Zorii', 'Jango'], ['Jabba', 'Bail + Breha', 'Sidious'], ['Watto', 'Rey', 'Ben', 'C-3PO']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Finn', 'Obi-Wan', 'Jango'], ['R2-D2', 'Owen + Beru', 'Rey'], ['Hux', 'Shmi + Cliegg', 'Phasma'], ['Yoda', 'Anakin + Padme', 'Boba'], ['Poe', 'Leia + Han', 'BB-8'], ['Qui-Gon', 'Ben', 'Mace', 'Sidious'], ['C-3PO', 'Jabba', 'Zorii', 'Watto']],
[[5, 4, 4, 4, 4, 4, 4], ['Phasma', 'Bail + Breha', 'Finn', 'Watto'], ['Anakin + Padme', 'R2-D2', 'Hux'], ['Owen + Beru', 'Yoda', 'Poe'], ['Mace', 'Shmi + Cliegg', 'Obi-Wan'], ['Boba', 'Zorii', 'Jango', 'Ben'], ['Leia + Han', 'Jabba', 'Qui-Gon'], ['BB-8', 'C-3PO', 'Rey', 'Sidious']],
[[5, 4, 4, 4, 4, 4, 4], ['Qui-Gon', 'Shmi + Cliegg', 'Finn', 'BB-8'], ['Zorii', 'Anakin + Padme', 'Obi-Wan'], ['Bail + Breha', 'R2-D2', 'Hux'], ['C-3PO', 'Leia + Han', 'Boba'], ['Yoda', 'Phasma', 'Jango', 'Watto'], ['Jabba', 'Owen + Beru', 'Rey'], ['Poe', 'Sidious', 'Ben', 'Mace']],
[[5, 4, 4, 4, 4, 4, 4], ['BB-8', 'Bail + Breha', 'Finn', 'Phasma'], ['Shmi + Cliegg', 'Leia + Han'], ['Watto', 'Anakin + Padme', 'Obi-Wan'], ['R2-D2', 'Poe', 'Qui-Gon', 'Jabba'], ['Hux', 'Yoda', 'Zorii', 'Jango'], ['Ben', 'Owen + Beru', 'Boba'], ['Rey', 'C-3PO', 'Sidious', 'Mace']],
[[5, 4, 4, 4, 4, 4, 4], ['Finn', 'Leia + Han', 'Phasma', 'BB-8'], ['Jabba', 'Shmi + Cliegg', 'Obi-Wan'], ['Qui-Gon', 'Bail + Breha', 'R2-D2'], ['Anakin + Padme', 'Boba', 'Yoda'], ['Owen + Beru', 'Hux', 'Zorii'], ['Mace', 'Jango', 'Ben', 'Watto'], ['C-3PO', 'Poe', 'Rey', 'Sidious']],
[[5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Boba', 'Jabba', 'Watto'], ['Obi-Wan', 'Owen + Beru', 'Finn'], ['Phasma', 'Hux', 'Zorii', 'Jango'], ['Poe', 'Bail + Breha', 'Yoda'], ['Leia + Han', 'Anakin + Padme'], ['Sidious', 'Rey', 'Qui-Gon', 'Ben'], ['BB-8', 'R2-D2', 'Mace', 'C-3PO']],
[[5, 4, 4, 4, 4, 4, 4], ['Zorii', 'Shmi + Cliegg', 'R2-D2', 'BB-8'], ['Bail + Breha', 'Boba', 'Phasma'], ['Jango', 'Leia + Han', 'Finn'], ['Qui-Gon', 'Anakin + Padme', 'Obi-Wan'], ['Ben', 'Yoda', 'Jabba', 'Mace'], ['Watto', 'Owen + Beru', 'Sidious'], ['C-3PO', 'Hux', 'Rey', 'Poe']],
[[5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Boba', 'Phasma', 'Jango'], ['Jabba', 'Anakin + Padme', 'Finn'], ['Owen + Beru', 'R2-D2', 'Qui-Gon'], ['Obi-Wan', 'Poe', 'Ben', 'C-3PO'], ['Hux', 'Rey', 'BB-8', 'Sidious'], ['Yoda', 'Shmi + Cliegg', 'Mace'], ['Zorii', 'Bail + Breha', 'Watto']],
[[5, 4, 4, 4, 4, 4, 4], ['Boba', 'Shmi + Cliegg', 'Watto', 'Qui-Gon'], ['Anakin + Padme', 'Bail + Breha'], ['Finn', 'Yoda', 'Poe', 'Zorii'], ['R2-D2', 'Leia + Han', 'Jango'], ['C-3PO', 'Owen + Beru', 'Phasma'], ['Rey', 'Obi-Wan', 'BB-8', 'Hux'], ['Sidious', 'Jabba', 'Ben', 'Mace']],
[[5, 4, 4, 4, 4, 4, 4], ['Poe', 'Shmi + Cliegg', 'Finn', 'Boba'], ['Bail + Breha', 'Yoda', 'Qui-Gon'], ['Jango', 'Owen + Beru', 'Phasma'], ['Mace', 'Anakin + Padme', 'Rey'], ['Zorii', 'Leia + Han', 'Hux'], ['Watto', 'R2-D2', 'Ben', 'Obi-Wan'], ['BB-8', 'Sidious', 'Jabba', 'C-3PO']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Finn', 'Poe', 'Hux'], ['Shmi + Cliegg', 'Phasma', 'Qui-Gon'], ['Boba', 'Bail + Breha', 'BB-8'], ['Sidious', 'Leia + Han', 'Jango'], ['Jabba', 'Owen + Beru', 'Watto'], ['R2-D2', 'C-3PO', 'Zorii', 'Mace'], ['Yoda', 'Rey', 'Obi-Wan', 'Ben']],
[[5, 4, 4, 4, 4, 4, 4], ['BB-8', 'Anakin + Padme', 'Obi-Wan', 'Watto'], ['Leia + Han', 'Yoda', 'Poe'], ['Phasma', 'Owen + Beru', 'Boba'], ['Qui-Gon', 'Rey', 'Hux', 'Ben'], ['Bail + Breha', 'Zorii', 'Sidious'], ['Jango', 'Shmi + Cliegg', 'Mace'], ['C-3PO', 'Finn', 'R2-D2', 'Jabba']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Jabba', 'Qui-Gon', 'Hux'], ['Owen + Beru', 'Jango', 'Ben'], ['Poe', 'Obi-Wan', 'Phasma', 'Watto'], ['Mace', 'Bail + Breha', 'Zorii'], ['Shmi + Cliegg', 'C-3PO', 'Rey'], ['Finn', 'Leia + Han', 'Yoda'], ['Boba', 'Sidious', 'R2-D2', 'BB-8']],
[[4, 4, 4, 4, 4, 4, 5], ['Jabba', 'Leia + Han', 'R2-D2'], ['Ben', 'Shmi + Cliegg', 'Obi-Wan'], ['Watto', 'Bail + Breha', 'Finn'], ['Hux', 'C-3PO', 'Anakin + Padme'], ['Phasma', 'Rey', 'BB-8', 'Sidious'], ['Jango', 'Yoda', 'Poe', 'Qui-Gon'], ['Zorii', 'Boba', 'Mace', 'Owen + Beru']],
[[5, 4, 4, 4, 4, 4, 4], ['BB-8', 'Leia + Han', 'Hux', 'Phasma'], ['Finn', 'Ben', 'Jango', 'C-3PO'], ['Obi-Wan', 'Anakin + Padme', 'Jabba'], ['Qui-Gon', 'Owen + Beru', 'Boba'], ['Rey', 'Shmi + Cliegg', 'Watto'], ['Sidious', 'Bail + Breha', 'Mace'], ['Yoda', 'Poe', 'R2-D2', 'Zorii']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Zorii', 'C-3PO', 'Jango'], ['Leia + Han', 'Rey', 'Sidious'], ['Owen + Beru', 'BB-8', 'Jabba'], ['Hux', 'Watto', 'R2-D2', 'Ben'], ['Boba', 'Mace', 'Shmi + Cliegg'], ['Bail + Breha', 'Poe', 'Obi-Wan'], ['Phasma', 'Qui-Gon', 'Yoda', 'Finn']],
[[5, 4, 4, 4, 4, 4, 4], ['Watto', 'Shmi + Cliegg', 'Yoda', 'Jango'], ['Jabba', 'Hux', 'Boba', 'Phasma'], ['Ben', 'Anakin + Padme', 'R2-D2'], ['C-3PO', 'Bail + Breha', 'Obi-Wan'], ['Sidious', 'Owen + Beru', 'Finn'], ['Mace', 'Leia + Han', 'BB-8'], ['Poe', 'Rey', 'Qui-Gon', 'Zorii']],
[[5, 4, 4, 4, 4, 4, 4], ['Yoda', 'Finn', 'C-3PO', 'Qui-Gon', 'Phasma'], ['BB-8', 'Owen + Beru', 'Poe'], ['Shmi + Cliegg', 'Zorii', 'Sidious'], ['Obi-Wan', 'Watto', 'Leia + Han'], ['R2-D2', 'Ben', 'Anakin + Padme'], ['Boba', 'Rey', 'Jabba', 'Mace'], ['Bail + Breha', 'Jango', 'Hux']],
[[5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'C-3PO', 'Zorii', 'Hux'], ['Poe', 'Anakin + Padme', 'R2-D2'], ['Qui-Gon', 'Owen + Beru', 'Phasma'], ['Rey', 'Bail + Breha', 'Jango'], ['Finn', 'Jabba', 'Mace', 'Watto'], ['Sidious', 'Shmi + Cliegg', 'Boba'], ['Ben', 'Obi-Wan', 'Yoda', 'BB-8']],
[[5, 4, 4, 4, 4, 4, 4], ['Zorii', 'C-3PO', 'Sidious', 'Rey', 'Hux'], ['Bail + Breha', 'Jabba', 'Ben'], ['Owen + Beru', 'Mace', 'Obi-Wan'], ['Anakin + Padme', 'BB-8', 'Qui-Gon'], ['R2-D2', 'Watto', 'Leia + Han'], ['Phasma', 'Shmi + Cliegg', 'Yoda'], ['Jango', 'Finn', 'Poe', 'Boba']],
[[5, 4, 4, 4, 4, 4, 4], ['Obi-Wan', 'Qui-Gon', 'BB-8', 'Sidious', 'Jango'], ['Watto', 'Leia + Han', 'Mace'], ['Ben', 'Bail + Breha', 'Phasma'], ['C-3PO', 'Anakin + Padme', 'Yoda'], ['Hux', 'Shmi + Cliegg', 'Jabba'], ['Boba', 'Owen + Beru', 'Rey'], ['Poe', 'Finn', 'R2-D2', 'Zorii']],
[[5, 4, 4, 4, 4, 4, 4], ['Phasma', 'C-3PO', 'Obi-Wan', 'Ben', 'Hux'], ['Qui-Gon', 'Leia + Han', 'Yoda'], ['Jango', 'Bail + Breha', 'Rey'], ['Owen + Beru', 'Sidious', 'Mace'], ['Anakin + Padme', 'Shmi + Cliegg'], ['R2-D2', 'BB-8', 'Finn', 'Poe'], ['Jabba', 'Zorii', 'Watto', 'Boba']],
[[5, 4, 4, 4, 4, 4, 4], ['Mace', 'Owen + Beru', 'C-3PO', 'Phasma'], ['Shmi + Cliegg', 'Jango', 'Ben'], ['Rey', 'Anakin + Padme', 'Obi-Wan'], ['Yoda', 'BB-8', 'Sidious', 'Qui-Gon'], ['Poe', 'Hux', 'Leia + Han'], ['Bail + Breha', 'Finn', 'Jabba'], ['Boba', 'R2-D2', 'Zorii', 'Watto']],
[[5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Rey', 'Sidious', 'Phasma'], ['BB-8', 'Qui-Gon', 'Ben', 'Mace'], ['Leia + Han', 'Watto', 'Obi-Wan'], ['Owen + Beru', 'C-3PO', 'Yoda'], ['R2-D2', 'Shmi + Cliegg', 'Finn'], ['Hux', 'Bail + Breha', 'Poe'], ['Jabba', 'Jango', 'Zorii', 'Boba']],
[[5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Rey', 'Mace', 'Phasma'], ['Boba', 'C-3PO', 'Leia + Han'], ['Poe', 'Owen + Beru', 'Ben'], ['Qui-Gon', 'Anakin + Padme', 'Obi-Wan'], ['Zorii', 'Jabba', 'Shmi + Cliegg'], ['Jango', 'Yoda', 'Sidious', 'Finn'], ['Watto', 'Hux', 'R2-D2', 'BB-8']],
[[5, 4, 4, 4, 4, 4, 4], ['R2-D2', 'Sidious', 'Leia + Han', 'Boba'], ['Hux', 'Anakin + Padme', 'Rey'], ['Ben', 'Watto', 'Shmi + Cliegg'], ['C-3PO', 'Bail + Breha', 'Mace'], ['Owen + Beru', 'Obi-Wan', 'Qui-Gon'], ['Finn', 'Yoda', 'Poe', 'Jabba'], ['Phasma', 'BB-8', 'Zorii', 'Jango']],
[[5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Mace', 'Rey', 'Phasma'], ['Qui-Gon', 'Poe', 'Anakin + Padme'], ['Jango', 'Ben', 'Shmi + Cliegg'], ['Sidious', 'Bail + Breha', 'Obi-Wan'], ['Boba', 'Owen + Beru', 'Yoda'], ['Zorii', 'Finn', 'Jabba', 'R2-D2'], ['BB-8', 'C-3PO', 'Watto', 'Hux']],
[[5, 4, 4, 4, 4, 4, 4], ['Hux', 'Leia + Han', 'Rey', 'Boba'], ['C-3PO', 'Shmi + Cliegg', 'Ben'], ['Anakin + Padme', 'Mace', 'Obi-Wan'], ['Owen + Beru', 'Bail + Breha'], ['Finn', 'Qui-Gon', 'Yoda', 'Sidious'], ['R2-D2', 'Poe', 'Jabba', 'BB-8'], ['Phasma', 'Zorii', 'Watto', 'Jango']],
[[5, 4, 4, 4, 4, 4, 4], ['Rey', 'Owen + Beru', 'Ben', 'Phasma'], ['Sidious', 'Anakin + Padme', 'Mace'], ['Shmi + Cliegg', 'Leia + Han'], ['Obi-Wan', 'Bail + Breha', 'Qui-Gon'], ['Boba', 'Yoda', 'Finn', 'Poe'], ['Zorii', 'Jabba', 'R2-D2', 'C-3PO'], ['BB-8', 'Watto', 'Jango', 'Hux']],
[[5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Rey', 'Ben', 'Boba'], ['Mace', 'Sidious', 'Leia + Han'], ['Finn', 'Anakin + Padme', 'Obi-Wan'], ['R2-D2', 'Shmi + Cliegg', 'Qui-Gon'], ['Hux', 'Bail + Breha', 'Yoda'], ['Phasma', 'Poe', 'Jabba', 'C-3PO'], ['Jango', 'BB-8', 'Zorii', 'Watto']]
]
```
#### group3.txt with m = 4:
```
[
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Shmi + Cliegg', 'Phasma', 'Mace'], ['BB-8', 'Owen + Beru', 'Sidious', 'Poe'], ['Ben', 'Leia + Han', 'Watto'], ['Grevious', 'Bail + Breha', 'Jabba'], ['Luke', 'Anakin + Padme', 'Zorii'], ['Finn', 'Yoda', 'Rey', 'Qui-Gon'], ['C-3PO', 'Boba', 'Lando', 'Jannah'], ['Jango', 'Obi-Wan', 'Wedge', 'R2-D2']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Phasma', 'Shmi + Cliegg', 'Hux', 'Mace'], ['Sidious', 'Owen + Beru', 'Watto', 'Poe'], ['Jabba', 'Leia + Han', 'Zorii'], ['Yoda', 'Bail + Breha', 'Finn'], ['Rey', 'Anakin + Padme', 'BB-8'], ['Qui-Gon', 'Ben', 'Grevious', 'Luke'], ['Boba', 'C-3PO', 'Lando', 'Jannah'], ['Obi-Wan', 'Jango', 'Wedge', 'R2-D2']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Watto', 'Shmi + Cliegg', 'Hux', 'Obi-Wan'], ['Zorii', 'Owen + Beru', 'Phasma', 'Boba'], ['Lando', 'Leia + Han', 'Sidious'], ['Jannah', 'Bail + Breha', 'Jabba'], ['Mace', 'Anakin + Padme', 'Finn'], ['Wedge', 'BB-8', 'Ben', 'Yoda'], ['R2-D2', 'Grevious', 'Luke', 'Rey'], ['Poe', 'Qui-Gon', 'C-3PO', 'Jango']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Owen + Beru', 'Lando'], ['Leia + Han', 'Bail + Breha', 'Jannah'], ['Anakin + Padme', 'Hux', 'Phasma'], ['Jabba', 'Sidious', 'Watto', 'Finn'], ['Ben', 'Zorii', 'BB-8', 'Yoda'], ['Grevious', 'Luke', 'Rey', 'Qui-Gon'], ['C-3PO', 'Jango', 'Obi-Wan', 'Wedge'], ['Boba', 'R2-D2', 'Poe', 'Mace']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Shmi + Cliegg', 'Obi-Wan'], ['Bail + Breha', 'Leia + Han', 'Watto'], ['Yoda', 'Anakin + Padme', 'Hux'], ['Rey', 'Phasma', 'Sidious', 'Jabba'], ['Luke', 'Wedge', 'Finn', 'BB-8'], ['Lando', 'Zorii', 'Ben', 'Grevious'], ['Jannah', 'Qui-Gon', 'C-3PO', 'Boba'], ['Mace', 'Jango', 'R2-D2', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Leia + Han', 'Mace'], ['Anakin + Padme', 'Owen + Beru', 'Obi-Wan'], ['Hux', 'Bail + Breha', 'Sidious'], ['Zorii', 'Watto', 'Jabba', 'Finn'], ['BB-8', 'Phasma', 'Ben', 'Yoda'], ['Qui-Gon', 'Rey', 'C-3PO', 'Boba'], ['Jango', 'Grevious', 'Luke', 'Jannah'], ['Wedge', 'Lando', 'R2-D2', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Leia + Han', 'Mace'], ['Bail + Breha', 'Shmi + Cliegg', 'Boba'], ['Finn', 'Anakin + Padme', 'Hux'], ['Phasma', 'Sidious', 'Watto', 'Jabba'], ['Obi-Wan', 'Zorii', 'BB-8', 'Ben'], ['R2-D2', 'Yoda', 'Qui-Gon', 'C-3PO'], ['Poe', 'Grevious', 'Luke', 'Rey'], ['Jannah', 'Wedge', 'Jango', 'Lando']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Shmi + Cliegg', 'R2-D2'], ['Sidious', 'Bail + Breha', 'Hux', 'Jango'], ['Watto', 'Owen + Beru', 'Phasma'], ['Yoda', 'Jabba', 'Zorii', 'BB-8'], ['Anakin + Padme', 'Finn', 'Ben'], ['Grevious', 'C-3PO', 'Boba', 'Lando'], ['Luke', 'Rey', 'Qui-Gon', 'Jannah'], ['Mace', 'Wedge', 'Obi-Wan', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Bail + Breha', 'Mace'], ['Owen + Beru', 'Anakin + Padme', 'Poe'], ['Jabba', 'Hux', 'BB-8', 'Phasma'], ['Finn', 'Leia + Han', 'Zorii'], ['Ben', 'Grevious', 'Luke', 'Rey'], ['Lando', 'Wedge', 'Yoda', 'Qui-Gon'], ['C-3PO', 'Sidious', 'Watto', 'R2-D2'], ['Boba', 'Jango', 'Obi-Wan', 'Jannah']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Owen + Beru', 'Obi-Wan'], ['Bail + Breha', 'Anakin + Padme', 'R2-D2'], ['Hux', 'Watto', 'Jabba', 'Zorii'], ['Rey', 'Shmi + Cliegg', 'Finn'], ['BB-8', 'Grevious', 'Luke', 'Qui-Gon'], ['Phasma', 'Ben', 'Yoda', 'C-3PO'], ['Sidious', 'Boba', 'Lando', 'Jannah'], ['Jango', 'Poe', 'Mace', 'Wedge']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Watto', 'Leia + Han', 'Sidious', 'Lando'], ['Shmi + Cliegg', 'Anakin + Padme', 'Mace'], ['Zorii', 'Bail + Breha', 'Hux'], ['Owen + Beru', 'Jabba', 'Finn'], ['Qui-Gon', 'BB-8', 'Phasma', 'Yoda'], ['Obi-Wan', 'Grevious', 'Luke', 'Rey'], ['Wedge', 'C-3PO', 'Jannah', 'Jango'], ['R2-D2', 'Ben', 'Poe', 'Boba']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Poe', 'Shmi + Cliegg', 'Hux', 'Obi-Wan'], ['Leia + Han', 'Anakin + Padme', 'R2-D2'], ['Bail + Breha', 'Owen + Beru'], ['Finn', 'Jabba', 'Wedge', 'BB-8'], ['Yoda', 'Phasma', 'Ben', 'Grevious'], ['Rey', 'Zorii', 'Luke', 'Qui-Gon'], ['Mace', 'C-3PO', 'Boba', 'Jannah'], ['Jango', 'Sidious', 'Lando', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Hux', 'Phasma', 'Mace'], ['Anakin + Padme', 'Leia + Han', 'Sidious'], ['Jabba', 'Owen + Beru', 'Ben'], ['Zorii', 'BB-8', 'Yoda', 'Grevious'], ['Luke', 'Bail + Breha', 'C-3PO'], ['Boba', 'Finn', 'Rey', 'Wedge'], ['Lando', 'Jannah', 'Jango', 'Obi-Wan'], ['Watto', 'R2-D2', 'Qui-Gon', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Hux', 'Phasma', 'Poe'], ['Bail + Breha', 'Sidious', 'Jabba', 'Boba'], ['Ben', 'Shmi + Cliegg', 'Finn'], ['Grevious', 'Owen + Beru', 'Zorii'], ['Jannah', 'Anakin + Padme', 'BB-8'], ['C-3PO', 'Yoda', 'Luke', 'Rey'], ['Qui-Gon', 'Wedge', 'Lando', 'Jango'], ['R2-D2', 'Mace', 'Obi-Wan', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Owen + Beru', 'Finn', 'Mace'], ['Shmi + Cliegg', 'Sidious', 'Jabba', 'Jango'], ['Anakin + Padme', 'Bail + Breha'], ['Wedge', 'Leia + Han', 'Zorii'], ['BB-8', 'Rey', 'C-3PO', 'Boba'], ['Phasma', 'Grevious', 'Luke', 'Qui-Gon'], ['Obi-Wan', 'Yoda', 'Lando', 'Jannah'], ['Poe', 'Watto', 'R2-D2', 'Ben']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Bail + Breha', 'Poe'], ['Sidious', 'Shmi + Cliegg', 'Jabba', 'R2-D2'], ['Finn', 'Phasma', 'Ben', 'Grevious'], ['Yoda', 'Leia + Han', 'Wedge'], ['Luke', 'Hux', 'Boba', 'Lando'], ['Rey', 'C-3PO', 'Jannah', 'Jango'], ['Mace', 'Zorii', 'Qui-Gon', 'BB-8'], ['Watto', 'Anakin + Padme', 'Obi-Wan']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Hux', 'Zorii', 'Poe'], ['Anakin + Padme', 'Shmi + Cliegg', 'Jango'], ['Jabba', 'Yoda', 'Grevious', 'Luke'], ['Ben', 'Owen + Beru', 'Phasma'], ['Jannah', 'Leia + Han', 'Finn'], ['Boba', 'Qui-Gon', 'BB-8', 'Sidious'], ['Lando', 'Rey', 'C-3PO', 'R2-D2'], ['Wedge', 'Mace', 'Obi-Wan', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Hux', 'Zorii', 'Watto'], ['Grevious', 'Shmi + Cliegg', 'Wedge', 'Boba'], ['Leia + Han', 'Jabba', 'Finn'], ['Jango', 'Bail + Breha', 'BB-8'], ['Phasma', 'Anakin + Padme', 'Rey'], ['Yoda', 'Luke', 'Qui-Gon', 'C-3PO'], ['Sidious', 'Obi-Wan', 'Ben', 'Mace'], ['R2-D2', 'Jannah', 'Lando', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Leia + Han', 'BB-8', 'R2-D2'], ['Zorii', 'Shmi + Cliegg', 'Ben', 'Jango'], ['Anakin + Padme', 'Jabba', 'Yoda'], ['C-3PO', 'Owen + Beru', 'Finn'], ['Qui-Gon', 'Bail + Breha', 'Jannah'], ['Obi-Wan', 'Phasma', 'Boba', 'Sidious'], ['Watto', 'Grevious', 'Luke', 'Wedge'], ['Poe', 'Lando', 'Mace', 'Rey']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Zorii', 'Finn', 'Poe'], ['BB-8', 'Leia + Han', 'Jabba', 'R2-D2'], ['Ben', 'Bail + Breha', 'Hux'], ['Grevious', 'Anakin + Padme', 'Phasma'], ['Owen + Beru', 'Yoda', 'Luke'], ['Jannah', 'Rey', 'Sidious', 'Obi-Wan'], ['Jango', 'Qui-Gon', 'C-3PO', 'Boba'], ['Mace', 'Lando', 'Watto', 'Wedge']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Leia + Han', 'Zorii', 'BB-8', 'Watto'], ['Bail + Breha', 'Finn', 'Phasma', 'Jango'], ['Jabba', 'Shmi + Cliegg', 'Rey'], ['Hux', 'Anakin + Padme', 'Ben'], ['Luke', 'Owen + Beru', 'Yoda'], ['Qui-Gon', 'Sidious', 'Obi-Wan', 'R2-D2'], ['C-3PO', 'Poe', 'Mace', 'Grevious'], ['Wedge', 'Boba', 'Lando', 'Jannah']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Finn', 'Shmi + Cliegg', 'Luke', 'Obi-Wan'], ['Rey', 'Owen + Beru', 'Wedge', 'Poe'], ['Anakin + Padme', 'Zorii', 'BB-8'], ['Phasma', 'Leia + Han', 'Boba'], ['Ben', 'Jabba', 'Qui-Gon', 'C-3PO'], ['Grevious', 'Hux', 'Yoda', 'Jannah'], ['Lando', 'Bail + Breha', 'Watto'], ['R2-D2', 'Sidious', 'Jango', 'Mace']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Zorii', 'Leia + Han', 'Luke', 'R2-D2'], ['Shmi + Cliegg', 'BB-8', 'Ben', 'Jango'], ['Owen + Beru', 'Phasma', 'Grevious'], ['Boba', 'Bail + Breha', 'Jabba'], ['Poe', 'Anakin + Padme', 'Finn'], ['Wedge', 'Hux', 'Rey', 'Qui-Gon'], ['Yoda', 'Lando', 'Jannah', 'Sidious'], ['Obi-Wan', 'Watto', 'C-3PO', 'Mace']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Yoda', 'Grevious', 'Luke', 'Lando'], ['Jabba', 'Bail + Breha', 'Qui-Gon', 'Obi-Wan'], ['BB-8', 'Shmi + Cliegg', 'Zorii'], ['Jannah', 'Owen + Beru', 'Phasma'], ['Sidious', 'Leia + Han', 'Finn'], ['Mace', 'Rey', 'Ben', 'Wedge'], ['Watto', 'C-3PO', 'Jango', 'Boba'], ['Anakin + Padme', 'R2-D2', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Luke', 'Shmi + Cliegg', 'Jabba', 'Qui-Gon'], ['Leia + Han', 'Ben', 'Yoda', 'Watto'], ['Bail + Breha', 'BB-8', 'Grevious'], ['Finn', 'Owen + Beru', 'C-3PO'], ['Phasma', 'Zorii', 'Lando', 'Jannah'], ['Rey', 'Hux', 'Boba', 'R2-D2'], ['Jango', 'Anakin + Padme', 'Wedge'], ['Poe', 'Sidious', 'Mace', 'Obi-Wan']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Boba', 'Shmi + Cliegg', 'Zorii', 'Rey'], ['Owen + Beru', 'BB-8', 'Ben', 'Obi-Wan'], ['Lando', 'Anakin + Padme', 'Jabba'], ['R2-D2', 'Leia + Han', 'Hux'], ['Grevious', 'Finn', 'Sidious', 'Jango'], ['Qui-Gon', 'Watto', 'Poe', 'Mace'], ['C-3PO', 'Bail + Breha', 'Phasma'], ['Jannah', 'Luke', 'Yoda', 'Wedge']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Shmi + Cliegg', 'Yoda', 'Grevious', 'C-3PO'], ['Sidious', 'Anakin + Padme', 'Zorii', 'Watto'], ['BB-8', 'Bail + Breha', 'Wedge'], ['Ben', 'Boba', 'Lando', 'Jannah'], ['Luke', 'Leia + Han', 'Phasma'], ['Jango', 'Owen + Beru', 'Jabba'], ['Mace', 'Hux', 'Rey', 'Obi-Wan'], ['Poe', 'Qui-Gon', 'Finn', 'R2-D2']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Zorii', 'Anakin + Padme', 'Rey', 'Poe'], ['Leia + Han', 'Grevious', 'Luke', 'Phasma'], ['Bail + Breha', 'Ben', 'Yoda'], ['Jabba', 'C-3PO', 'Boba', 'Lando'], ['Finn', 'Jannah', 'Sidious', 'Jango'], ['Owen + Beru', 'Wedge', 'R2-D2'], ['Obi-Wan', 'Shmi + Cliegg', 'Hux'], ['Watto', 'BB-8', 'Mace', 'Qui-Gon']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Poe', 'Owen + Beru', 'Jabba', 'Watto'], ['Anakin + Padme', 'Grevious', 'Luke', 'Jango'], ['Yoda', 'Shmi + Cliegg', 'Rey'], ['Boba', 'Leia + Han', 'Hux'], ['Lando', 'Finn', 'BB-8', 'Phasma'], ['Mace', 'Bail + Breha', 'Sidious'], ['Wedge', 'Jannah', 'Ben', 'Obi-Wan'], ['R2-D2', 'Zorii', 'Qui-Gon', 'C-3PO']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Rey', 'Qui-Gon', 'C-3PO', 'R2-D2'], ['Shmi + Cliegg', 'Luke', 'Boba', 'Watto'], ['BB-8', 'Anakin + Padme', 'Finn'], ['Phasma', 'Owen + Beru', 'Jango'], ['Jannah', 'Zorii', 'Ben', 'Grevious'], ['Sidious', 'Wedge', 'Yoda', 'Lando'], ['Leia + Han', 'Mace', 'Obi-Wan'], ['Bail + Breha', 'Poe', 'Jabba']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Wedge', 'Shmi + Cliegg', 'Jabba', 'Mace'], ['Rey', 'Leia + Han', 'Ben', 'Phasma'], ['Luke', 'Grevious', 'Sidious', 'Jango'], ['C-3PO', 'Anakin + Padme', 'Zorii'], ['R2-D2', 'Owen + Beru', 'Finn'], ['Poe', 'Bail + Breha', 'BB-8'], ['Yoda', 'Watto', 'Boba', 'Obi-Wan'], ['Qui-Gon', 'Hux', 'Lando', 'Jannah']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Jango', 'Shmi + Cliegg', 'Zorii', 'R2-D2'], ['Bail + Breha', 'Luke', 'Rey', 'Hux'], ['Anakin + Padme', 'Qui-Gon', 'C-3PO'], ['Ben', 'Sidious', 'Obi-Wan', 'Wedge'], ['Grevious', 'Leia + Han', 'BB-8'], ['Owen + Beru', 'Jannah', 'Boba'], ['Mace', 'Jabba', 'Phasma', 'Yoda'], ['Watto', 'Finn', 'Lando', 'Poe']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Zorii', 'Qui-Gon', 'C-3PO', 'Lando', 'Mace'], ['Boba', 'Owen + Beru', 'Phasma', 'Yoda'], ['Leia + Han', 'Wedge', 'Rey'], ['Obi-Wan', 'Bail + Breha', 'Jabba'], ['Finn', 'Watto', 'R2-D2', 'Poe'], ['BB-8', 'Jannah', 'Hux', 'Jango'], ['Sidious', 'Luke', 'Grevious', 'Ben'], ['Shmi + Cliegg', 'Anakin + Padme']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Wedge', 'Owen + Beru', 'Finn', 'BB-8'], ['Phasma', 'Bail + Breha', 'R2-D2', 'Watto'], ['Jabba', 'Anakin + Padme', 'Jannah'], ['Rey', 'Yoda', 'Grevious', 'Mace'], ['Qui-Gon', 'Shmi + Cliegg', 'Zorii'], ['C-3PO', 'Leia + Han', 'Hux'], ['Lando', 'Luke', 'Poe', 'Boba'], ['Jango', 'Ben', 'Obi-Wan', 'Sidious']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Watto', 'Bail + Breha', 'Jabba', 'Yoda'], ['Poe', 'Leia + Han', 'Zorii', 'Finn'], ['R2-D2', 'Shmi + Cliegg', 'Wedge'], ['Anakin + Padme', 'Rey', 'Jannah'], ['Hux', 'Jango', 'Boba', 'Obi-Wan'], ['Grevious', 'Ben', 'Mace', 'Lando'], ['Luke', 'Owen + Beru', 'Qui-Gon'], ['Sidious', 'C-3PO', 'BB-8', 'Phasma']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Qui-Gon', 'C-3PO', 'Watto'], ['Shmi + Cliegg', 'Rey', 'Jannah', 'Hux'], ['Owen + Beru', 'Sidious', 'Jango'], ['Leia + Han', 'Boba', 'Lando'], ['Obi-Wan', 'Anakin + Padme', 'Finn'], ['Wedge', 'Luke', 'Phasma', 'Grevious'], ['Jabba', 'R2-D2', 'Poe', 'Mace'], ['Ben', 'Yoda', 'BB-8', 'Zorii']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Jango', 'Leia + Han', 'Hux', 'Sidious'], ['Luke', 'Ben', 'Obi-Wan', 'R2-D2', 'Zorii'], ['Jannah', 'Shmi + Cliegg', 'Watto'], ['Phasma', 'Wedge', 'Finn', 'BB-8'], ['Yoda', 'Owen + Beru', 'Poe'], ['Qui-Gon', 'Anakin + Padme', 'Jabba'], ['C-3PO', 'Bail + Breha', 'Lando'], ['Boba', 'Grevious', 'Rey', 'Mace']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Poe', 'Phasma', 'Wedge', 'Jannah', 'C-3PO'], ['Ben', 'Anakin + Padme', 'R2-D2', 'Jango'], ['Bail + Breha', 'Obi-Wan', 'Lando'], ['Mace', 'Shmi + Cliegg', 'Luke'], ['Zorii', 'Sidious', 'Leia + Han'], ['Finn', 'Boba', 'Owen + Beru'], ['BB-8', 'Watto', 'Grevious', 'Rey'], ['Hux', 'Qui-Gon', 'Yoda', 'Jabba']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['C-3PO', 'Shmi + Cliegg', 'Jabba', 'Zorii'], ['R2-D2', 'Bail + Breha', 'BB-8', 'Hux'], ['Anakin + Padme', 'Boba', 'Wedge'], ['Grevious', 'Poe', 'Obi-Wan', 'Watto'], ['Rey', 'Lando', 'Leia + Han'], ['Owen + Beru', 'Qui-Gon', 'Jannah'], ['Jango', 'Finn', 'Phasma', 'Yoda'], ['Luke', 'Mace', 'Ben', 'Sidious']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Watto', 'Jannah', 'Zorii', 'Rey', 'C-3PO'], ['Shmi + Cliegg', 'Wedge', 'R2-D2', 'Phasma'], ['Boba', 'Anakin + Padme', 'Luke'], ['Lando', 'Owen + Beru', 'Hux'], ['Leia + Han', 'Qui-Gon', 'Jango'], ['Obi-Wan', 'Poe', 'Bail + Breha'], ['Finn', 'Mace', 'Grevious', 'Ben'], ['BB-8', 'Yoda', 'Sidious', 'Jabba']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Jannah', 'R2-D2', 'Hux', 'Poe', 'Boba'], ['Zorii', 'Wedge', 'Obi-Wan', 'Lando', 'Phasma'], ['Yoda', 'Jango', 'Mace', 'Grevious'], ['Rey', 'Bail + Breha', 'Watto'], ['Qui-Gon', 'Owen + Beru', 'Finn'], ['C-3PO', 'BB-8', 'Ben', 'Luke'], ['Anakin + Padme', 'Leia + Han'], ['Jabba', 'Shmi + Cliegg', 'Sidious']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Hux', 'Wedge', 'Jannah', 'Poe', 'Jango'], ['BB-8', 'Lando', 'Obi-Wan', 'Mace', 'Boba'], ['Owen + Beru', 'Rey', 'C-3PO'], ['Bail + Breha', 'Leia + Han'], ['R2-D2', 'Anakin + Padme', 'Jabba'], ['Shmi + Cliegg', 'Qui-Gon', 'Grevious'], ['Finn', 'Luke', 'Ben', 'Yoda'], ['Phasma', 'Sidious', 'Zorii', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Obi-Wan', 'Owen + Beru', 'Qui-Gon', 'Hux'], ['Mace', 'Leia + Han', 'Grevious', 'Phasma'], ['Wedge', 'Bail + Breha', 'Sidious'], ['Anakin + Padme', 'Lando', 'Watto'], ['Jabba', 'Jango', 'Shmi + Cliegg'], ['Ben', 'Poe', 'Jannah', 'Luke'], ['Boba', 'Rey', 'Yoda', 'Finn'], ['Zorii', 'R2-D2', 'C-3PO', 'BB-8']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Bail + Breha', 'Wedge', 'Jannah', 'Boba'], ['Phasma', 'Poe', 'Obi-Wan', 'Lando', 'Hux'], ['Finn', 'Leia + Han', 'Grevious'], ['Luke', 'Watto', 'Anakin + Padme'], ['Sidious', 'Rey', 'Qui-Gon', 'Ben'], ['Shmi + Cliegg', 'Owen + Beru'], ['Yoda', 'R2-D2', 'Mace', 'Jabba'], ['C-3PO', 'BB-8', 'Zorii', 'Jango']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Boba', 'Ben', 'Watto', 'Wedge', 'Jango'], ['Lando', 'Shmi + Cliegg', 'Mace', 'Hux'], ['Leia + Han', 'C-3PO', 'Sidious'], ['Poe', 'Yoda', 'Anakin + Padme'], ['Jabba', 'Bail + Breha', 'Jannah'], ['Zorii', 'Owen + Beru', 'Grevious'], ['Qui-Gon', 'Luke', 'Rey', 'Obi-Wan'], ['R2-D2', 'Phasma', 'Finn', 'BB-8']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Finn', 'Bail + Breha', 'Lando', 'Hux'], ['Watto', 'Ben', 'Leia + Han', 'Phasma'], ['Shmi + Cliegg', 'Obi-Wan', 'Wedge'], ['Grevious', 'R2-D2', 'Anakin + Padme'], ['Luke', 'Poe', 'Owen + Beru'], ['Rey', 'Jannah', 'Mace', 'Qui-Gon'], ['C-3PO', 'Yoda', 'Sidious', 'Jabba'], ['Jango', 'BB-8', 'Zorii', 'Boba']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Jabba', 'Wedge', 'Leia + Han', 'Jango'], ['Zorii', 'Jannah', 'Anakin + Padme', 'Phasma'], ['Ben', 'Mace', 'Shmi + Cliegg'], ['Qui-Gon', 'Bail + Breha', 'Lando'], ['Owen + Beru', 'Grevious', 'Luke'], ['Obi-Wan', 'Rey', 'Yoda', 'Sidious'], ['Poe', 'Boba', 'Finn', 'R2-D2'], ['Hux', 'C-3PO', 'BB-8', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Rey', 'Obi-Wan', 'Leia + Han', 'Boba'], ['Jango', 'Anakin + Padme', 'Wedge', 'Hux'], ['C-3PO', 'Qui-Gon', 'Shmi + Cliegg'], ['Jannah', 'Mace', 'Bail + Breha'], ['Finn', 'Owen + Beru', 'Lando'], ['BB-8', 'Grevious', 'Luke', 'Ben'], ['Phasma', 'Yoda', 'Sidious', 'Poe'], ['R2-D2', 'Jabba', 'Zorii', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Owen + Beru', 'Lando', 'Wedge', 'Jango'], ['Qui-Gon', 'Leia + Han', 'Jannah', 'Phasma'], ['Bail + Breha', 'Mace', 'Grevious'], ['Obi-Wan', 'Anakin + Padme', 'Luke'], ['Jabba', 'Shmi + Cliegg', 'Rey'], ['Zorii', 'Ben', 'Yoda', 'Sidious'], ['Hux', 'Finn', 'Poe', 'R2-D2'], ['Boba', 'C-3PO', 'BB-8', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Jango', 'Rey', 'Leia + Han', 'Boba'], ['Mace', 'Owen + Beru', 'Wedge', 'Hux'], ['Anakin + Padme', 'Shmi + Cliegg'], ['Finn', 'Bail + Breha', 'Lando'], ['BB-8', 'Jannah', 'Grevious', 'Luke'], ['Phasma', 'Ben', 'Obi-Wan', 'Qui-Gon'], ['Yoda', 'Sidious', 'Poe', 'Jabba'], ['R2-D2', 'C-3PO', 'Zorii', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Obi-Wan', 'Leia + Han', 'Wedge', 'Jango'], ['Jabba', 'Anakin + Padme', 'Lando', 'Phasma'], ['Zorii', 'Shmi + Cliegg', 'Jannah'], ['Hux', 'Bail + Breha', 'Grevious'], ['Ben', 'Owen + Beru', 'Luke'], ['Rey', 'Mace', 'Qui-Gon', 'Yoda'], ['C-3PO', 'Sidious', 'Finn', 'Poe'], ['Boba', 'R2-D2', 'BB-8', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Wedge', 'Anakin + Padme', 'Lando', 'Boba'], ['Finn', 'Leia + Han', 'Jannah', 'Hux'], ['Shmi + Cliegg', 'Bail + Breha'], ['BB-8', 'Owen + Beru', 'Grevious'], ['Phasma', 'Luke', 'Rey', 'Ben'], ['Yoda', 'Mace', 'Obi-Wan', 'Qui-Gon'], ['Sidious', 'Poe', 'Jabba', 'R2-D2'], ['Jango', 'C-3PO', 'Zorii', 'Watto']],
[[5, 5, 4, 4, 4, 4, 4, 4], ['Anakin + Padme', 'Mace', 'Wedge', 'Boba'], ['Hux', 'Leia + Han', 'Lando', 'Phasma'], ['Jabba', 'Shmi + Cliegg', 'Jannah'], ['Zorii', 'Bail + Breha', 'Grevious'], ['Ben', 'Owen + Beru', 'Luke'], ['Rey', 'Obi-Wan', 'Qui-Gon', 'Yoda'], ['C-3PO', 'Sidious', 'Finn', 'Poe'], ['R2-D2', 'BB-8', 'Watto', 'Jango']]
]
``` 
