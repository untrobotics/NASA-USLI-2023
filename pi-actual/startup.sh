#!/bin/bash
service pigpiod start
rtl_fm -f 144.39M - | direwolf -c ./sdr.conf -r 24000 -D 1 -
