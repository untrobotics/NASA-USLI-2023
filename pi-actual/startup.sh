#!/bin/bash
#sudo service pigpiod start
rtl_fm -f 144.39M - | direwolf -c ./sdr.conf -r 24000 -D 1 - &
python /home/pi/NASA-USLI-2023/pi-actual/control.py
