import socket
import sys
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Timeout for socket connections (in seconds)
TIMEOUT = 0.5
# Number of threads for concurrent scanning
MAX_THREADS = 100

def scan_port(host, port):
    """Scan a single port on the target host"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        result = s.connect_ex((host, port))
        s.close()
        
        if result == 0:
            return port, 'open'
        else:
            return port, 'closed'
    except socket.timeout:
        return port, 'filtered (timeout)'
    except Exception as e:
        return port, f'error: {e}'

def scan_ports_threaded(host, start_port, end_port, max_threads=MAX_THREADS):
    """Scan ports using threading for faster execution"""
    open_ports = []
    closed_ports = []
    filtered_ports = []
    
    # Limit threads to avoid overwhelming the system
    thread_count = min(max_threads, end_port - start_port + 1)
    
    print(f'Scanning {host} from port {start_port} to {end_port} using {thread_count} threads...')
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        # Submit all port scan tasks
        future_to_port = {
            executor.submit(scan_port, host, port): port 
            for port in range(start_port, end_port + 1)
        }
        
        # Process completed tasks
        for future in as_completed(future_to_port):
            port, status = future.result()
            
            if status == 'open':
                open_ports.append(port)
                print(f'Port {port}: {status}')
            elif 'filtered' in status:
                filtered_ports.append(port)
            else:
                closed_ports.append(port)
    
    end_time = time.time()
    
    # Summary
    print(f'\n--- Scan Summary ---')
    print(f'Scan completed in {end_time - start_time:.2f} seconds')
    print(f'Open ports ({len(open_ports)}): {sorted(open_ports) if open_ports else "None"}')
    print(f'Filtered ports ({len(filtered_ports)}): {len(filtered_ports)}')
    print(f'Closed ports: {len(closed_ports)}')
    
    return open_ports, closed_ports, filtered_ports

def main():
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('host', help='Target host to scan')
    parser.add_argument('-p', '--ports', help='Port range, e.g. 20-80', default='1-1024')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads (default: 100)', default=MAX_THREADS)
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all ports (including closed)')
    args = parser.parse_args()

    host = args.host
    port_range = args.ports.split('-')
    try:
        start_port = int(port_range[0])
        end_port = int(port_range[1])
    except (IndexError, ValueError):
        print('Invalid port range. Use format start-end, e.g. 20-80')
        sys.exit(1)

    if args.verbose:
        # Original behavior - show all ports
        print(f'Scanning {host} from port {start_port} to {end_port}...')
        for port in range(start_port, end_port + 1):
            port_num, status = scan_port(host, port)
            print(f'Port {port_num}: {status}')
    else:
        # Fast threaded scan - show summary
        scan_ports_threaded(host, start_port, end_port, args.threads)

if __name__ == '__main__':
    main()
