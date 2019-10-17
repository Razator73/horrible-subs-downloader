# Horrible Subs Downloader

Use this to scrape the HorribleSubs site for a particular show and add new episodes
to be downloaded.

## Dependencies
### transmission-daemon

```
sudo apt-get install -y transmission-daemon transmission-cli transmission-common
sudo service transmission-daemon stop
sudo nano /etc/transmission-daemon/settings.json
sudo service transmission-daemon start
```

See [transmission documentation](https://github.com/transmission/transmission/wiki/Editing-Configuration-Files)
for details on the `settings.json` file options

### Others
```
sudo apt install -y chromium-browser chromium-chromedriver
sudo apt install -y libxml2-dev libxslt1-dev
```

### VPN (recommended)

I choose to use a paid VPN from [Private Internet Access](https://www.privateinternetaccess.com/) (PIA).
You will need a paid account for this to work.
```
sudo apt-get install openvpn -y
cd /etc/openvpn
sudo wget https://www.privateinternetaccess.com/openvpn/openvpn.zip
sudo unzip openvpn.zip
```
Set it up to auto start at boot by supplying your PIA username to the first line
and then the password to the second line of a `login.conf` file
```
sudo nano login.conf
sudo chmod 400 login.conf
sudo cp <desired country>.ovpn <desired country>.conf
```
And edit the conf file:
```
sudo nano *desired country you'd like to connect to*.conf
``` 
Find auth-user-pass, add a space and enter:
```
/etc/openvpn/login.conf
```
Locate crl-verify and input:
```
/etc/openvpn/
```
Under ca add:
```
/etc/openvpn/
```
Press CTRL + X, then Y and enter. Test your connection with:
```
sudo openvpn *desired country you'd like to connect to*.conf
```
Run:
```
sudo nano /etc/default/openvpn
```
Under the last line where it says auto start, add:
```
AUTOSTART=”desired country you'd like to connect to”
```
Again, CTRL + X, Y, and enter. Then, restart:
```
sudo shutdown -r 0
```
