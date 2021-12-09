Repository structure:

| File Name | Description |
| --- | --- |
| MasterCommunicator/ | Distributed password cracking system. |
| MasterWeb/ | Web interface to interact with distributed password cracking system. |
| c.sh | Utility script to interact with GENI. |
| installNpm.sh | Script to install npm on GENI node. |
| rspec.xml | rspec file used to request resources from GENI. |
| README.md | This file. |

The distributed password cracker system is built in python 3.6.5.
The web interface is built using the Express framework for Node.js.

Instructions to install:
1. Use rspec.xml to request resources from GENI.
	* Use any InstaGENI test site.
	* Use the Auto IP function.
1. Change the variables at the top of c.sh as appropriate.
1. In MasterCommunicator/Common.py, change the HOST_NAME variable to the hostname of the master node on geni.
1. Run `. c.sh`.
	* You may be asked about trusting key fingerprints. Of course, say yes in order to continue with the instructions.
1. Log into each node using ssh.
	* In worker nodes, run `ls` and ensure that the MasterCommunicator folder exists.
	* In the master node, run `ls` and ensure that the following exist:
		* MasterCommunicator folder
		* MasterWeb folder
		* installNpm.sh file
		* runMaster.sh file
1. On the master node, run `. installNpm.sh`.
1. On the master node, run `npm install -g npm`.
1. For every worker node:
	1. On the worker node, run `sudo route add -net ${ip} netmask 255.255.255.255 dev eth1`, where ${ip} is the ip address of eth0 of the master node.
	1. Choose a delay in milliseconds, a packet loss rate in percentage, and a corruption rate in percentage for the network environment.
		1. On the worker node, run `sudo tc qdisc add dev eth1 root netem delay ${d}ms loss ${p}% corrupt ${c}%`, where ${d} is the chosen delay in milliseconds, ${p} is the chosen packet loss rate in percentage, and ${c} is the chosen corruption rate in percentage.
		1. On the master node, run `sudo tc qdisc add dev ${if} root netem delay ${d}ms loss ${p}% corrupt ${c}%`, where ${if} is the name of the interface that connects it to the worker node, ${d} is the chosen delay in milliseconds, ${p} is the chosen packet loss rate in percentage, and ${c} is the chosen corruption rate in percentage.
		* The delay or loss or corrupt parameter and the parameter that follows it can be omitted to add no additional delay or loss or corruption to the network environment.

Instructions to start up system:
1. On the master node, run:
	1. `cd MasterCommunicator`
	1. `python3 Master.py`.
1. At any time, on as many worker nodes as you wish, but at least one, run:
	1. `cd MasterCommunicator`
	1. `python3 Worker.py`
* You can delete worker nodes on demand by killing their process.
* You can add worker nodes on demand by running the `python3 Worker.py` command on them.
* The worker nodes print the number of hashes checked so far and an estimate of the hash rate, unless it is not currently hashing, in which case it prints "sleeping" instead of the estimate of the hash rate.

Instructions to use the web interface:
1. Do the instructions to install.
1. Do the instructions to start up system.
1. ssh into the the master node and then run:
	1. `cd MasterWeb`
	1. `npm install`
	1. `npm start`
1. In your web browser, go to hostname:3000, but where hostname is replaced with the hostname of the master node on geni.
	* An example of the url to go to is master.gnhfp1.ch-geni-net.instageni.research.umich.edu:3000 if master.gnhfp1.ch-geni-net.instageni.research.umich.edu is the hostname of the master node.
1. You can type in the hex string of an MD5 hash of an element of the search space into the text field and then hit the submit button to make the system begin the brute force search.
	* The search space is all strings of length 5 of all uppercase characters.
	* An example of an element in the search space is SRYKS and the hex string of its MD5 hash is 6abf295909e6e07f5cb89e182b2a476f.
	* After hitting submit, the web page should show that you submitted at least one hash and it should show you the hashes submitted.
		* If after the equals sign it says "Still cracking" then you can refresh the page to check on its progress.

Instructions to run test:
1. Do the instructions to install.
1. Do the instructions to start up system.
1. ssh into master node and then run:
	1. `cd MasterCommunicator`
	1. `python3 MasterTester.py`