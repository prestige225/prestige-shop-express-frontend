import os
import requests
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__, static_folder='.', template_folder='.', root_path='.')
CORS(app)

# URL du backend existant
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://prestige-shop-backend.onrender.com')

# Routes pour servir les pages HTML
@app.route('/')
def admin_home():
    return render_template('admin.html')

@app.route('/admin_commandes.html')
def admin_commandes():
    return render_template('admin_commandes.html')

@app.route('/admin_produits.html')
def admin_produits():
    return render_template('admin_produits.html')

@app.route('/messages.html')
def messages():
    return render_template('messages.html')


# Route pour servir le fichier api-config.js
@app.route('/api-config.js')
def serve_api_config():
    return send_from_directory('.', 'api-config.js')

@app.route('/backend_render/<path:filename>')
def serve_backend_render_file(filename):
    # Redirect or proxy to the backend service for backend_render files
    import requests
    from flask import redirect, url_for
    backend_url = f"{BACKEND_URL}/backend_render/{filename}"
    return redirect(backend_url)

@app.route('/message_history.html')
def serve_message_history():
    # Redirect to the backend service for message history
    from flask import redirect
    backend_url = f"{BACKEND_URL}/backend_render/message_history.html"
    return redirect(backend_url)

# Routes API pour interagir avec le backend existant
@app.route('/api/produits', methods=['GET'])
def get_produits():
    try:
        response = requests.get(f'{BACKEND_URL}/api/produits')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/commandes', methods=['GET'])
def get_commandes():
    try:
        response = requests.get(f'{BACKEND_URL}/api/commandes')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route générique pour servir les fichiers HTML du répertoire admin - DOIT ÊTRE À LA FIN
@app.route('/<path:filename>')
def serve_static_html(filename):
    import os
    # Vérifier si le fichier existe dans le répertoire courant
    if os.path.isfile(os.path.join('.', filename)) and filename.endswith('.html'):
        return send_from_directory('.', filename)
    # Si le fichier n'existe pas, retourner une erreur 404
    from flask import abort
    return abort(404)

# Point d'entrée pour Render
if __name__ == '__main__':
    # Utilise le port fourni par Render ou 8000 par défaut
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)