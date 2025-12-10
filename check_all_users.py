#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier l'état de tous les utilisateurs
"""

import mysql.connector
import os
from datetime import datetime

def check_all_users():
    """Vérifie l'état de tous les utilisateurs"""
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
        
        # Récupérer tous les utilisateurs
        cursor.execute("SELECT id, email, statut, session_active, derniere_connexion FROM users ORDER BY id")
        results = cursor.fetchall()
        
        print("Tous les utilisateurs:")
        print("=" * 100)
        for user in results:
            print(f"{user[0]}: {user[1]} - Statut: {user[2]}, Session active: {user[3]}, Dernière connexion: {user[4]}")
        
        # Compter le nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        
        # Compter le nombre d'utilisateurs actifs
        cursor.execute("SELECT COUNT(*) FROM users WHERE session_active = 1")
        active = cursor.fetchone()[0]
        
        # Compter le nombre d'utilisateurs avec dernière connexion
        cursor.execute("SELECT COUNT(*) FROM users WHERE derniere_connexion IS NOT NULL")
        connected = cursor.fetchone()[0]
        
        print("\nRésumé:")
        print(f"- Total utilisateurs: {total}")
        print(f"- Utilisateurs actifs: {active}")
        print(f"- Utilisateurs ayant déjà été connectés: {connected}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("Vérification de l'état de tous les utilisateurs...")
    check_all_users()