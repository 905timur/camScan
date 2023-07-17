This Python script scans a subnet for CCTV cameras, fingerprints them, and attempts to brute force default credentials.

Sets up scanning parameters; subnet, IP queue, camera list, credentials list

Defines port scanning and banner grabbing functions to find cameras and get details

Defines a brute force function to try logging in with default creds

Defines a scan worker function to coordinate scanning an IP

Populates queue with IPs and spins up scanner threads

Scans IPs by port scanning, banner grabbing, and brute forcing

Saves discovered camera details and brute force attempts to a file

Edit the following subnet and credentials as needed before executing the script:

```
target_subnet = "192.168.0.0/24"
    credentials = [('admin', 'password'), ('user', '12345')]
```
