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
sudo sed -ri '/^\s*\/home\/pi\/NASA-USLI-2023\/pi-actual\/startup.sh/q;s/^(\s*exit\s+0[^\n\r]*)/\/home\/pi\/NASA-USLI-2023\/pi-actual\/startup.sh ;\n\1/' /etc/rc.local ;

sudo pip3 install aprs kiss picamera2 pigpio
sudo pip3 install adafruit-circuitpython-mpu6050
sudo pip3 install adafruit-circuitpython-bmp3xx
