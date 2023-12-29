#!/bin/bash

# Chemin du répertoire du clone GitHub sur votre machine
REP_GITHUB="/jokertitoolbox"

# Aller dans le répertoire du clone
cd $REP_GITHUB

# Mettre à jour le dépôt local
git pull

# Vérifier si la mise à jour a réussi
if [ $? -eq 0 ]; then
    echo "Le dépôt a été mis à jour avec succès."
else
    echo "Erreur lors de la mise à jour du dépôt. Assurez-vous que Git est installé et que le chemin du dépôt est correct."
fi
