import os
from flask import Flask, send_from_directory, Response
from werkzeug.exceptions import NotFound

# Initialisation de l'application Flask
# Configuration pour servir tous les fichiers du répertoire courant
app = Flask(__name__)

# Configuration pour améliorer la compatibilité avec les crawlers
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Middleware pour ajouter les en-têtes appropriés
@app.after_request
def add_headers(response):
    # En-têtes de sécurité et d'identification du serveur
    response.headers['Server'] = 'Prestige-Shop-Express/1.0'
    response.headers['X-UA-Compatible'] = 'IE=edge'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Gestion du cache pour les crawlers
    if 'text/html' in response.content_type:
        # Permettre l'indexation Google avec cache court (1 heure)
        response.headers['Cache-Control'] = 'public, max-age=3600, must-revalidate'
    elif 'text/plain' in response.content_type or 'application/xml' in response.content_type:
        # robots.txt et sitemap.xml - courte durée de cache
        response.headers['Cache-Control'] = 'public, max-age=86400'
        # En-têtes spécifiques pour robots.txt
        if 'robots' in response.headers.get('Content-Type', ''):
            response.headers['Content-Disposition'] = 'inline'
    else:
        # Assets statiques - cache long
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    
    # En-têtes pour éviter les problèmes d'indexation
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

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

# Healthcheck pour Render (très important!)
@app.route('/health')
def health():
    """Endpoint de santé pour monitoring et relance automatique"""
    return {'status': 'healthy', 'service': 'prestige-shop-express'}, 200

@app.route('/')
def home():
    """Servir index.html avec send_from_directory (plus robuste que render_template)"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/login.html')
def login():
    try:
        return send_from_directory('.', 'login.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/register.html')
def register():
    try:
        return send_from_directory('.', 'register.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/welcome.html')
def welcome():
    try:
        return send_from_directory('.', 'welcome.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/chatbot.html')
def chatbot():
    try:
        return send_from_directory('.', 'chatbot.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/demo-video-carousel.html')
def demo_video():
    try:
        return send_from_directory('.', 'demo-video-carousel.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/admin/admin_messages.html')
def admin_messages():
    try:
        return send_from_directory('admin', 'admin_messages.html')
    except Exception as e:
        return f"Erreur: {str(e)}", 500

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

@app.route('/ima/<path:filename>')
def serve_ima(filename):
    try:
        return send_from_directory('ima', filename)
    except FileNotFoundError:
        # Si le fichier n'est pas trouvé, retourner une réponse 404
        return 'File not found', 404
    except Exception as e:
        # Pour tout autre erreur, retourner une erreur 500
        return f'Internal server error: {str(e)}', 500

# ----------------------------
# Route pour robots.txt
# ----------------------------
@app.route('/robots.txt')
def robots():
    """Servir robots.txt - permission pour crawler tout sauf admin"""
    robots_content = """User-agent: *
Allow: /
Allow: /css/
Allow: /js/
Allow: /images/
Allow: /ima/
Allow: /imageprestige/
Allow: /videos/
Disallow: /admin/
Disallow: /*.json
Disallow: /*?*

User-agent: Googlebot
Allow: /
Allow: /css/
Allow: /js/
Allow: /images/
Allow: /ima/
Allow: /imageprestige/
Disallow: /admin/

Sitemap: https://prestige-shop-express.onrender.com/sitemap.xml
"""
    return Response(robots_content, mimetype='text/plain')

# ----------------------------
# Sitemap dynamique
# ----------------------------
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Générer un sitemap XML pour Google"""
    try:
        base_url = "https://prestige-shop-express.onrender.com"

        # Pages principales - simples et fiables
        pages = [
            {"url": f"{base_url}/", "freq": "weekly", "priority": "1.0"},
            {"url": f"{base_url}/login.html", "freq": "monthly", "priority": "0.7"},
            {"url": f"{base_url}/register.html", "freq": "monthly", "priority": "0.7"},
            {"url": f"{base_url}/welcome.html", "freq": "monthly", "priority": "0.6"},
            {"url": f"{base_url}/chatbot.html", "freq": "monthly", "priority": "0.5"},
            {"url": f"{base_url}/demo-video-carousel.html", "freq": "monthly", "priority": "0.5"},
        ]

        # Générer le XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for page in pages:
            xml += '  <url>\n'
            xml += f'    <loc>{page["url"]}</loc>\n'
            xml += f'    <changefreq>{page["freq"]}</changefreq>\n'
            xml += f'    <priority>{page["priority"]}</priority>\n'
            xml += '  </url>\n'

        xml += '</urlset>'

        return Response(xml, mimetype='application/xml; charset=utf-8')
    
    except Exception as e:
        # En cas d'erreur, retourner un sitemap minimal
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += '  <url>\n'
        xml += '    <loc>https://prestige-shop-express.onrender.com/</loc>\n'
        xml += '    <changefreq>weekly</changefreq>\n'
        xml += '    <priority>1.0</priority>\n'
        xml += '  </url>\n'
        xml += '</urlset>'
        return Response(xml, mimetype='application/xml; charset=utf-8')

# ----------------------------
# Route catch-all pour SPA (PRIORITÉ HAUTE)
# ----------------------------
@app.route('/<path:path>')
def catch_all(path):
    """Servir les fichiers statiques ou index.html pour les routes SPA"""
    filepath = os.path.join('.', path)
    
    # Si le fichier existe exactement, le servir
    if os.path.isfile(filepath):
        directory = os.path.dirname(filepath) or '.'
        filename = os.path.basename(filepath)
        return send_from_directory(directory, filename)
    
    # Sinon rediriger vers index.html (pour React/SPA routing)
    return send_from_directory('.', 'index.html')

# ----------------------------
# Point d'entrée pour Render
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Render va passer le port en variable d'environnement
    app.run(host='0.0.0.0', port=port, debug=False)