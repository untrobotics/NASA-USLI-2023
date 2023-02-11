# Setup tl;dr

`sudo apt-get install python-smbus i2c-tools`

Add to /boot/config.txt

`dtoverlay=i2c-rtc,ds3231`

Run

```
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock
```

Edit /lib/udev/hwclock-set and comment out these lines

```
if [ -e /run/systemd/system ] ; then
exit 0
fi
```

and

`/sbin/hwclock --rtc=$dev --systz --badyear` and `/sbin/hwclock --rtc=$dev --systz`

Reboot (adafruit says to reboot after editing config.txt, but that's for making sure the clock shows up in `i2cdetect`)



[Guide Link](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time)
