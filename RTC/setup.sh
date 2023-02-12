#!/bin/bash
sudo apt-get install python-smbus i2c-tools -y ;
sudo echo 'dtoverlay=i2c-rtc,ds3231' >> /boot/config.txt ;
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove -y
sudo systemctl disable fake-hwclock -y
sudo sed -ri 's/^(\s*if\s+\[\s+-e\s+\/run\/systemd\/system\s+\]\s+;\s+then.*fi\s*;?)(.*)/(.*)/#\1\n\2/' /lib/udev/hwclock-set ;
sudo sed -ri '/^(\s*if\s+\[\s+-e\s+\/run\/systemd\/system\s+\]\s+;\s+then.*)/,/^fi/s/(.*)/#\1/' /lib/udev/hwclock-set ;
sudo sed -ri 's/(\/sbin\/hwclock --rtc=$dev --systz --badyear\s*;?)(.*)/#\1\n\2/' /lib/udev/hwclock-set ;
sudo sed -ri 's/(\/sbin\/hwclock --rtc=$dev --rtc=$dev --systz\s*;?)(.*)/#\1\n\2/' /lib/udev/hwclock-set ;
