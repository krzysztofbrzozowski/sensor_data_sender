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
pytest -v  tests/test_serial_query_cmd_function.py tests/test_serial_send_cmd_function.py
```