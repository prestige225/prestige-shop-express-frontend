#!/usr/bin/env python3
"""
Script de test - Marquer quelques produits comme recommandés et du moment
"""
import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def mark_products_as_recommended():
    """Marque les 5 premiers produits comme recommandés"""
    try:
        print("🔗 Connexion à la base de données...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connecté!\n")

        # Récupérer les IDs des 5 premiers produits
        print("⭐ Marquage des 5 premiers produits comme recommandés...")
        cursor.execute("SELECT id FROM produits ORDER BY ordre ASC, date_creation DESC LIMIT 5")
        top_5_ids = [row[0] for row in cursor.fetchall()]
        print(f"   IDs trouvés: {top_5_ids}")
        
        for prod_id in top_5_ids:
            cursor.execute("UPDATE produits SET recommande = 1 WHERE id = %s", (prod_id,))
        print(f"✅ {len(top_5_ids)} produits marqués comme recommandés\n")

        # Récupérer les IDs des 5 suivants
        print("🔥 Marquage de 5 autres produits comme produits du moment...")
        cursor.execute("SELECT id FROM produits ORDER BY ordre ASC, date_creation DESC LIMIT 5 OFFSET 5")
        next_5_ids = [row[0] for row in cursor.fetchall()]
        print(f"   IDs trouvés: {next_5_ids}")
        
        for prod_id in next_5_ids:
            cursor.execute("UPDATE produits SET moment = 1 WHERE id = %s", (prod_id,))
        print(f"✅ {len(next_5_ids)} produits marqués comme du moment\n")

        # Vérifier les résultats
        print("🔍 Vérification...")
        cursor.execute("SELECT id, nom, recommande, moment FROM produits WHERE recommande = 1 OR moment = 1 LIMIT 10")
        results = cursor.fetchall()
        
        print(f"\n📋 Produits marqués ({len(results)}):")
        for row in results:
            status = []
            if row[2] == 1:
                status.append("⭐ Recommandé")
            if row[3] == 1:
                status.append("🔥 Moment")
            print(f"   • ID {row[0]:3d}: {row[1]:40s} | {', '.join(status)}")

        conn.commit()
        print("\n✅ Test completed successfully! ✅")
        cursor.close()
        conn.close()

    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    mark_products_as_recommended()
