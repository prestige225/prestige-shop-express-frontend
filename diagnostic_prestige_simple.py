#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour diagnostiquer les produits Prestige Business
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

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    print("\n" + "="*90)
    print("🔍 DIAGNOSTIC: Produits Prestige Business")
    print("="*90 + "\n")
    
    # Tous les produits avec "Business" dans la catégorie
    query = """
    SELECT * FROM produits 
    WHERE categorie LIKE '%Business%' OR categorie LIKE '%business%'
    ORDER BY id
    """
    cursor.execute(query)
    all_business = cursor.fetchall()
    
    print(f"✅ Total de produits avec 'Business' en catégorie: {len(all_business)}\n")
    
    for i, p in enumerate(all_business, 1):
        print(f"{i}. ID: {p['id']:3} | {p['nom'][:50]:50}")
        print(f"   Catégorie: {p['categorie']}")
        print(f"   Statut: {p.get('statut', 'N/A')}")
        print()
    
    # Comptage par catégorie exacte
    print("\n" + "-"*90)
    query2 = """
    SELECT COUNT(*) as count FROM produits 
    WHERE categorie = '💼 Prestige Business'
    """
    cursor.execute(query2)
    result = cursor.fetchone()
    print(f"✅ Produits avec catégorie EXACTE '💼 Prestige Business': {result['count']}\n")
    
    # Compter par différentes variantes de Business
    print("-"*90)
    query3 = """
    SELECT DISTINCT categorie FROM produits 
    WHERE categorie LIKE '%usiness%'
    ORDER BY categorie
    """
    cursor.execute(query3)
    categories = cursor.fetchall()
    print(f"Variantes de catégories avec 'usiness':\n")
    for cat in categories:
        cursor.execute("SELECT COUNT(*) as count FROM produits WHERE categorie = %s", (cat['categorie'],))
        count = cursor.fetchone()['count']
        print(f"  • '{cat['categorie']}': {count} produits")
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"❌ Erreur DB: {e}")
