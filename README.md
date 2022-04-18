## How to run
### Install virtualenv
```
sudo apt-get install python3-pip
```
```
sudo pip3 install virtualenv
```
```
cd $YOUR_PROJECT_DIRECTORY
```
```
virtualenv venv
```

### Activate virtualenv
```
source venv/bin/activate
```

### Install requirements
```
pip install -r requirements.txt
```

### Enable UART
```
sudo raspi-config > Interface Options > Serial Port (Enable)
'Would you like a login shell to be accessible over serial?' > No
'Would you like the serial port hardware to be enabled?' > Yes
Finish > 'Would you like to reboot now?' > Yes
```


## How to run tests
```
pytest -v tests/test_serial_send_cmd_function.py tests/test_serial_query_cmd_function.py
```

## Known issues
When you run test on local PC and using I2C Adafruit FT232H, it might occur you will have issues with DYLD_LIBRARY_PATH libusb-1.0.0.dylib
```
Issue:
Please be sure you have the latest packages running: 'pip3 install --upgrade adafruit-blinka adafruit-platformdetect
```
![Please be sure you have the latest packages running: 'pip3 install --upgrade adafruit-blinka adafruit-platformdetect](https://krzysztofbrzozowski.com/media/2022/04/18/python_pip3_install_-upgrade_adafruit-blinka_adafruit-platformdetect.png)
```
Issue:
...
    raise ValueError('No backend available')
ValueError: No backend available
```
![raise ValueError('No backend available')ValueError: No backend available](https://krzysztofbrzozowski.com/media/2022/04/18/python_no_backend_available_ft232h_adafruit.png)
```
Solution:
echo "export BLINKA_FT232H=1" >> ~/.zshrc
echo "export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"" >> ~/.zshrc
```