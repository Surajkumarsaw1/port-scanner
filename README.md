
# Network Port Scanner

![License](https://img.shields.io/github/license/Surajkumarsaw1/port-scanner)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Detailed Documentation](#detailed-documentation)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Contact](#contact)

## Introduction
The Network Port Scanner is a Python-based tool designed to scan a network range for open ports using multithreading and multiprocessing. It efficiently identifies open ports on specified IP addresses, making it ideal for network administrators and security professionals.

## Features
- Multithreaded port scanning for faster results.
- Multiprocessing to leverage multiple CPU cores.
- Configurable timeout and maximum workers.
- Detailed logging of scan results and errors.
- Option to save scan results to a file in JSON format.

## Installation
To install and set up the project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/Surajkumarsaw1/port-scanner.git
cd port-scanner

# Install dependencies
# no additional package needed
# pip install -r requirements.txt
```

## Usage
Examples of how to use the project:

### Run the Python Script Directly
To run the script directly, use the following command:
```bash
python port_scanner.py
```
You will be prompted to enter the IP range, port range, number of processes, and number of workers.

### Using as a Module
```python
# Example usage
from port_scanner import NetworkScanner, divide_ports

ip_range = '192.168.1.0/24'
ports = list(range(1, 1025))
num_processes = 4
max_workers = 10

# Divide ports into chunks
port_ranges = divide_ports(ports, num_processes)

# Initialize network scanner
network_scanner = NetworkScanner(ip_range, ports, num_processes, max_workers)

# Scan network
open_ports, errors = network_scanner.scan_network(port_ranges)

# Print results
for ip, ports in open_ports.items():
    print(f"IP: {ip}, Open Ports: {ports}")
```

## Configuration
Configuration options include:
- `timeout` (int): Timeout for the socket connection in seconds. Default is 1 second.
- `max_workers` (int): Maximum number of threads to use. Default is 100.

## Screenshots
![Example Screenshot](path/to/screenshot.png)

## Detailed Documentation
Detailed documentation for the project's classes and functions:

### `PortScanner` Class
- **Methods:**
  - `scan_port(ip: str, port: int) -> tuple`: Scans a specific port on a given IP address.
  - `scan_ports(ip: str, ports: list, max_workers: int) -> tuple`: Scans multiple ports on a given IP address using multithreading.

### `NetworkScanner` Class
- **Methods:**
  - `_scan_ip(ip: str, port_range: list) -> tuple`: Private method to scan a single IP address with a specified port range.
  - `scan_network(port_ranges: list) -> tuple`: Scans the entire network range for open ports using multiprocessing.

### Helper Functions
- `divide_ports(ports: list, num_chunks: int) -> list`: Divides a list of ports into smaller chunks.
- `calculate_optimal_chunks(ports: list) -> int`: Calculates the optimal number of chunks for dividing the port list based on the CPU count.

## Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Roadmap
- Add support for scanning UDP ports.
- Implement a GUI for easier usage.
- Enhance logging to include more detailed scan statistics.

## FAQ
**Q: How can I specify a custom port range?**
A: You can specify a port range using the format `start:end` or provide a comma-separated list of ports.

**Q: Can I save the scan results to a file?**
A: Yes, you can save the results to a JSON file by following the prompts after the scan completes.

## Acknowledgements
- [socket](https://docs.python.org/3/library/socket.html) for network communication.
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) for multithreading and multiprocessing.
- [logging](https://docs.python.org/3/library/logging.html) for logging scan results and errors.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
For questions or support, please contact [Me](https://dsa.pythonanywhere.com/contact).
