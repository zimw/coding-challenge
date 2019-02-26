# coding-challenge
# Challenge #1 - Programming
Q1: What would the bottleneck(s) be in your implementation as you acquire more users? How you might scale your
microservice?
A: currently, through docker, I have two machines and 5 instances of the website running at the same time.
However all these five instance are sharing a single DB(redis) which is configured only in the master machine.
This will become an issue as we build up the DB. 
To overcome this, I would add sharding to split the redis hash to multiple servers.

Q2: How would you improve your deployment process if you needed to maintain this application long term?
Automate the deployment process such as creating identical nodes/servers through tools like chef.
