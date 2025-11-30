import socket
import threading
from queue import Queue
import time

# Configuration
TARGET = "127.0.0.1"  # Scanning localhost for demo purposes
QUEUE = Queue()
OPEN_PORTS = []

def port_scan(port):
    """
    Attempts to connect to a specific port. 
    If successful, the port is open.
    """
    try:
        sock = socket.socket(socket.socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Fast timeout for speed
        result = sock.connect_ex((TARGET, port))
        if result == 0:
            OPEN_PORTS.append(port)
        sock.close()
    except:
        pass

def threader():
    """
    Worker thread that pulls ports from the queue and scans them.
    """
    while True:
        worker = QUEUE.get()
        port_scan(worker)
        QUEUE.task_done()

def run_scanner():
    print(f"Starting scan on host: {TARGET}")
    start_time = time.time()
    
    # Spin up 100 threads for high concurrency
    for _ in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()
        
    # Scan ports 1 through 1000
    for worker in range(1, 1001):
        QUEUE.put(worker)
        
    QUEUE.join()
    
    print(f"Scan completed in {time.time() - start_time:.2f} seconds")
    print(f"Open Ports: {OPEN_PORTS}")

if __name__ == '__main__':
    run_scanner()
