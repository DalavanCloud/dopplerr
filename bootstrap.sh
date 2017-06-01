#!/bin/bash

echo "Bootstrap system tools"
echo "sudo it accodingly to your system"

if [ -f /etc/debian_version ]; then
    apt-get install git
elif [ -f /etc/redhat-release ]; then
    yum install git
else
    echo "Please ensure 'git' is installed on your system"
fi

# Freeze the version of pip and pipenv for setup reproductibility
pip install -U 'pip==9.0.1' 'pipenv==4.1.3' 'setuptools<36' || echo "you may need to sudo me !"
echo "Done"
