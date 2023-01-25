#!/bin/bash

source ./lora_app/venv/bin/activate
python3 ./lora_app/pySX127x/socket_transceiver.py &
FLASK_APP=./web_app/app.py flask run -h 0.0.0.0 &
python3 ./lora_app/pySX127x/motion_detection.py &