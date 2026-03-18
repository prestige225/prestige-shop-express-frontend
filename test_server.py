#!/usr/bin/env python
# Script de test pour vérifier que le serveur Flask fonctionne

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'OK', 200

@app.route('/test')
def test():
    return jsonify({"status": "ok", "message": "Server is running"})

if __name__ == '__main__':
    print("🚀 Starting test server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
