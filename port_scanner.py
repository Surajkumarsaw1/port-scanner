import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import logging
import json
import multiprocessing
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PortScanner:
    """
    A class to scan ports on a given IP address.

    Attributes:
        timeout (int): The timeout for socket connection in seconds.
    """

    def __init__(self, timeout: int = 1):
        """
        Initializes the PortScanner with a specified timeout.

        Args:
            timeout (int): Timeout for the socket connection. Default is 1 second.
        """
        self.timeout = timeout

    def scan_port(self, ip: str, port: int) -> tuple:
        """
        Scans a specific port on a given IP address.

        Args:
            ip (str): The IP address to scan.
            port (int): The port number to scan.

        Returns:
            tuple: A tuple containing a boolean indicating if the port is open and an error message if any.
        """
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(self.timeout)
        try:
            scanner.connect((ip, port))
            logging.info(f"Open port found: {ip}:{port}")
            return True, None
        except (socket.timeout, ConnectionRefusedError):
            logging.debug(f"Closed port found: {ip}:{port}")
            return False, None
        except Exception as e:
            logging.error(f"Error scanning port {port} on {ip}: {e}")
            return False, str(e)
        finally:
            scanner.close()

    def scan_ports(self, ip: str, ports: list, max_workers: int) -> tuple:
        """
        Scans multiple ports on a given IP address using multithreading.

        Args:
            ip (str): The IP address to scan.
            ports (list): A list of port numbers to scan.
            max_workers (int): The maximum number of threads to use.

        Returns:
            tuple: A tuple containing a list of open ports and a list of errors.
        """
        open_ports = []
        errors = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.scan_port, ip, port): port for port in ports}
            for future in futures:
                port = futures[future]
                try:
                    is_open, error = future.result()
                    if is_open:
                        open_ports.append(port)
                    if error:
                        errors.append((port, error))
                except Exception as e:
                    logging.error(f"Error retrieving scan result for {ip}: {e}")
                    errors.append((port, str(e)))
        return open_ports, errors


class NetworkScanner:
    """
    A class to scan a network range for open ports.

    Attributes:
        ip_range (str): The IP range to scan.
        ports (list): A list of port numbers to scan.
        max_workers (int): The maximum number of threads to use.
    """

    def __init__(self, ip_range: str, ports: list, num_processes: int, max_workers: int):
        """
        Initializes the NetworkScanner with a specified IP range, ports, and maximum workers.

        Args:
            ip_range (str): The IP range to scan.
            ports (list): A list of port numbers to scan.
            max_workers (int): The maximum number of threads to use.
        """
        self.ip_range = ip_range
        self.ports = ports
        self.num_processes = num_processes
        self.max_workers = max_workers
        self.port_scanner = PortScanner()
        logging.debug(f"Initialized NetworkScanner with IP range: {ip_range}, Ports: {ports}, Max workers: {max_workers}")

    def _scan_ip(self, ip: str, port_range: list) -> tuple:
        """
        Private method to scan a single IP address with a specified port range.

        Args:
            ip (str): The IP address to scan.
            port_range (list): A list of port numbers to scan.

        Returns:
            tuple: A tuple containing a list of open ports and a list of errors.
        """
        logging.debug(f"Scanning IP {ip} with port range {port_range}")
        open_ports, errors = self.port_scanner.scan_ports(ip, port_range, self.max_workers)
        return open_ports, errors

    def scan_network(self, port_ranges: list) -> tuple:
        """
        Scans the entire network range for open ports using multiprocessing.

        Args:
            port_ranges (list): A list of port ranges to divide the scanning work.

        Returns:
            tuple: A tuple containing a dictionary of open ports and a dictionary of errors.
        """
        network = ipaddress.ip_network(self.ip_range)
        open_ports_dict = {}
        errors_dict = {}

        # num_processes = max(1, multiprocessing.cpu_count() // 2)
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            futures = {executor.submit(self._scan_ip, str(ip), port_range): (str(ip), port_range) for ip in network.hosts() for port_range in port_ranges}
            for future in futures:
                ip, port_range = futures[future]
                try:
                    open_ports, errors = future.result()
                    if open_ports:
                        logging.info(f"Open ports for {ip}: {open_ports}")
                        if ip not in open_ports_dict:
                            open_ports_dict[ip] = []
                        open_ports_dict[ip].extend(open_ports)
                    if errors:
                        logging.error(f"Errors for {ip}: {errors}")
                        if ip not in errors_dict:
                            errors_dict[ip] = []
                        errors_dict[ip].extend(errors)
                except Exception as e:
                    logging.error(f"Error retrieving scan result for {ip}: {e}")

        return open_ports_dict, errors_dict


def divide_ports(ports: list, num_chunks: int) -> list:
    """
    Divides a list of ports into smaller chunks.

    Args:
        ports (list): A list of port numbers to divide.
        num_chunks (int): The number of chunks to divide the ports into.

    Returns:
        list: A list of port number lists divided into the specified number of chunks.
    """
    if num_chunks > len(ports):
        num_chunks = len(ports)
    chunk_size = len(ports) // num_chunks
    return [ports[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)] + [ports[num_chunks * chunk_size:]]


def calculate_optimal_chunks(ports: list) -> int:
    """
    Calculates the optimal number of chunks for dividing the port list based on the CPU count.

    Args:
        ports (list): A list of port numbers.

    Returns:
        int: The optimal number of chunks.
    """
    cpu_count = multiprocessing.cpu_count()
    return max(1, cpu_count // 2)


def main():
    """
    The main function to execute the network port scanning.
    """
    try:
        # Default values
        default_ip_range = '127.0.0.1/32'
        default_ports = "1:65535"

        # User input with defaults
        ip_range = input(f"Enter IP range (default {default_ip_range}): ") or default_ip_range
        port_range_input = input(f"Enter port range as start:end or comma-separated values (default {default_ports}): ") or default_ports

        # num_processes = max(1, multiprocessing.cpu_count() // 2)
        # num_processes = max(1, multiprocessing.cpu_count())
        num_processes = max(1, multiprocessing.cpu_count())
        num_processes_input = input(f"Enter the number of max process (default {num_processes}): ")
        num_processes = int(num_processes_input) if num_processes_input else num_processes

        max_workers = 100
        max_workers_input = input(f"Enter the number of max workers (default {max_workers}): ")
        max_workers = int(max_workers_input) if max_workers_input else max_workers

        # Parse port range input
        if ':' in port_range_input:
            port_start, port_end = map(int, port_range_input.split(':'))
            ports = list(range(port_start, port_end + 1))
        elif ',' in port_range_input:
            ports = list(map(int, port_range_input.split(',')))
        else:
            try:
                ports = [int(port_range_input)]
            except ValueError:
                ports = list(range(1, 65536))  # Use full range if input is invalid

        # Save the original port input
        original_ports_input = port_range_input

        # Calculate number of chunks (equals number of processes)
        # num_chunks = calculate_optimal_chunks(ports)
        num_chunks = num_processes

        # Divide ports into chunks
        port_ranges = divide_ports(ports, num_chunks)
        logging.info(f"Port ranges divided into {num_chunks} chunks")

        # Initialize network scanner
        network_scanner = NetworkScanner(ip_range, ports, num_processes, max_workers)

        # Start timing
        start_time = time.time()
        logging.info("Starting network scan")

        # Scan network
        open_ports, errors = network_scanner.scan_network(port_ranges)

        # End timing
        end_time = time.time()
        time_taken = end_time - start_time

        # Print results
        for ip, ports in open_ports.items():
            print(f"IP: {ip}, Open Ports: {ports}")

        # Print time taken
        logging.info(f"Time taken: {time_taken:.2f} seconds")

        # Ask user if they want to save the results
        save_results = input("Do you want to save the results to a file? (YES/no): ").strip().lower()
        if (save_results == 'yes') or not save_results:
            filename = input("Enter the filename (or press enter for default name): ").strip()
            if not filename:
                filename = f"scan_{ip_range.replace('/', '_')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{str(uuid.uuid4())[:8]}.json"
            results = {
                'Network': ip_range,
                'Ports': original_ports_input,
                'Number of Chunks': num_chunks,
                'Max Workers': max_workers,
                'Open Ports': open_ports,
                'Errors': errors,
                'Time Taken': time_taken
            }
            try:
                with open(filename, 'w') as file:
                    json.dump(results, file, indent=4)
                logging.info(f"Results saved to {filename}")
            except IOError as e:
                logging.error(f"Failed to save results to {filename}: {e}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
