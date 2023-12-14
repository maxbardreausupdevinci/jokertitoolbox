import subprocess
import os
import sys
# Vérification de toutes les dépendances nécessaires à l'exécution du script

def update_apt():
    subprocess.call(["sudo", "apt", "update"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def install_pip():
    try:
        # Check if pip is installed
        subprocess.check_output(["pip", "--version"])
    except subprocess.CalledProcessError:
        # Install pip using apt
        print("pip non trouvé, installation en cours...")
        update_apt()
        subprocess.call(["sudo", "apt", "install", "python3-pip", "-y"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("ok")

def install_nmap():
    try:
        # Check if nmap is installed
        subprocess.check_output(["nmap", "--version"])
    except FileNotFoundError:
        # Install nmap using apt
        print("Nmap non trouvé, installation en cours...")
        update_apt()
        subprocess.call(["sudo", "apt", "install", "nmap", "-y"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("ok")

def install_paramiko():
    try:
        # Check if paramiko is installed
        subprocess.check_output(["python3", "-c", "import paramiko"])
    except subprocess.CalledProcessError:
        # Install paramiko using apt
        print("Paramiko (SSH) non trouvé, installation en cours...")
        update_apt()
        subprocess.call(["sudo", "apt", "install", "python3-paramiko", "-y"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("ok")

# Installation des dépendances
install_nmap()
install_pip()
install_paramiko()
