from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# URL de ton API sur Render
API_BASE_URL = "https://africa-geo-api.onrender.com"

@app.route('/')
def index():
    try:
        # On récupère les pays pour l'accueil
        response = requests.get(f"{API_BASE_URL}/countries", timeout=5)
        countries = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Erreur API: {e}")
        countries = []
    return render_template('index.html', countries=countries)

@app.route('/explorer/<int:country_id>')
def explorer(country_id):
    try:
        # On appelle ton API sur Render
        response = requests.get(f"{API_BASE_URL}/countries/{country_id}/full-tree", timeout=10)
        data = response.json()
        
        # DEBUG : Affiche dans ton terminal VS Code ce que l'API renvoie vraiment
        print(f"DEBUG DATA pour ID {country_id}:", data)
        
        # Sécurité : si l'API renvoie une erreur ou un objet vide
        if response.status_code != 200 or not data:
            return "Pays non trouvé ou erreur API", 404
            
        return render_template('explorer.html', country=data)
    except Exception as e:
        print(f"ERREUR CONNEXION API: {e}")
        return f"Impossible de contacter l'API : {e}", 500

if __name__ == '__main__':
    # On récupère le port via la variable d'environnement de Render
    import os
    port = int(os.environ.get("PORT", 5001))
    
    # IMPORTANT : host="0.0.0.0" permet à Render de router le trafic vers votre app
    app.run(host="0.0.0.0", port=port)
