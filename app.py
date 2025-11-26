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

# Route pour servir les fichiers statiques
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Point d'entrée pour Render
if __name__ == '__main__':
    # Utilise le port fourni par Render ou 8000 par défaut
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)