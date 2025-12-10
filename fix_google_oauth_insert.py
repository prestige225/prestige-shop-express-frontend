#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction pour le problème d'insertion des utilisateurs Google OAuth
"""

import re

def fix_google_oauth_insert(file_path):
    """Corrige la requête INSERT pour les nouveaux utilisateurs Google OAuth"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver la requête INSERT problématique
    pattern = r'(INSERT INTO users\s*\(\s*nom\s*,\s*prenom\s*,\s*email\s*,\s*mot_de_passe\s*,\s*statut\s*,\s*session_active\s*\)\s*VALUES\s*\([^)]+\))'
    
    # Fonction de remplacement
    def replace_func(match):
        insert_statement = match.group(1)
        # Ajouter la valeur 1 pour session_active
        if "VALUES (" in insert_statement and not insert_statement.endswith(", 1)"):
            # Trouver la position de VALUES et insérer , 1) à la fin
            values_pos = insert_statement.rfind(')')
            if values_pos != -1:
                # Remplacer la dernière parenthèse fermante par , 1)
                fixed_statement = insert_statement[:values_pos] + ", 1" + insert_statement[values_pos:]
                return fixed_statement
        return insert_statement
    
    # Appliquer le remplacement
    fixed_content = re.sub(pattern, replace_func, content)
    
    # Écrire le contenu corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fichier {file_path} mis à jour avec succès.")

if __name__ == "__main__":
    # Chemin vers le fichier server_fixed.py
    server_file_path = r"c:\Users\RCK COMPUTERS\Desktop\prestige shop express\backend_render\server_fixed.py"
    
    print("Application de la correction...")
    fix_google_oauth_insert(server_file_path)
    print("Correction appliquée.")