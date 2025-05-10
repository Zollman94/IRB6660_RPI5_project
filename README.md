RPI 5- MAC: 2C:CF:67:3E:92:26
IP kamera MAC: E8:B7:23:00:E5:CF

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses "192.168.50.149/24" ipv4.gateway "192.168.50.200" ipv4.dns "8.8.8.8" ipv4.method manual
```


RTPS Stream of poe camera
```bash
rtsp://admin:123456@192.168.50.226:554/stream1
```

vs code server
```bash
code-server /opt/robot/IRB6660_RPI5_project
```

venv
```bash
source venv/bin/activate
deactivate
```

flask preview server
```bash
sudo python3 preview_server.py
```

HSV
```bash
https://pseudopencv.site/utilities/hsvcolormask/
```