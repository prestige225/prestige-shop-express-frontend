#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'analyse des utilisateurs Google OAuth
"""

import mysql.connector
import os
from datetime import datetime

def analyze_google_users():
    """Analyse les utilisateurs Google OAuth"""
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
        
        # Compter le nombre total d'utilisateurs Google
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = ''")
        total_google_users = cursor.fetchone()[0]
        print(f"Nombre total d'utilisateurs Google: {total_google_users}")
        
        # Compter le nombre d'utilisateurs Google avec session active
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = '' AND session_active = 1")
        active_google_users = cursor.fetchone()[0]
        print(f"Nombre d'utilisateurs Google actifs: {active_google_users}")
        
        # Compter le nombre d'utilisateurs Google avec dernière connexion
        cursor.execute("SELECT COUNT(*) FROM users WHERE mot_de_passe = '' AND derniere_connexion IS NOT NULL")
        connected_google_users = cursor.fetchone()[0]
        print(f"Nombre d'utilisateurs Google ayant déjà été connectés: {connected_google_users}")
        
        # Lister les utilisateurs Google sans connexion réussie
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion 
            FROM users 
            WHERE mot_de_passe = '' AND (derniere_connexion IS NULL OR session_active = 0)
            ORDER BY id
        """)
        inactive_users = cursor.fetchall()
        
        print("\nUtilisateurs Google sans connexion réussie:")
        print("=" * 80)
        for user in inactive_users:
            print(f"ID: {user[0]}, Nom: {user[1]} {user[2]}, Email: {user[3]}, Statut: {user[4]}, Session active: {user[5]}, Dernière connexion: {user[6]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    print("Analyse des utilisateurs Google OAuth...")
    analyze_google_users()