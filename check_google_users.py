#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier l'état des utilisateurs Google OAuth
"""

import mysql.connector
import os
from datetime import datetime

def check_google_users():
    """Vérifie l'état des utilisateurs Google OAuth"""
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
            user=os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
            password=os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
            database=os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        
        cursor = conn.cursor()
        
        # Récupérer tous les utilisateurs Google OAuth
        cursor.execute("SELECT id, email, session_active, derniere_connexion FROM users WHERE mot_de_passe = '' ORDER BY id")
        results = cursor.fetchall()
        
        print("Utilisateurs Google OAuth:")
        print("=" * 80)
        for user in results:
            print(f"{user[0]}: {user[1]} - Session active: {user[2]}, Dernière connexion: {user[3]}")
        
        # Compter le nombre total d'utilisateurs Google
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = ''")
        total = cursor.fetchone()[0]
        
        # Compter le nombre d'utilisateurs Google actifs
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = '' AND session_active = 1")
        active = cursor.fetchone()[0]
        
        # Compter le nombre d'utilisateurs Google avec dernière connexion
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = '' AND derniere_connexion IS NOT NULL")
        connected = cursor.fetchone()[0]
        
        print("\nRésumé:")
        print(f"- Total utilisateurs Google OAuth: {total}")
        print(f"- Utilisateurs actifs: {active}")
        print(f"- Utilisateurs ayant déjà été connectés: {connected}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("Vérification de l'état des utilisateurs Google OAuth...")
    check_google_users()