import os
from flask import Flask, render_template, send_from_directory, Response, redirect, url_for, request

# Initialisation de l'application Flask
app = Flask(__name__, static_folder='.', template_folder='.')

# ----------------------------
# Produits et catégories
# ----------------------------
produits = [
    {"slug": "casque-bluetooth"},
    {"slug": "ecouteurs-true-wireless"},
    {"slug": "chargeur-rapide"},
    # ajoute ici tous tes produits
]

categories = [
    "produits",
    "contact"
    # ajoute ici d'autres catégories si besoin
]

# ----------------------------
# Routes HTML principales
# ----------------------------
@app.route('/')
def home():
    # Servir index.html directement
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

@app.route('/admin/admin_messages.html')
def admin_messages():
    return render_template('admin/admin_messages.html')

# ----------------------------
# Routes pour les assets statiques
# ----------------------------
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

# ----------------------------
# Route pour robots.txt
# ----------------------------
@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')

# ----------------------------
# Sitemap dynamique
# ----------------------------
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    base_url = "https://prestige-shop-express.onrender.com"

    # Pages fixes
    pages = [
        {"loc": f"{base_url}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base_url}/login.html", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base_url}/register.html", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base_url}/contact", "changefreq": "monthly", "priority": "0.5"},
    ]

    # Ajouter les catégories
    for cat in categories:
        pages.append({"loc": f"{base_url}/{cat}", "changefreq": "weekly", "priority": "0.8"})

    # Ajouter les produits
    for prod in produits:
        pages.append({"loc": f"{base_url}/produits/{prod['slug']}", "changefreq": "monthly", "priority": "0.6"})

    # Génération du XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        xml += '  <url>\n'
        xml += f"    <loc>{page['loc']}</loc>\n"
        xml += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml += f"    <priority>{page['priority']}</priority>\n"
        xml += '  </url>\n'

    xml += '</urlset>'

    return Response(xml, mimetype='application/xml')

# ----------------------------
# Route catch-all pour SPA - Améliorée
# ----------------------------
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Si le chemin correspond à un fichier statique qui existe, le servir
    if path and os.path.exists(os.path.join('.', path)) and path != 'index.html':
        # Vérifier si c'est un fichier (pas un dossier)
        if os.path.isfile(os.path.join('.', path)):
            return send_from_directory('.', path)
    
    # Pour toutes les autres routes, servir index.html (SPA)
    return render_template('index.html')

# ----------------------------
# Point d'entrée pour Render
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)