# geni ssh username
login=nathanhh

# geni ssh key file location
keyfile=../geni

# ssh master node name
nm=pcvm3-4.instageni.colorado.edu

# ssh worker node names
n1=pc3.instageni.colorado.edu
n2=pc3.instageni.colorado.edu
n3=pc3.instageni.colorado.edu
n4=pc3.instageni.colorado.edu
n5=pc3.instageni.colorado.edu
n6=pc3.instageni.colorado.edu
n7=pc3.instageni.colorado.edu
n8=pc3.instageni.colorado.edu

# ssh worker node port numbers
p1=25011
p2=25012
p3=25013
p4=25014
p5=25015
p6=25016
p7=25017
p8=25018

if [ "$#" -eq 0 ]; then
	scp -r -i $keyfile -P $p1 MasterCommunicator $login@$n1:~
	scp -r -i $keyfile -P $p2 MasterCommunicator $login@$n2:~
	scp -r -i $keyfile -P $p3 MasterCommunicator $login@$n3:~
	scp -r -i $keyfile -P $p4 MasterCommunicator $login@$n4:~
	scp -r -i $keyfile -P $p5 MasterCommunicator $login@$n5:~
	scp -r -i $keyfile -P $p6 MasterCommunicator $login@$n6:~
	scp -r -i $keyfile -P $p7 MasterCommunicator $login@$n7:~
	scp -r -i $keyfile -P $p8 MasterCommunicator $login@$n8:~
	
	scp -r -i $keyfile installNpm.sh $login@$nm:~
	scp -r -i $keyfile runMaster.sh $login@$nm:~
	scp -r -i $keyfile MasterCommunicator $login@$nm:~
	scp -r -i $keyfile MasterWeb $login@$nm:~
elif [ "$#" -eq 1 ]; then
	if [ $1 == m ]; then
		ssh -i $keyfile $login@$nm
	elif [ $1 == 1 ]; then
		ssh -i $keyfile $login@$n1 -p $p1
	elif [ $1 == 2 ]; then
		ssh -i $keyfile $login@$n2 -p $p2
	elif [ $1 == 3 ]; then
		ssh -i $keyfile $login@$n3 -p $p3
	elif [ $1 == 4 ]; then
		ssh -i $keyfile $login@$n4 -p $p4
	elif [ $1 == 5 ]; then
		ssh -i $keyfile $login@$n5 -p $p5
	elif [ $1 == 6 ]; then
		ssh -i $keyfile $login@$n6 -p $p6
	elif [ $1 == 7 ]; then
		ssh -i $keyfile $login@$n7 -p $p7
	elif [ $1 == 8 ]; then
		ssh -i $keyfile $login@$n8 -p $p8
	fi
fi

