#!/usr/bin/bash

sudo apt-get update -y
sudo raspi-config nonint do_spi 0
sudo apt-get install python-dev python3-dev -y

