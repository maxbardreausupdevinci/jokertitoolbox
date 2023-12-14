import os
import subprocess
import json

# Function to install necessary dependencies
def install_dependencies():
    subprocess.run(["apt-get", "install", "-y", "nmap"])

# Function to scan IP for open ports, services, and CVEs
def scan_ip(ip):
    output = subprocess.run(["nmap", "-p-", "-sV", "--script", "vulners", ip], capture_output=True, text=True)
    return output.stdout

# Check if Nmap is installed, if not install it
if not os.path.exists("/usr/bin/nmap"):
    install_dependencies()

# Get the IP address from user input
ip = input("Enter the IP address to scan: ")

# Scan the IP for open ports, services, and CVEs
scan_result = scan_ip(ip)

# Extract the open ports, services, and CVEs from the scan output
open_ports = []
services = []
cves = []
lines = scan_result.split("\n")
for line in lines:
    if "/tcp" in line or "/udp" in line:
        port = line.split("/")[0]
        open_ports.append(port)
    elif "Service Info" in line:
        service = line.split(":")[1].strip()
        services.append(service)
    elif "CVE" in line:
        cve = line.split(":")[1].strip()
        cves.append(cve)

# Prepare the final data
data = {"IP": ip, "Open Ports": open_ports, "Services": services, "CVEs": cves}

# Write the data to a JSON file
with open("scan_result.json", "w") as f:
    json.dump(data, f, indent=4)