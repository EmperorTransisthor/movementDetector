# Movement detector
**Introduction**

This is project which aims to create movement detector system using Raspberry Pi 3Bs with
Dragino LoRa modules and cameras. It works in master-slave configuration, with many slaves and one master. General idea is about
creating system, which would be able to detect movement (slave) and inform master Raspberry about it.
Some action takes place after detection, our ideas: send email/sms/photo on trigger.

Such system would be useful in large area places, where WiFi is not available.

# How to use it

Main folder contains pySX127x folder, where are *rx_cont.py* (receiver) and *tx_beacon.py*
(transmiter) scripts. Test it by yourselves by starting both scripts simultaneously. It is
recommended to setup environment (when launching project for the first time) via *setup.sh* script.

Other files:
* test.jpg - test image
* Compressed.jpg - compressed test image
* compress_image.py - python script for compressing images
* example2.py - python script with example on how to compress images from compress_image.py


# Important websites
- https://wiki1.dragino.com/index.php?title=Lora/GPS_HAT
- https://pypi.org/project/pyLoRa/
- https://circuitdigest.com/microcontroller-projects/raspberry-pi-with-lora-peer-to-peer-communication-with-arduino
- https://pypi.org/project/LoRaRF/
- https://www.dragino.com/downloads/downloads/LoRa-GPS-HAT/LoRa_GPS_HAT_UserManual_v1.0.pdf
