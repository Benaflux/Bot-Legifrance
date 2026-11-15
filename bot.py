import os
import requests

# Récupération sécurisée depuis les Secrets GitHub
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
WEBHOOK_DISCORD = os.environ.get("DISCORD_WEBHOOK")

# 1. Connexion à Légifrance (PISTE)
token_res = requests.post(
    "https://oauth.piste.gouv.fr/api/oauth/token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid"
    }
).json()
token = token_res["access_token"]

# 2. Récupération des 3 dernières lois publiées
search_res = requests.post(
    "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "fond": "JORF",
        "recherche": {
            "champs": [],
            "filtres": [{"facette": "NATURE", "valeurs": ["LOI"]}],
            "pageNumber": 1,
            "pageSize": 3,
            "sort": "SIGNATURE_DATE_DESC",
            "typePagination": "DEFAUT"
        }
    }
).json()

# 3. Envoi dans ton salon Discord
for item in search_res.get("results", []):
    titre = item["titles"][0]["title"]
    id_loi = item["titles"][0]["id"]
    lien = f"https://www.legifrance.gouv.fr/jorf/id/{id_loi}"
    
    requests.post(WEBHOOK_DISCORD, json={
        "embeds": [{
            "title": titre[:256],
            "url": lien,
            "color": 3447003
        }]
    })
