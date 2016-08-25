#!/bin/bash
# Script to add a user Restricted to SSH Tunneling Only
if [ $(id -u) -eq 0 ]; then
	read -p "Enter username : " username
	read -s -p "Enter password : " password
	egrep "^$username" /etc/passwd >/dev/null
	if [ $? -eq 0 ]; then
		echo "$username exists!"
		exit 1
	else
		pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
        # I will show in the following how you can create such a restricted SSH user on a Linux server (tested on Debian Linux) that can be used for SSH tunneling only.
        # First of all we create a new user (I just call him sshtunnel now) with rbash as shell:
		useradd -m -d /home/$username -p $pass $username -s /bin/rbash
        # Using rbash instead of bash will restrict the user already as he especially cannot change the directory and cannot set any environment variables. But the user can still execute most of the bash commands.
        # To prevent him from this, we use a small trick: we set the environment variable PATH for this user to nothing. This way the bash won’t find the commands to execute anymore. That’s easily done by adding this line to the end of the file .profile in the home directory of the user (in our example it is /home/sshtunnel/):
        echo 'PATH=""' >> /home/$username/.profile
        # As we want to make sure the user is not able to change this again himself, we remove the write permissions from the user configuration files and from the home directory of the user itself:
        chmod 555 /home/$username/
        cd /home/$username/
        chmod 444 .bash_logout .bashrc .profile
		[ $? -eq 0 ] && echo "User has been added to system $username!" || echo "Failed to add a user $username!"
	fi
else
	echo "Only root may add a user to the system"
	exit 2
fi