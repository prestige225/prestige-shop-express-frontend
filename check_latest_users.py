#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier les derniers utilisateurs créés
"""

import mysql.connector
import os
from datetime import datetime

def check_latest_users():
    """Vérifie les derniers utilisateurs créés"""
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host='bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com',
            user='usblj9n0kraq8uoc',
            password='4fcY691gsJlwoQnk5xwa',
            database='bracv1wswmu4vsqxycku',
            port=3306
        )
        
        cursor = conn.cursor()
        
        # Récupérer les 5 derniers utilisateurs
        cursor.execute("SELECT id, email, statut, session_active, derniere_connexion FROM users ORDER BY id DESC LIMIT 5")
        results = cursor.fetchall()
        
        print("5 derniers utilisateurs:")
        print("=" * 100)
        for user in results:
            print(f"{user[0]}: {user[1]} - Statut: {user[2]}, Session active: {user[3]}, Dernière connexion: {user[4]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("Vérification des derniers utilisateurs créés...")
    check_latest_users()