This Python script scans a subnet for CCTV cameras, fingerprints them, and attempts to brute force default credentials. 

Saves discovered camera details and brute force attempts to a txt file.

Edit the subnet and credentials in the 'try' block as needed before executing the script:

```
target_subnet = "192.168.0.0/24"
    credentials = [('admin', 'password'), ('user', '12345')]
```
