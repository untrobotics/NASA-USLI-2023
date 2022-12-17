# About
This is the python code to control the servos and camera on the payloads.

# Installation

Download the directory and place it in your project. Make sure to keep the files in the [aprs directory](https://github.com/untrobotics/NASA-USLI-2023/tree/main/PayloadController/aprs) there.

Install [kiss](https://github.com/ampledata/kiss) using pip with `pip install kiss`.

Note: 

This uses the [python APRS module](https://github.com/ampledata/aprs) by ampledata, however the installation package is broken, so the files from there are in the aprs directory.

This bug is unlikely to ever be fixed (see this [4-year old issue](https://github.com/ampledata/aprs/issues/27)).

## Setting up Raspiaudio

[Source](https://forum.raspiaudio.com/t/ultra-installation-guide/21)

To set up the sound card for usage, you need to follow these steps:

1. git clone https://github.com/RASPIAUDIO/ultra2 78
2. cd ultra2
3. sudo ./install.sh
4. sudo reboot

**This can take about 14-15 minutes on a raspberry pi zero**. 
