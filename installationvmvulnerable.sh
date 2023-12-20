#!/bin/bash

# Installation de SSH
sudo apt-get update
sudo apt-get install -y openssh-server

# Configuration du fichier de configuration SSH
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config
sudo sed -i 's/#UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Redémarrage du service SSH
sudo service ssh restart
# Ajout du démarrage de SSH au démarrage du système
sudo systemctl enable ssh
