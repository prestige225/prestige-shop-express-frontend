# Mise à jour du serveur Flask pour gérer les attributs de produits

# 1. Ajout des routes pour gérer les attributs de produits

from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

# Route pour obtenir les attributs d'un produit
@app.route('/api/produits/<int:produit_id>/attributs', methods=['GET', 'OPTIONS'])
def get_produit_attributs(produit_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM produit_attributs 
            WHERE produit_id = %s 
            ORDER BY couleur, taille
        """
        cursor.execute(query, (produit_id,))
        attributs = cursor.fetchall()
        
        return jsonify({"success": True, "data": attributs})
        
    except Error as e:
        print(f"Erreur lors de la récupération des attributs: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route pour obtenir les tailles disponibles pour un produit et une couleur
@app.route('/api/produits/<int:produit_id>/couleurs/<couleur>/tailles', methods=['GET', 'OPTIONS'])
def get_tailles_disponibles(produit_id, couleur):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT taille, stock 
            FROM produit_attributs 
            WHERE produit_id = %s AND couleur = %s AND stock > 0
            ORDER BY taille
        """
        cursor.execute(query, (produit_id, couleur))
        tailles = cursor.fetchall()
        
        return jsonify({"success": True, "data": tailles})
        
    except Error as e:
        print(f"Erreur lors de la récupération des tailles: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route pour obtenir les couleurs disponibles pour un produit et une taille
@app.route('/api/produits/<int:produit_id>/tailles/<taille>/couleurs', methods=['GET', 'OPTIONS'])
def get_couleurs_disponibles(produit_id, taille):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT couleur, stock 
            FROM produit_attributs 
            WHERE produit_id = %s AND taille = %s AND stock > 0
            ORDER BY couleur
        """
        cursor.execute(query, (produit_id, taille))
        couleurs = cursor.fetchall()
        
        return jsonify({"success": True, "data": couleurs})
        
    except Error as e:
        print(f"Erreur lors de la récupération des couleurs: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route pour vérifier la disponibilité d'un attribut spécifique
@app.route('/api/produits/<int:produit_id>/disponibilite', methods=['POST', 'OPTIONS'])
def verifier_disponibilite(produit_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    
    if 'couleur' not in data or 'taille' not in data:
        return jsonify({"success": False, "message": "Couleur et taille sont requis"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT stock 
            FROM produit_attributs 
            WHERE produit_id = %s AND couleur = %s AND taille = %s
            LIMIT 1
        """
        cursor.execute(query, (produit_id, data['couleur'], data['taille']))
        result = cursor.fetchone()
        
        disponible = False
        stock = 0
        if result and result['stock'] > 0:
            disponible = True
            stock = result['stock']
        
        return jsonify({
            "success": True, 
            "disponible": disponible,
            "stock": stock
        })
        
    except Error as e:
        print(f"Erreur lors de la vérification de disponibilité: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

# 2. Modification de la route de création de commande pour gérer les attributs

# Modification de la route /api/commandes POST
@app.route('/api/commandes', methods=['POST', 'OPTIONS'])
def creer_commande():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    
    # Get user_id from request body or session
    user_id = data.get('user_id') or session.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "message": "Non authentifié"}), 401
    
    # Validation des données requises
    required_fields = ['montant_total', 'adresse_livraison', 'telephone']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"Le champ {field} est requis"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor()
        
        # Générer un numéro de commande unique
        from datetime import datetime
        import random
        import json
        numero_commande = f"CMD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Extraire les noms de produits et détails complets
        produits_str = ''
        produits_details_json = None
        if 'produits' in data and data['produits']:
            produits_list = data['produits']
            # Format texte pour affichage simple
            produits_str = ', '.join([f"{p['nom']} (x{p['quantite']})" for p in produits_list])
            # Stocker les détails complets en JSON
            produits_details_json = json.dumps(produits_list, ensure_ascii=False)
        
        # Insérer la commande
        query = """
            INSERT INTO commandes 
            (user_id, numero_commande, montant_total, adresse_livraison, telephone, produits, produits_details, notes, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'en_attente')
        """
        cursor.execute(query, (
            user_id,
            numero_commande,
            data['montant_total'],
            data['adresse_livraison'],
            data['telephone'],
            produits_str,
            produits_details_json,
            data.get('notes', '')
        ))
        
        commande_id = cursor.lastrowid
        
        # Si des attributs de produits sont fournis, les mettre à jour
        if 'produits_attributs' in data and data['produits_attributs']:
            for produit_attr in data['produits_attributs']:
                # Mettre à jour le stock des attributs
                update_query = """
                    UPDATE produit_attributs 
                    SET stock = stock - %s 
                    WHERE produit_id = %s AND couleur = %s AND taille = %s
                """
                cursor.execute(update_query, (
                    produit_attr['quantite'],
                    produit_attr['produit_id'],
                    produit_attr['couleur'],
                    produit_attr['taille']
                ))
        
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": "Commande créée avec succès",
            "commande_id": commande_id,
            "numero_commande": numero_commande
        })
        
    except Error as e:
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
        print(f"Erreur lors de la création de la commande: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# 3. Ajout d'une route pour obtenir tous les produits avec leurs attributs
@app.route('/api/produits/complets', methods=['GET', 'OPTIONS'])
def get_produits_complets():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                p.id as produit_id,
                p.name as nom_produit,
                p.price as prix_base,
                p.category as categorie,
                p.subcategory as sous_categorie,
                p.images,
                p.description,
                pa.id as attribut_id,
                pa.couleur,
                pa.taille,
                pa.stock,
                (p.price + pa.prix_additionnel) as prix_final,
                pa.image_url
            FROM commandes p
            LEFT JOIN produit_attributs pa ON p.id = pa.produit_id
            ORDER BY p.id, pa.couleur, pa.taille
        """
        cursor.execute(query)
        produits = cursor.fetchall()
        
        # Regrouper les attributs par produit
        produits_groupes = {}
        for row in produits:
            produit_id = row['produit_id']
            if produit_id not in produits_groupes:
                produits_groupes[produit_id] = {
                    'id': row['produit_id'],
                    'name': row['nom_produit'],
                    'price': float(row['prix_base']),
                    'category': row['categorie'],
                    'subcategory': row['sous_categorie'],
                    'images': row['images'].split(',') if row['images'] else [],
                    'description': row['description'],
                    'attributs': []
                }
            
            if row['attribut_id']:
                produits_groupes[produit_id]['attributs'].append({
                    'id': row['attribut_id'],
                    'couleur': row['couleur'],
                    'taille': row['taille'],
                    'stock': row['stock'],
                    'prix_final': float(row['prix_final']),
                    'image_url': row['image_url']
                })
        
        # Convertir le dictionnaire en liste
        result = list(produits_groupes.values())
        
        return jsonify({"success": True, "data": result})
        
    except Error as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()