import socket
import time
import threading

from queue import Queue

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = input('Enter the host to be scanned: ')
targetIP = socket.gethostbyname(target)
print('Starting scan on host: ', targetIP)

ports = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    109: 'POP2',
    110: 'POP3',
    115: 'SFTP',
    143: 'IMAP4',
    220: 'IMAP3',
    443: 'HTTPS',
    873: 'Rsync',
    2375: 'Docker',
    3128: 'Squid Proxy',
    3306: 'MySQL',
    5432: 'PostgreSQL',
    5900: 'VNC',
    8080: 'Webcache',
    6000: 'Windows X11',
    9200: 'AWS ElasticSearch HTTP',
    9300: 'AWS ElasticSearch',
    11371: 'PGP Keyserver',
    25565: 'Minecraft Server',
    27017: 'MongoDB',
    32400: 'Plex Media Server'
}

def search(values, search):
    for key in values:
        for v in values[key]:
            if search in v:
                return key
    return None

def portscan(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect((targetIP, port))
        if port in ports:
            with print_lock:
                print(port, '= OPEN (' + ports[port] + ')')
        else:
            with print_lock:
                print(port, '= OPEN')
        con.close()
    except:
        pass
        # with print_lock:
        #     print(port, '= CLOSED')

# Pulls worker from Queue & processes logic
def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

# Creating Queue & Threader
q = Queue()

# Amount of threads to run
for x in range(10):
    t = threading.Thread(target=threader)
    t.daemon = True # Daemon = die when main dies
    t.start()

startTime = time.time()

# Assign jobs to Threader
for worker in range(1, 2000):
    q.put(worker)

q.join()
print('\nTime taken:', time.time() - startTime)
