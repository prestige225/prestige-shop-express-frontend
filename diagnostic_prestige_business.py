#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour diagnostiquer le problème d'affichage de 8/12 produits Prestige Business
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration DB
db_config = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def check_prestige_business_products():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        print("\n" + "="*80)
        print("🔍 DIAGNOSTIC: Produits Prestige Business")
        print("="*80 + "\n")
        
        # Voir la structure de la table
        cursor.execute("DESCRIBE produits")
        columns = cursor.fetchall()
        
        print("📋 Colonnes de la table produits:")
        for col in columns:
            print(f"  - {col}")
        
        # 1. Tous les produits avec "Business" dans la catégorie
        query1 = """
        SELECT * FROM produits 
        WHERE categorie LIKE '%Business%' OR categorie LIKE '%business%'
        ORDER BY id
        """
        cursor.execute(query1)
        all_business = cursor.fetchall()
        
        print(f"\n✅ Total de produits avec 'Business' en catégorie: {len(all_business)}\n")
        
        for i, p in enumerate(all_business, 1):
            print(f"{i}. ID: {p['id']:3} | {p['nom'][:40]:40}")
            print(f"   Catégorie: {p['categorie']}")
            print(f"   Statut: {p.get('statut', 'N/A')}")
            print()
        
        # 2. Vérifier ceux avec le statut exact
        query2 = """
        SELECT id, nom, categorie, statut, visible
        FROM produits 
        WHERE categorie = '💼 Prestige Business'
        ORDER BY id
        """
        cursor.execute(query2)
        exact_match = cursor.fetchall()
        
        print("\n" + "-"*80)
        print(f"✅ Produits avec CATÉGORIE EXACTE '💼 Prestige Business': {len(exact_match)}\n")
        for i, p in enumerate(exact_match, 1):
            print(f"{i}. ID: {p['id']:3} | {p['nom'][:40]:40} | Statut: {p['statut']:15} | Visible: {p['visible']}")
        
        # 3. Vérifier les statuts des produits non affichés
        print("\n" + "-"*80)
        print("🔧 ANALYSE DES STATUTS:\n")
        
        query3 = """
        SELECT statut, COUNT(*) as count
        FROM produits 
        WHERE categorie LIKE '%Business%'
        GROUP BY statut
        """
        cursor.execute(query3)
        status_count = cursor.fetchall()
        
        for item in status_count:
            print(f"  • Statut '{item['statut']}': {item['count']} produits")
        
        # 4. Vérifier la visibilité
        print("\n" + "-"*80)
        print("🔧 ANALYSE DE LA VISIBILITÉ:\n")
        
        query4 = """
        SELECT visible, COUNT(*) as count
        FROM produits 
        WHERE categorie LIKE '%Business%'
        GROUP BY visible
        """
        cursor.execute(query4)
        visible_count = cursor.fetchall()
        
        for item in visible_count:
            print(f"  • Visible = {item['visible']}: {item['count']} produits")
        
        # 5. Chercher les produits qui pourraient être cachés
        print("\n" + "-"*80)
        print("⚠️ PRODUITS POTENTIELLEMENT CACHÉS:\n")
        
        query5 = """
        SELECT id, nom, categorie, statut, visible
        FROM produits 
        WHERE categorie LIKE '%Business%' 
        AND (visible = 0 OR statut != 'actif' OR statut IS NULL)
        ORDER BY id
        """
        cursor.execute(query5)
        hidden = cursor.fetchall()
        
        if hidden:
            for i, p in enumerate(hidden, 1):
                print(f"{i}. ID: {p['id']:3} | {p['nom'][:40]:40} | Visible: {p['visible']} | Statut: {p['statut']}")
        else:
            print("  ✅ Aucun produit caché trouvé")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Erreur DB: {e}")

if __name__ == '__main__':
    check_prestige_business_products()
