#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error
import os

# Configuration de la base de données
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def execute_migration():
    """Exécute la migration pour ajouter les colonnes recommande et moment"""
    try:
        print("🔗 Connexion à la base de données Clever Cloud...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connexion réussie!\n")

        # Ajouter la colonne recommande
        print("➕ Ajout de la colonne 'recommande'...")
        try:
            cursor.execute("""
                ALTER TABLE produits 
                ADD COLUMN recommande INT DEFAULT 0 
                COMMENT 'Produit recommandé (0 ou 1)'
            """)
            print("✅ Colonne 'recommande' créée\n")
        except Error as col_error:
            if "Duplicate column name" in str(col_error):
                print("⚠️  Colonne 'recommande' déjà existe\n")
            else:
                raise col_error

        # Ajouter la colonne moment
        print("➕ Ajout de la colonne 'moment'...")
        try:
            cursor.execute("""
                ALTER TABLE produits 
                ADD COLUMN moment INT DEFAULT 0 
                COMMENT 'Produit du moment (0 ou 1)'
            """)
            print("✅ Colonne 'moment' créée\n")
        except Error as col_error:
            if "Duplicate column name" in str(col_error):
                print("⚠️  Colonne 'moment' déjà existe\n")
            else:
                raise col_error

        # Vérifier la structure
        print("🔍 Vérification de la structure...")
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_DEFAULT, IS_NULLABLE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'produits' 
            AND COLUMN_NAME IN ('recommande', 'moment')
            ORDER BY ORDINAL_POSITION
        """)
        
        results = cursor.fetchall()
        print("\n📋 Colonnes vérifiées:")
        for row in results:
            print(f"   • {row[0]}: {row[1]} (défaut: {row[2]}, nullable: {row[3]})")

        conn.commit()
        print("\n✅ Migration completed successfully! ✅")
        cursor.close()
        conn.close()

    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == '__main__':
    execute_migration()
