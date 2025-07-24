import socket
import sys
import argparse

# Timeout for socket connections (in seconds)
TIMEOUT = 1.0

def scan_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            return 'open'
        else:
            return 'closed'
    except socket.timeout:
        return 'filtered (timeout)'
    except Exception as e:
        return f'error: {e}'
    finally:
        s.close()

def main():
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('host', help='Target host to scan')
    parser.add_argument('-p', '--ports', help='Port range, e.g. 20-80', default='1-1024')
    args = parser.parse_args()

    host = args.host
    port_range = args.ports.split('-')
    try:
        start_port = int(port_range[0])
        end_port = int(port_range[1])
    except (IndexError, ValueError):
        print('Invalid port range. Use format start-end, e.g. 20-80')
        sys.exit(1)

    print(f'Scanning {host} from port {start_port} to {end_port}...')
    for port in range(start_port, end_port + 1):
        status = scan_port(host, port)
        print(f'Port {port}: {status}')

if __name__ == '__main__':
    main()
