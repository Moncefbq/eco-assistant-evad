import requests
import json
import subprocess

# --- Configuration NoCoDB ---
NOCODB_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
TABLE_ID = "m6zxxbaq2f869a0"
NOCODB_URL = f"https://app.nocodb.com/api/v2/tables/{TABLE_ID}/records"
HEADERS = {"xc-token": NOCODB_TOKEN, "Content-Type": "application/json"}


# --- Appel local au modèle Ollama ---
def ask_model_ollama(description):
    """Interroge le modèle local Ollama (Gemma ou Mistral)."""
    try:
        cmd = ["ollama", "run", "gemma:2b", description]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {"response": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}


# --- Sauvegarde dans NoCoDB ---
def save_to_nocodb(data):
    """Envoie les données dans ta table NoCoDB."""
    try:
        payload = {"Title": data["Title"], "Description": data["Description"], "Type": data["Type"], "Revenues": data["Revenues"]}
        resp = requests.post(NOCODB_URL, headers=HEADERS, data=json.dumps({"fields": payload}))
        if resp.status_code == 200 or resp.status_code == 201:
            print("✅ Projet enregistré dans NoCoDB !")
        else:
            print(f"❌ Erreur NoCoDB : {resp.status_code} - {resp.text}")
    except Exception as e:
        print("⚠️ Erreur lors de la sauvegarde :", e)
