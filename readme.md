AI powered agent, running locally on your machine, analyzing what's going on in the logs and overall on the system, and advertizing what's wrong, then, hopefully, offer an answer to help you fix it.

You know when you try to start a command and the system tells you "maybe you need to apt-get install <X> so it works"? Well, this would be the same, but for any aspect of your system. "You've been hacked, you should install rkhunter", "mysql is not performing well, you should ..."

There are 3 phases to get this done. 
First a "model" has to be trained. This requires a lot of data from running and failing systems, to identify issues, causes, and solutions
Then an agent capable of using this model and run it locally has to be created (you don't want to ship your logs to the cloud permanently, everything has to be local)
Then it needs to improve over time, and keep getting better as more and more problems arise, so it's kind of a ever-running system.

Installing the client from repository:
--------------------------------------

```
cd client
sudo python setup.py install
```

Installing the server from repository:
--------------------------------------

```
curl -sSL https://get.docker.com/ | sh
sudo apt install python-pip
sudo pip install docker-compose
cd server/alpha
sudo docker-compose up
```

Creating the debian package:
----------------------------

```
sudo apt install debhelper python-requests python-gi automake cdbs
cd client
make builddeb
```
