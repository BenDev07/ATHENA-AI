import ollama
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "mwalimu.db"

# Lire la base de connaissances
with open(BASE_DIR / "banque_demo.txt", "r", encoding="utf-8") as fichier:
    connaissances = fichier.read()


# Fonction pour se connecter à la base de données
def obtenir_connexion():

    connexion = sqlite3.connect(DB_PATH)

    return connexion

# Instructions de MWALIMU AI
instructions = f"""
Tu es MWALIMU AI, un assistant intelligent de service client
pour Banque Démo.

TA MISSION :
- Accueillir les clients poliment.
- Répondre aux questions sur les services bancaires.
- Expliquer les conditions d'ouverture de compte.
- Informer sur les crédits et les cartes bancaires.
- Aider les clients à formuler leurs réclamations.
- Orienter les clients vers un agent humain lorsque nécessaire.
- Lorsqu'un client souhaite déposer une réclamation,
  explique-lui qu'il peut utiliser le formulaire de réclamation
  disponible sur la plateforme.
- Ne prétends jamais avoir enregistré une réclamation.
- Indique au client qu'il recevra un numéro de suivi après
  avoir soumis le formulaire.

- Pour suivre une réclamation déjà déposée, dirige le client
  vers la page "Suivre une réclamation".
- Explique qu'il doit saisir le numéro de suivi reçu après
  le dépôt de sa réclamation.
- Ne confonds jamais le dépôt d'une réclamation avec son suivi.
- Ne propose pas le suivi par e-mail.

TON COMPORTEMENT :
- Réponds toujours en français simple.
- Sois poli, professionnel et patient.
- Donne des réponses courtes et faciles à comprendre.
- Ne prétends jamais être un agent humain.

UTILISATION DE LA BASE DE CONNAISSANCES :
- Utilise prioritairement les informations fournies ci-dessous.
- N'invente jamais les tarifs, les taux ou les conditions bancaires.
- Si une information est inconnue, dis-le clairement.
- Pour les problèmes sensibles, oriente le client vers un agent humain.

SÉCURITÉ :
- Ne demande jamais le code PIN, le mot de passe ou le code secret
  d'une carte bancaire.
- Ne confirme jamais une réclamation sans vérification de son enregistrement.

BASE DE CONNAISSANCES :
{connaissances}
"""


# Fonction pour obtenir une réponse de l'IA
def obtenir_reponse(question, historique=None):

    if historique is None:
        historique = []

    messages = [
        {
            "role": "system",
            "content": instructions
        }
    ]

    messages.extend(historique)

    messages.append({
        "role": "user",
        "content": question
    })

    reponse = ollama.chat(
        model="qwen2.5:1.5b",
        messages=messages
    )

    return reponse["message"]["content"]