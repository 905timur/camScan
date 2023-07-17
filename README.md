# Camera Scanner and Brute Forcer

This Python script allows you to scan a target subnet for network cameras and perform a basic brute force login attempt on them. It utilizes asynchronous programming to improve the speed of the scanning process.

## Requirements

- Python 3.7+
- Requests library (`pip install requests`)
- Netaddr library (`pip install netaddr`)

## Instructions 

1. Install the required libraries if you haven't already:

```
pip install requests netaddr
```

Execute:

```
python camScan.py
```

Edit the subnet and credentials in the 'try' block as needed before executing the script:

```
target_subnet = "192.168.0.0/24"
    credentials = [('admin', 'password'), ('user', '12345')]
```

The script will perform the following tasks:

a. Scan the specified subnet for open ports (default port 80).

b. Identify network cameras based on the received data.

c. Attempt to brute force login using the provided credentials.

d. Save the discovered cameras' information in cameras.txt.
