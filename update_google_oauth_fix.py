#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction pour le problème des utilisateurs Google OAuth
dans le panneau d'administration.

Ce script corrige deux problèmes :
1. Les utilisateurs Google OAuth nouvellement créés n'ont pas leur champ 
   session_active initialisé à 1
2. La logique de vérification de session dans l'administration ne tient 
   pas compte du temps d'inactivité
"""

import re
import os

def fix_google_oauth_insert_statements(file_path):
    """Corrige les requêtes INSERT pour les utilisateurs Google OAuth"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les requêtes INSERT des utilisateurs Google OAuth
    pattern = r'(INSERT INTO users\s*\(\s*nom\s*,\s*prenom\s*,\s*email\s*,\s*mot_de_passe\s*,\s*statut\s*\)\s*VALUES\s*\([^)]+\)\s*)'
    
    # Remplacement pour inclure session_active
    def replace_func(match):
        insert_statement = match.group(1)
        # Ajouter session_active à la liste des colonnes
        fixed_statement = insert_statement.replace(
            'INSERT INTO users (nom, prenom, email, mot_de_passe, statut)',
            'INSERT INTO users (nom, prenom, email, mot_de_passe, statut, session_active)'
        )
        # Ajouter la valeur 1 pour session_active
        fixed_statement = fixed_statement.replace(
            'VALUES (',
            'VALUES ('
        ).replace(
            ');', 
            ', 1);'
        ).replace(
            '),', 
            ', 1),'
        )
        return fixed_statement
    
    # Appliquer le remplacement
    fixed_content = re.sub(pattern, replace_func, content)
    
    # Écrire le contenu corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fichier {file_path} mis à jour avec succès.")

def fix_session_check_logic(file_path):
    """Corrige la logique de vérification de session"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patterns pour les requêtes SELECT dans les routes /api/users et /api/user/<int:user_id>
    patterns = [
        (r'(SELECT id, CONCAT\(prenom, \' \', nom\) as nom_complet, email, numero, statut,\s*CASE WHEN session_active = 1 THEN \'CONNECTÉ\' ELSE \'DÉCONNECTÉ\' END as statut_connexion,\s*derniere_connexion\s*FROM users)',
         '''SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, numero, statut,
                   CASE 
                       WHEN session_active = 1 AND derniere_connexion >= DATE_SUB(NOW(), INTERVAL 30 MINUTE) THEN 'CONNECTÉ' 
                       ELSE 'DÉCONNECTÉ' 
                   END as statut_connexion,
                   derniere_connexion
            FROM users'''),
        (r'(SELECT id, nom, prenom, email, numero, statut,\s*CASE WHEN session_active = 1 THEN \'CONNECTÉ\' ELSE \'DÉCONNECTÉ\' END as statut_connexion,\s*derniere_connexion, ip_connexion, token_session\s*FROM users\s*WHERE id = %s)',
         '''SELECT id, nom, prenom, email, numero, statut,
                   CASE 
                       WHEN session_active = 1 AND derniere_connexion >= DATE_SUB(NOW(), INTERVAL 30 MINUTE) THEN 'CONNECTÉ' 
                       ELSE 'DÉCONNECTÉ' 
                   END as statut_connexion,
                   derniere_connexion, ip_connexion, token_session
            FROM users
            WHERE id = %s''')
    ]
    
    fixed_content = content
    for pattern, replacement in patterns:
        fixed_content = re.sub(pattern, replacement, fixed_content)
    
    # Écrire le contenu corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Logique de vérification de session dans {file_path} mise à jour avec succès.")

if __name__ == "__main__":
    # Chemin vers le fichier server_fixed.py
    server_file_path = r"c:\Users\RCK COMPUTERS\Desktop\prestige shop express\backend_render\server_fixed.py"
    
    if os.path.exists(server_file_path):
        print("Application des corrections...")
        fix_google_oauth_insert_statements(server_file_path)
        fix_session_check_logic(server_file_path)
        print("Toutes les corrections ont été appliquées.")
    else:
        print(f"Le fichier {server_file_path} n'existe pas.")