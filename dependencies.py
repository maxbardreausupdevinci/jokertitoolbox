import subprocess
# Vérification de toutes les dépendances nécessaires à l'exécution du script

def update_apt():
    subprocess.call(["sudo", "apt", "update"])

def install_pip():
    try:
        # Check if pip is installed
        subprocess.check_output(["pip", "--version"])
    except subprocess.CalledProcessError:
        # Install pip using apt
        subprocess.call(["sudo", "apt", "install", "python3-pip"])

def install_nmap():
    try:
        # Check if nmap is installed
        subprocess.check_output(["nmap", "--version"])
    except subprocess.CalledProcessError:
        # Install nmap using apt
        subprocess.call(["sudo", "apt", "install", "nmap"]) 

def install_paramiko():
    try:
        # Check if paramiko is installed
        subprocess.check_output(["python3", "-c", "import paramiko"])
    except subprocess.CalledProcessError:
        # Install paramiko using apt
        subprocess.call(["sudo", "apt", "install", "python3-paramiko"])


# Mise à jour des paquets
update_apt()

# Installation des dépendances
install_nmap()
install_pip()
install_paramiko()
