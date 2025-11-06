from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import requests
import json
import sys
import traceback

# Force UTF-8 pour stdout/stderr
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_ici'

# Configuration CORS
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Configuration DB
DB_CONFIG = {
    'host': 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com',
    'user': 'usblj9n0kraq8uoc',
    'password': '4fcY691gsJlwoQnk5xwa',
    'database': 'bracv1wswmu4vsqxycku',
    'port': 3306
}

def get_db_connection():
    """Créer une connexion à la base de données"""
    try:
        print("Tentative de connexion à MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connexion MySQL réussie")
        return conn
    except Error as e:
        print(f"❌ Erreur de connexion à MySQL: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return None

@app.route('/')
def index():
    return "Serveur Flask fonctionne !"

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_endpoint():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({"success": True, "message": "Serveur Flask principal fonctionne !"})

# Routes produits
@app.route('/api/produits', methods=['GET', 'OPTIONS'])
def get_produits():
    if request.method == 'OPTIONS':
        return '', 200
        
    print("🔍 Démarrage récupération produits...")
    
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Erreur: Connexion DB impossible")
            return jsonify({'success': False, 'message': 'Erreur de connexion à la base de données'}), 500

        cursor = conn.cursor(dictionary=True)
        
        print("✅ Connexion DB établie")

        # Filtres
        categorie = request.args.get('categorie')
        statut = request.args.get('statut')
        search = request.args.get('search')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        print(f"📋 Filtres reçus - categorie: {categorie}, statut: {statut}, search: {search}")

        # Construction requête
        query = "SELECT * FROM produits"
        conditions = []
        params = []

        if categorie:
            conditions.append("categorie = %s")
            params.append(categorie)
        if statut:
            conditions.append("statut = %s")
            params.append(statut)
        if search:
            conditions.append("(nom LIKE %s OR description LIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY date_creation DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        print(f"🔍 Requête SQL: {query}")
        print(f"🔢 Paramètres: {params}")

        cursor.execute(query, tuple(params))
        produits = cursor.fetchall()
        print(f"✅ {len(produits)} produits trouvés")

        # Traitement des produits
        for p in produits:
            produit_id = p.get('id', 'unknown')
            print(f"🔄 Traitement produit ID: {produit_id}")
            
            # Champs JSON
            for field in ('images_urls', 'taille_disponible', 'couleur_disponible'):
                if field in p and p[field]:
                    try:
                        p[field] = json.loads(p[field]) if isinstance(p[field], str) else p[field]
                        print(f"  ✅ {field} OK pour produit {produit_id}")
                    except Exception as e:
                        print(f"  ⚠️ Erreur {field} produit {produit_id}: {e}")
                        p[field] = []
            
            # Dates
            for date_field in ('date_creation', 'date_mise_a_jour'):
                if date_field in p and p[date_field]:
                    try:
                        p[date_field] = p[date_field].isoformat()
                    except Exception as e:
                        print(f"  ⚠️ Erreur date {date_field} produit {produit_id}: {e}")
                        p[date_field] = str(p[date_field])

        print("✅ Traitement terminé avec succès")
        return jsonify({'success': True, 'produits': produits})

    except Exception as e:
        print(f"❌ Erreur globale: {str(e)}")
        print(f"📜 Détails:\n{traceback.format_exc()}")
        return jsonify({'success': False, 'message': str(e)}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()
            print("🔒 Connexion DB fermée")

@app.route('/api/produits/<int:produit_id>', methods=['GET', 'OPTIONS'])
def get_produit(produit_id):
    if request.method == 'OPTIONS':
        return '', 200

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Erreur DB'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM produits WHERE id = %s', (produit_id,))
        produit = cursor.fetchone()
        
        if not produit:
            return jsonify({'success': False, 'message': 'Produit non trouvé'}), 404

        # Traitement JSON et dates
        for field in ('images_urls', 'taille_disponible', 'couleur_disponible'):
            if field in produit and produit[field]:
                try:
                    produit[field] = json.loads(produit[field]) if isinstance(produit[field], str) else produit[field]
                except:
                    produit[field] = []

        for date_field in ('date_creation', 'date_mise_a_jour'):
            if date_field in produit and produit[date_field]:
                try:
                    produit[date_field] = produit[date_field].isoformat()
                except:
                    produit[date_field] = str(produit[date_field])

        return jsonify({'success': True, 'produit': produit})
        
    except Exception as e:
        print(f"Erreur get_produit {produit_id}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()

@app.route('/api/produits', methods=['POST', 'OPTIONS'])
def create_produit():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    if not data or 'nom' not in data or 'prix' not in data:
        return jsonify({'success': False, 'message': 'nom et prix requis'}), 400

    try:
        nom = data.get('nom')
        description = data.get('description', '')
        prix = data.get('prix')
        categorie = data.get('categorie', '')
        image_url = data.get('image_url', '')
        images_urls = json.dumps(data.get('images_urls', []))
        taille_disponible = json.dumps(data.get('taille_disponible', []))
        couleur_disponible = json.dumps(data.get('couleur_disponible', []))
        stock = int(data.get('stock', 0))
        statut = data.get('statut', 'actif')

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Erreur DB'}), 500

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO produits 
            (nom, description, prix, categorie, image_url, images_urls, 
             taille_disponible, couleur_disponible, stock, statut, date_creation, date_mise_a_jour)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (nom, description, prix, categorie, image_url, images_urls, 
             taille_disponible, couleur_disponible, stock, statut)
        )
        conn.commit()
        produit_id = cursor.lastrowid
        
        return jsonify({'success': True, 'produit_id': produit_id}), 201
        
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"Erreur create_produit: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()

@app.route('/api/produits/<int:produit_id>', methods=['PUT', 'OPTIONS'])
def update_produit(produit_id):
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Aucune donnée'}), 400

    try:
        # Construire update dynamique
        champs = []
        valeurs = []
        
        # Champs JSON
        for key in ('images_urls', 'taille_disponible', 'couleur_disponible'):
            if key in data:
                champs.append(f"{key} = %s")
                valeurs.append(json.dumps(data[key]))
                
        # Champs texte
        for key in ('nom', 'description', 'categorie', 'image_url', 'statut'):
            if key in data:
                champs.append(f"{key} = %s")
                valeurs.append(data[key])
                
        # Champs numériques
        for key in ('prix', 'stock'):
            if key in data:
                champs.append(f"{key} = %s")
                valeurs.append(data[key])

        if not champs:
            return jsonify({'success': False, 'message': 'Aucun champ à modifier'}), 400

        # Ajouter date mise à jour
        champs.append('date_mise_a_jour = NOW()')

        # Construire et exécuter requête
        query = f"UPDATE produits SET {', '.join(champs)} WHERE id = %s"
        valeurs.append(produit_id)

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Erreur DB'}), 500

        cursor = conn.cursor()
        cursor.execute(query, tuple(valeurs))
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Produit mis à jour'})
        
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"Erreur update_produit: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()

@app.route('/api/produits/<int:produit_id>', methods=['DELETE', 'OPTIONS'])
def delete_produit(produit_id):
    if request.method == 'OPTIONS':
        return '', 200

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Erreur DB'}), 500

        cursor = conn.cursor()
        
        # Vérifier existence
        cursor.execute('SELECT id FROM produits WHERE id = %s', (produit_id,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': 'Produit non trouvé'}), 404

        # Supprimer
        cursor.execute('DELETE FROM produits WHERE id = %s', (produit_id,))
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Produit supprimé'})
        
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"Erreur delete_produit: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()

# Routes fichiers statiques
@app.route('/login.html')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/register.html')
def serve_register():
    return send_from_directory('.', 'register.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/admin.html')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/admin_produits.html')
def serve_admin_produits():
    return send_from_directory('.', 'admin_produits.html')

@app.route('/admin_commandes.html')
def serve_admin_commandes():
    return send_from_directory('.', 'admin_commandes.html')

@app.route('/test-order.html')
def serve_test_order():
    return send_from_directory('.', 'test-order.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    print("🚀 Démarrage serveur Flask...")
    
    # Test DB au démarrage
    print("🔍 Test connexion base de données...")
    conn = get_db_connection()
    if conn:
        conn.close()
        print("✅ Base de données accessible")
    else:
        print("⚠️ Base de données non accessible")
    
    print("🌐 Serveur disponible sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)