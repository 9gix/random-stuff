# Raspberry PI Setup

## Auto Login

```bash
# File: /etc/inittab
# Find and Comment out the following line
# 1:2345:respawn:/sbin/getty 115200 tty1
# Add these instead
1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1
```

## Auto Start Desktop GUI (run LXDE)

```bash
# File: /etc/rc.local
# Add this command above exit 0
su -l pi -c startx
```

## Auto Execute a Python Script After startup.
```bash
# File: /etc/rc.local
# Add the command followed by `&` to execute it in the background
python /home/pi/script1.py &
```

## Auto Connect to Wi-Fi
```bash
# File: /etc/network/interfaces
# At the top
auto wlan0

# At the bottom
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

```bash
# File: /etc/wpa_supplicant/wpa_supplicant
network={
    ssid="My SSID"
    psk="p@ssword"
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
}

```

## Static IP for eth0
```bash
# File: /etc/network/interfaces
# Change the following line:
# iface eth0 inet dhcp

# Become
iface eth0 inet static
address 192.168.0.250
netmask 255.255.255.0
gateway 192.168.0.1
network 192.168.0.0
broadcast 192.168.0.255
```

## Setup VNC for Remote Desktop
`sudo apt-get install tightvncserver`

```bash
# File: /etc/init.d/vncboot

### BEGIN INIT INFO
# Provides: vncboot
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start VNC Server at boot time
# Description: Start VNC Server at boot time.
### END INIT INFO

#! /bin/sh
# /etc/init.d/vncboot

USER=pi
HOME=/home/pi

export USER HOME

case "$1" in
 start)
  echo "Starting VNC Server"
  #Insert your favoured settings for a VNC session
  su - $USER -c /usr/bin/vncserver :0 -geometry 1280x800 -depth 16 -pixelformat rgb565
  ;;

 stop)
  echo "Stopping VNC Server"
  su - $USER -c /usr/bin/vncserver -kill :0
  ;;

 *)
  echo "Usage: /etc/init.d/vncboot {start|stop}"
  exit 1
  ;;
esac

exit 0
```

`chmod 755 vncboot`
`update-rc.d vncboot defaults`

