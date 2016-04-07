Title: Clustering and classification of application's error messages for offline retrieval of an existing solution. Preliminary research.
--------------------------

Abstract 
--------------
*#PERSON Marek Bardoński #2ND*

General usage: problem description, proposed solution

Introduction, motivation
--------------------------
*#PERSON Mateusz Macias*

1) Where did the idea come from? (idea from Canonical + us, meeting)

2) UW ML RG, to learn ML techniques, focus on teaching, large group of people, some of them are unexperienced

3) Use cases (1) new linux users, 2) admins, manual scripting replacement, 3) others(google + stackoverflow))

4) Plans to incorporate the app in Ubuntu 17.04
 
Algorithms overview  
--------------------------
*#PERSON Mateusz Susik #2ND*

1) Clustering - affinity propagation

2) Classification - NN

Techincal overview 
--------------------------
*#PERSON Mateusz Susik #2ND*

1) Server

a) Communication with client, security - detecting spam, loops, attacks, etc

b) HDFS, canonical, Spark

c) Cleaning the database

2) Client

a) REST, problems with reading from terminals

b) offline classification

3) Pipeline description



Preprocessing 
--------------------------
*#PERSON Hubert Tarasiuk*

1) Normalization of system paths (~home), /opt/bin, /bin/ etc - heuristics

2) lowercase, 's, timestamps, PII (emails, passwords) removal (library?)

3) Optional translation

4) Stopwords (?)


Clustering 
--------------------------
*#PERSON Marek Bardoński Jacek Karwowski*

Features

1) Word count, word bigram, TF, IDF, package name, package version, basic system info (possible size limitations?) [src5]

Main algorithm

2) Affinity propagation [src1] [abstract generation - src needed]

Supporting algorithms

3) Spectral clustering [src needed]

Heuristics

4) thefuck [src4], microsoft [src3]

Classification 
--------------------------
*#PERSON Piotr Wiśniewski*

Main algorithm

1) Neural networks

Supporting algorithms

2) Multiclass logistic regression


Solution matching approaches
--------------------------
Stack overflow crawler

*#PERSON Szymon Pajzert*

Lifelong systemlogs 

*#PERSON Marek Bardonski*

Examples 
--------------------------
*#PERSON Krystyna Gajczyk*

Usecases 


Similar projects
-------------------------- 
*#PERSON Jakub Staroń*

Red Hat Access

Pulse

Entropy

Cluebox



Bibliography
--------------------------
[src1] http://www.psi.toronto.edu/affinitypropagation/FreyDueckScience07.pdf 

[src4] https://github.com/nvbn/thefuck

[src3] http://research.microsoft.com/apps/pubs/default.aspx?id=81176

[src5] http://uu.diva-portal.org/smash/get/diva2:667650/FULLTEXT01.pdf

Symbols
----------
#2ND - second iteration, after completing other tasks
(?) - to the autor's discretion
