import os
from flask import Flask, render_template, send_from_directory

# Initialisation de l'application Flask
app = Flask(__name__, static_folder='.', template_folder='.')

# Routes pour servir les pages HTML principales
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')

@app.route('/demo-video-carousel.html')
def demo_video():
    return render_template('demo-video-carousel.html')

# Routes pour servir les fichiers CSS
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

# Routes pour servir les fichiers JavaScript
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename) if os.path.exists(os.path.join('js', filename)) else send_from_directory('.', filename)

# Route pour servir les autres fichiers statiques
@app.route('/<path:filename>')
def serve_static(filename):
    # Vérifier si le fichier existe localement
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    # Sinon, renvoyer vers le template (pour la compatibilité avec les routes existantes)
    return render_template(filename) if filename.endswith('.html') else ('File not found', 404)

# Point d'entrée pour Render
if __name__ == '__main__':
    # Utilise le port fourni par Render ou 8000 par défaut
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)