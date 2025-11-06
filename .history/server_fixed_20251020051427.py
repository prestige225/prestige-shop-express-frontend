from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_ici'

# Configuration CORS simple et efficace
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Configuration de la base de données
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

@app.route('/api/users', methods=['GET', 'OPTIONS'])
def api_get_users():
    if request.method == 'OPTIONS':
        return '', 200
        
    print("📊 Requête pour récupérer les utilisateurs")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur DB'})

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, numero, statut,
                   CASE WHEN session_active = 1 THEN 'CONNECTÉ' ELSE 'DÉCONNECTÉ' END as statut_connexion,
                   derniere_connexion
            FROM users
            ORDER BY derniere_connexion DESC
        """)

        utilisateurs = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"✅ {len(utilisateurs)} utilisateurs récupérés")
        return jsonify({'success': True, 'users': utilisateurs})
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/user/<int:user_id>', methods=['GET', 'OPTIONS'])
def api_get_user_profile(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    print(f"👤 Requête pour récupérer le profil utilisateur {user_id}")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur DB'})

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nom, prenom, email, numero, statut,
                   CASE WHEN session_active = 1 THEN 'CONNECTÉ' ELSE 'DÉCONNECTÉ' END as statut_connexion,
                   derniere_connexion, ip_connexion, token_session
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            print(f"✅ Profil utilisateur {user_id} récupéré")
            return jsonify({'success': True, 'user': user})
        else:
            print(f"❌ Utilisateur {user_id} non trouvé")
            return jsonify({'success': False, 'error': 'Utilisateur non trouvé'})
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/suspendre/<int:user_id>', methods=['POST', 'OPTIONS'])
def api_suspendre(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    print(f"⛔ Suspension de l'utilisateur {user_id}")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur DB'})

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET statut = 'suspendu' WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Utilisateur {user_id} suspendu")
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"❌ Erreur lors de la suspension: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/activer/<int:user_id>', methods=['POST', 'OPTIONS'])
def api_activer(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    print(f"✅ Activation de l'utilisateur {user_id}")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur DB'})

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET statut = 'actif' WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Utilisateur {user_id} activé")
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"❌ Erreur lors de l'activation: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def api_login():
    if request.method == 'OPTIONS':
        return '', 200
        
    print("🔐 Requête de connexion reçue")
    data = request.get_json()
    print(f"📧 Données reçues: {data}")
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email et mot de passe requis'})

    email = data['email']
    mot_de_passe = data['password']

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur de connexion DB'})

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nom, prenom, email, statut
            FROM users
            WHERE email = %s AND mot_de_passe = %s AND statut = 'actif'
        """, (email, mot_de_passe))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            print(f"✅ Utilisateur trouvé: {user['email']}")
            # Créer une session
            session['user_id'] = user['id']
            session['user_email'] = user['email']

            # Enregistrer la connexion dans la base
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET session_active = 1, token_session = %s, derniere_connexion = NOW(), ip_connexion = %s
                    WHERE id = %s
                """, (f"token_{user['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}", request.remote_addr, user['id']))
                conn.commit()
                cursor.close()
                conn.close()

            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'nom': user['nom'],
                    'prenom': user['prenom'],
                    'email': user['email']
                }
            })
        else:
            print("❌ Utilisateur non trouvé")
            return jsonify({'success': False, 'error': 'Email ou mot de passe incorrect'})
    except Exception as e:
        print(f"❌ Erreur lors de la requête: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def api_register():
    if request.method == 'OPTIONS':
        return '', 200
        
    print("📝 Requête d'inscription reçue")
    data = request.get_json()
    print(f"📋 Données reçues: {data}")
    
    if not data or not all(k in data for k in ('nom', 'prenom', 'email', 'mot_de_passe')):
        return jsonify({'success': False, 'error': 'Tous les champs sont requis' })

    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    mot_de_passe = data['mot_de_passe']
    numero = data.get('numero', '')  # Récupère le numéro s'il existe, sinon une chaîne vide

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur de connexion DB'})

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (nom, prenom, email, numero, mot_de_passe)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, prenom, email, numero, mot_de_passe))
        conn.commit()

        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"✅ Utilisateur créé avec ID: {user_id}")

        return jsonify({
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user_id': user_id
        })
    except mysql.connector.IntegrityError as e:
        print(f"❌ Email déjà utilisé: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Email déjà utilisé'})
    except Exception as e:
        print(f"❌ Erreur lors de l'inscription: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

# Routes pour servir les fichiers statiques
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

@app.route('/admin_commandes.html')
def serve_admin_commandes():
    return send_from_directory('.', 'admin_commandes.html')

@app.route('/test-order.html')
def serve_test_order():
    return send_from_directory('.', 'test-order.html')

@app.route('/profile.html')
def serve_profile():
    return send_from_directory('.', 'profile.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/api/logout', methods=['POST', 'OPTIONS'])
def api_logout():
    if request.method == 'OPTIONS':
        return '', 200
        
    print("🔒 Requête de déconnexion reçue")
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({'success': False, 'error': 'ID utilisateur requis'})
    
    user_id = data['user_id']
    ip_address = request.remote_addr
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur de connexion DB'})
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users 
            SET session_active = 0,
                date_derniere_deconnexion = NOW(),
                ip_derniere_deconnexion = %s
            WHERE id = %s
        """, (ip_address, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Utilisateur {user_id} déconnecté avec succès")
        return jsonify({'success': True, 'message': 'Déconnexion réussie'})
        
    except Exception as e:
        print(f"❌ Erreur lors de la déconnexion: {e}")
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur serveur'})

@app.route('/api/users/<int:user_id>', methods=['DELETE', 'OPTIONS'])
def delete_user(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    print(f"🔍 Tentative de suppression de l'utilisateur ID: {user_id}")
    
    # Vérifier si l'utilisateur a les droits d'administration
    # Note: Vous devrez peut-être implémenter une vérification d'authentification ici
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Erreur de connexion à la base de données'}), 500
    
    cursor = conn.cursor()
    
    try:
        # Vérifier d'abord si l'utilisateur existe
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Utilisateur non trouvé'}), 404
        
        # Supprimer l'utilisateur
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Utilisateur ID {user_id} supprimé avec succès")
        return jsonify({'success': True, 'message': 'Utilisateur supprimé avec succès'})
        
    except Error as e:
        print(f"❌ Erreur lors de la suppression de l'utilisateur: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur lors de la suppression de l\'utilisateur'}), 500
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Erreur inattendue'}), 500

# Routes pour la gestion des commandes

@app.route('/api/commandes', methods=['GET', 'OPTIONS'])
def get_commandes():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.*, u.nom, u.prenom, u.email 
            FROM commandes c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.date_commande DESC
        """
        cursor.execute(query)
        commandes = cursor.fetchall()
        
        # Convertir les objets datetime en chaînes pour la sérialisation JSON
        for commande in commandes:
            if 'date_commande' in commande and commande['date_commande'] is not None:
                commande['date_commande'] = commande['date_commande'].isoformat()
        
        return jsonify({"success": True, "data": commandes})
        
    except Error as e:
        print(f"Erreur lors de la récupération des commandes: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/commandes/me', methods=['GET', 'OPTIONS'])
def get_mes_commandes():
    if request.method == 'OPTIONS':
        return '', 200
        
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Non authentifié"}), 401
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM commandes 
            WHERE user_id = %s 
            ORDER BY date_commande DESC
        """
        cursor.execute(query, (session['user_id'],))
        commandes = cursor.fetchall()
        
        # Convertir les objets datetime en chaînes pour la sérialisation JSON
        for commande in commandes:
            if 'date_commande' in commande and commande['date_commande'] is not None:
                commande['date_commande'] = commande['date_commande'].isoformat()
        
        return jsonify({"success": True, "data": commandes})
        
    except Error as e:
        print(f"Erreur lors de la récupération des commandes: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

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
        
        # Extraire les noms de produits depuis data['produits'] si disponible
        produits_str = ''
        produits_json_str = ''
        if 'produits' in data and data['produits']:
            produits_list = data['produits']
            # Format texte simple pour la colonne produits
            produits_str = ', '.join([f"{p['nom']} (x{p['quantite']})" for p in produits_list])
            # Format JSON complet pour produits_json (avec images)
            produits_json_str = json.dumps(produits_list, ensure_ascii=False)
        
        # Insérer la commande
        query = """
            INSERT INTO commandes 
            (user_id, numero_commande, montant_total, adresse_livraison, telephone, produits, produits_json, notes, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'en_attente')
        """
        cursor.execute(query, (
            user_id,
            numero_commande,
            data['montant_total'],
            data['adresse_livraison'],
            data['telephone'],
            produits_str,
            produits_json_str,
            data.get('notes', '')
        ))
        
        commande_id = cursor.lastrowid
        
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

@app.route('/api/commandes/<int:commande_id>', methods=['GET', 'OPTIONS'])
def get_commande_detail(commande_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.*, u.nom, u.prenom, u.email, u.numero as user_numero
            FROM commandes c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """
        cursor.execute(query, (commande_id,))
        commande = cursor.fetchone()
        
        if not commande:
            return jsonify({"success": False, "message": "Commande non trouvée"}), 404
        
        if 'date_commande' in commande and commande['date_commande']:
            commande['date_commande'] = commande['date_commande'].isoformat()
        
        return jsonify({"success": True, "data": commande})
        
    except Error as e:
        print(f"Erreur: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/commandes/<int:commande_id>', methods=['PUT', 'OPTIONS'])
def mettre_a_jour_commande(commande_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        # Vérifier que la commande existe
        cursor.execute("SELECT id FROM commandes WHERE id = %s", (commande_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Commande non trouvée"}), 404
            
        # Mettre à jour la commande
        update_fields = []
        update_values = []
        
        if 'statut' in data:
            update_fields.append("statut = %s")
            update_values.append(data['statut'])
        if 'notes' in data:
            update_fields.append("notes = %s")
            update_values.append(data['notes'])
            
        if not update_fields:
            return jsonify({"success": False, "message": "Aucune donnée à mettre à jour"}), 400
            
        update_query = f"UPDATE commandes SET {', '.join(update_fields)} WHERE id = %s"
        update_values.append(commande_id)
        
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Commande mise à jour avec succès"})
        
    except Error as e:
        if 'conn' in locals() and conn and conn.is_connected():
            conn.rollback()
        print(f"Erreur: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/commandes/<int:commande_id>', methods=['DELETE', 'OPTIONS'])
def supprimer_commande(commande_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor()
        
        # Vérifier que la commande existe
        cursor.execute("SELECT id FROM commandes WHERE id = %s", (commande_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Commande non trouvée"}), 404
        
        # Supprimer la commande
        cursor.execute("DELETE FROM commandes WHERE id = %s", (commande_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Commande supprimée avec succès"})
        
    except Error as e:
        if 'conn' in locals() and conn and conn.is_connected():
            conn.rollback()
        print(f"Erreur: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/commandes/user/<int:user_id>', methods=['GET', 'OPTIONS'])
def get_commandes_by_user(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Erreur de connexion à la base de données"}), 500
            
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM commandes 
            WHERE user_id = %s 
            ORDER BY date_commande DESC
        """
        cursor.execute(query, (user_id,))
        commandes = cursor.fetchall()
        
        for commande in commandes:
            if 'date_commande' in commande and commande['date_commande']:
                commande['date_commande'] = commande['date_commande'].isoformat()
        
        return jsonify({"success": True, "data": commandes})
        
    except Error as e:
        print(f"Erreur: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask corrigé...")
    
    # Test de connexion DB au démarrage
    print("🔍 Test de connexion à la base de données...")
    conn = get_db_connection()
    if conn:
        conn.close()
        print("✅ Base de données accessible")
    else:
        print("⚠️  Base de données non accessible - le serveur démarrera quand même")
    
    print("🌐 Serveur disponible sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
