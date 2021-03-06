#!/bin/bash

# tkinter
sudo apt install -y python3-tk
# Creates a virtual python environment 
virtualenv --no-site-packages --distribute .env
source .env/bin/activate
pip install -r requirements.txt
