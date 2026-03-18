#!/usr/bin/env python
# Script pour vérifier la base de données et voir les produits

import mysql.connector
from mysql.connector import Error
import json

DB_CONFIG = {
    'host': 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com',
    'user': 'usblj9n0kraq8uoc',
    'password': '4fcY691gsJlwoQnk5xwa',
    'database': 'bracv1wswmu4vsqxycku',
    'port': 3306
}

def check_database():
    """Vérifier les tables et les produits dans la base de données"""
    try:
        print("📊 Connexion à la base de données...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 1. Vérifier les tables
        print("\n📋 Vérification des tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Tables trouvées: {[table[list(table.keys())[0]] for table in tables]}")
        
        # 2. Vérifier la structure de la table produits
        print("\n🏗️ Structure de la table 'produits'...")
        cursor.execute("DESCRIBE produits")
        columns = cursor.fetchall()
        print("Colonnes:")
        for col in columns:
            print(f"  - {col['Field']}: {col['Type']}")
        
        # 3. Compter les produits
        print("\n📦 Comptage des produits...")
        cursor.execute("SELECT COUNT(*) as count FROM produits")
        count = cursor.fetchone()
        print(f"✅ Nombre de produits: {count['count']}")
        
        # 4. Afficher les premiers produits
        if count['count'] > 0:
            print("\n📋 Les 5 premiers produits:")
            cursor.execute("SELECT id, nom, categorie, prix, stock, statut FROM produits LIMIT 5")
            produits = cursor.fetchall()
            for p in produits:
                print(f"  ID: {p['id']}, Nom: {p['nom']}, Catégorie: {p['categorie']}, Prix: {p['prix']}, Stock: {p['stock']}, Statut: {p['statut']}")
        else:
            print("\n⚠️ Aucun produit trouvé dans la base de données!")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Erreur: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == '__main__':
    check_database()
