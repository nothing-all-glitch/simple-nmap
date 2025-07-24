# Simple Port Scanner

A lightweight Python script to scan TCP ports on a target host and determine if they are open, closed, or filtered (e.g., by a firewall).

## Features
- Scans a range of ports on a specified host
- Reports port status as **open**, **closed**, or **filtered (timeout)**
- Simple command-line interface

## Requirements
- Python 3.x

## Usage

```sh
python3 port_scanner.py <host> -p <start_port>-<end_port>
```

- `<host>`: The target hostname or IP address to scan (e.g., `scanme.nmap.org` or `192.168.1.1`)
- `-p <start_port>-<end_port>`: (Optional) Port range to scan. Default is `1-1024`.

### Examples
Scan ports 20 to 25 on `scanme.nmap.org`:
```sh
python3 port_scanner.py scanme.nmap.org -p 20-25
```

Scan default ports 1 to 1024 on `localhost`:
```sh
python3 port_scanner.py localhost
```

## Output
For each port, the script prints its status:
```
Port 22: open
Port 23: closed
Port 80: filtered (timeout)
```

## Notes
- "filtered (timeout)" usually means the port is protected by a firewall or is not responding.
- Only TCP ports are scanned.

## License
MIT License
