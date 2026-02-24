#!/bin/bash

echo ACL module Auto-Setup
echo This .sh file will download all needed pip libraries Python script

sleep 1
read -p "Type anything to continue."

pip3 install -r requirements.txt

echo "'Externally managed' error? Enter to python3 virtual environment and use the script again."
sleep 1

echo "Done."
