sudo apt-get update
sudo apt-get install -y pigpiod python3 python3-pip i2c-tools git python3-smbus
sudo systemctl enable pigpiod

# 2023 specific installs
sudo apt-get install -y direwolf rtl-sdr multimon

# if using rtc
# then do stuff
#nano -w /boot/config.txt
#sudo nano -w /boot/config.txt
#sudo apt-get -y remove fake-hwclock
#sudo update-rc.d -f fake-hwclock remove
#sudo systemctl disable fake-hwclock
#nano -w /lib/udev/hwclock-set
#sudo nano -w /lib/udev/hwclock-set
#nano -w /lib/udev/hwclock-set
#sudo nano -w /lib/udev/hwclock-set
#sudo hwclock -r
#reboot
#sudo reboot
if !  cat /etc/rc.local | grep ^[[:space:]]*/home/pi/NASA-USLI-2023/pi-actual/startup.sh ; then
  sudo sed -ri 's/^(\s*exit\s+0[^\n\r]*)/\/home\/pi\/NASA-USLI-2023\/pi-actual\/startup.sh\n\1/' /etc/rc.local ;
fi
sudo apt-get install -y python3-prctl
sudo pip3 install aprs kiss picamera2 pigpio --break-system-packages
sudo pip3 install adafruit-circuitpython-mpu6050 --break-system-packages
sudo pip3 install adafruit-circuitpython-bmp3xx --break-system-packages
sudo pip3 install adafruit-circuitpython-bno055 --break-system-packages

if [ ! -d "/home/pi/capture" ]
then
  mkdir /home/pi/capture
fi
