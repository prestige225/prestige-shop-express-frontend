#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic post-correction : Vérifier que quantite_minimale est bien sauvegardée
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

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
    
    print("\n" + "="*100)
    print("✅ POST-CORRECTION: Vérifier les quantités minimales des produits Prestige Business")
    print("="*100 + "\n")
    
    # Vérifier les produits Business avec leurs quantités minimales
    query = """
    SELECT id, nom, categorie, quantite_minimale, statut 
    FROM produits 
    WHERE categorie LIKE '%business%' OR categorie LIKE '%Business%'
    ORDER BY id
    """
    cursor.execute(query)
    products = cursor.fetchall()
    
    print(f"Total: {len(products)} produits Business\n")
    
    # Compter combien ont quantite_minimale > 1
    high_qty_products = [p for p in products if p['quantite_minimale'] > 1]
    
    print(f"📊 Statistiques:")
    print(f"  • Produits avec quantite_minimale = 1: {len([p for p in products if p['quantite_minimale'] == 1])}")
    print(f"  • Produits avec quantite_minimale > 1: {len(high_qty_products)}")
    print(f"\n")
    
    for i, p in enumerate(products, 1):
        badge = "✅ BADGE VISIBLE" if p['quantite_minimale'] > 1 else "❌ Pas de badge"
        print(f"{i}. ID {p['id']:3} | {p['nom'][:50]:50} | Min: {p['quantite_minimale']:3} | {badge}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*100)
    print("✅ Diagnostic terminé ! Les badges devraient maintenant s'afficher correctement.")
    print("="*100 + "\n")
    
except Error as e:
    print(f"❌ Erreur DB: {e}")
