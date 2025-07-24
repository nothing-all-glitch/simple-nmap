# Simple Port Scanner

A lightweight and **fast** Python script to scan TCP ports on a target host and determine if they are open, closed, or filtered (e.g., by a firewall).

## Features
- **Multi-threaded scanning** for significantly faster performance
- Scans a range of ports on a specified host
- Reports port status as **open**, **closed**, or **filtered (timeout)**
- Simple command-line interface with customizable options
- Summary report showing scan time and results

## Requirements
- Python 3.x

## Usage

```sh
python3 port_scanner.py <host> [options]
```

### Options
- `<host>`: The target hostname or IP address to scan (e.g., `scanme.nmap.org` or `192.168.1.1`)
- `-p <start_port>-<end_port>`: (Optional) Port range to scan. Default is `1-1024`.
- `-t <threads>`: (Optional) Number of threads for concurrent scanning. Default is `100`.
- `-v, --verbose`: (Optional) Show all ports including closed ones (slower but detailed)

### Examples
**Fast scan** (default mode - shows only open ports and summary):
```sh
python3 port_scanner.py scanme.nmap.org -p 20-80
```

**Custom thread count** for very fast scanning:
```sh
python3 port_scanner.py scanme.nmap.org -p 1-1000 -t 200
```

**Verbose mode** (shows every port status like the original):
```sh
python3 port_scanner.py localhost -p 20-25 -v
```

**Default scan** (ports 1-1024):
```sh
python3 port_scanner.py localhost
```

## Output

### Fast Mode (Default)
Shows only open ports and a summary:
```
Scanning scanme.nmap.org from port 20 to 80 using 61 threads...
Port 22: open
Port 80: open

--- Scan Summary ---
Scan completed in 1.23 seconds
Open ports (2): [22, 80]
Filtered ports (15): 15
Closed ports: 44
```

### Verbose Mode
Shows status for each port:
```
Port 22: open
Port 23: closed
Port 80: open
Port 443: filtered (timeout)
```

## Performance
- **Multi-threaded**: Uses up to 100 threads by default for concurrent scanning
- **Fast timeouts**: 0.5-second timeout per port for quick results
- **Optimized**: Can scan 1000 ports in under 10 seconds on most networks

## Notes
- "filtered (timeout)" usually means the port is protected by a firewall or is not responding.
- Only TCP ports are scanned.
- Use fewer threads (`-t` option) if you experience network issues or want to be less aggressive.
- Default mode focuses on open ports for faster results; use `-v` for detailed output.

## License
MIT License
