#!/usr/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo raspi-config nonint do_spi 0
sudo apt-get install python-dev python3-dev -y
sudo apt-get install python3-pip

pip3 install RPi.GPIO
pip3 install LoRaRF
pip3 install wiringpi
pip3 install opencv-python
pip3 install requests

pythonVersion="$(python3 -V)"
requiredVersion="3.6.0"
if [ "$(printf '%s\n' "$requiredVersion" "$pythonVersion" | sort -V | head -n1)" = "$requiredVersion" ]; then 
    echo "Python version already satisfied (${pythonVersion})"
else
    echo "-----------------------------------------"
    echo "Older than ${requiredVersion}, needs upgrade!"
fi