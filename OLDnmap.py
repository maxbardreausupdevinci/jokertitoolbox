#It is necessary to check and change the network scanned before launching the script
#I can also set up a variable to call the script 

import os
import subprocess
import json

# Function to install necessary dependencies
def install_dependencies():
    subprocess.run(["apt-get", "install", "-y", "nmap"])

# Function to scan network for online devices
def scan_network():
    output = subprocess.run(["nmap", "-sn", "192.168.1.0/24"], capture_output=True, text=True)
    return output.stdout

# Check if Nmap is installed, if not install it
if not os.path.exists("/usr/bin/nmap"):
    install_dependencies()

# Scan the network
scan_result = scan_network()

# Extract the number of hosts from the scan output
hosts_count = scan_result.count("Nmap scan report for") - 1 # remove 1 to account for the machine running the script

# Extract IP and MAC addresses for each host
hosts = {}
lines = scan_result.split("\n")
host_index = 1
for line in lines:
    if "Nmap scan report for" in line:
        ip = line.split(" ")[-1]
    elif "MAC Address:" in line:
        mac = line.split(" ")[2]
        hosts["host"+str(host_index)] = {"ip": ip, "mac": mac}
        host_index += 1

# Prepare the final data
data = {"hosts_count": hosts_count, **hosts}

# Write the data to a JSON file
with open("scan_result.json", "w") as f:
    json.dump(data, f, indent=4)