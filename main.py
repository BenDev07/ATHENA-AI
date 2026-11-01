import ollama
import sqlite3

# Lire la base de connaissances
with open("banque_demo.txt", "r", encoding="utf-8") as fichier:
    connaissances = fichier.read()

# Connexion à la base de données
connexion = sqlite3.connect("mwalimu.db")

# Créer un curseur
curseur = connexion.cursor()

# Créer la table des messages
curseur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

# Enregistrer les changements
connexion.commit()

# Créer la table des réclamations
curseur.execute("""
    CREATE TABLE IF NOT EXISTS reclamations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'En attente',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

connexion.commit()

# Fonction pour enregistrer une réclamation
def enregistrer_reclamation(nom, description):

    curseur.execute(
        """
        INSERT INTO reclamations (client_name, description)
        VALUES (?, ?)
        """,
        (nom, description)
    )

    connexion.commit()

    numero = curseur.lastrowid

    return numero

# Fonction pour traiter une réclamation 
def traiter_reclamation():

    print("\nMWALIMU AI : Je vais vous aider à déposer une réclamation.")

    nom = input("Votre nom : ")

    description = input("Décrivez votre problème : ")

    confirmation = input(
        "Confirmez-vous l'enregistrement ? (oui/non) : "
    )

    if confirmation.lower() == "oui":

        numero = enregistrer_reclamation(nom, description)

        print("\nVotre réclamation a été enregistrée !")
        print("Votre numéro de suivi :", numero)

    else:
        print("\nEnregistrement annulé.")

# Déclarer notre outil pour Ollama
outils = [
    {
        "type": "function",
        "function": {
            "name": "enregistrer_reclamation",
            "description": "Enregistre une réclamation bancaire dans la base SQLite.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nom": {
                        "type": "string",
                        "description": "Nom du client"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description du problème du client"
                    }
                },
                "required": ["nom", "description"]
            }
        }
    }
]


# # Tester la fonction
# numero = enregistrer_reclamation(
#     "Benedict",
#     "Mon retrait bancaire n'a pas fonctionné."
# )

# print("Réclamation enregistrée !")
# print("Numéro de suivi :", numero)

# # Ajouter une réclamation de test
# curseur.execute(
#     """
#     INSERT INTO reclamations (client_name, description)
#     VALUES (?, ?)
#     """,
#     ("Benedict", "Mon compte a été débité, mais le retrait n'a pas fonctionné.")
# )

# connexion.commit()

# # Afficher les réclamations enregistrées
# curseur.execute("SELECT * FROM reclamations")

# reclamations = curseur.fetchall()

# for reclamation in reclamations:
#     print(reclamation)

# # Enregistrer un message de test
# curseur.execute(
#     "INSERT INTO messages (role, content) VALUES (?, ?)",
#     ("user", "Bonjour, je voudrais ouvrir un compte.")
# )

# # Valider l'enregistrement
# connexion.commit()

# # Lire les messages enregistrés
# curseur.execute("SELECT * FROM messages")

# messages = curseur.fetchall()

# print(messages)

print("Bienvenue dans MWALIMU AI !")
print("Écris 'quit' pour arrêter la conversation.")

# Notre mémoire conversationnelle
historique = [
    {
        "role": "system",
        "content": """
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
          recueille son nom et la description de son problème
          avant de procéder à l'enregistrement.
        
        GESTION DES RÉCLAMATIONS :
        - Lorsqu'un client souhaite déposer une réclamation,
          demande son nom et la description du problème.
        - Lorsque le client a fourni ces deux informations,
          utilise obligatoirement l'outil enregistrer_reclamation.
        - Ne te contente pas de dire que tu vas enregistrer la réclamation.
        - Attends le résultat de l'outil avant de confirmer l'enregistrement.

        TON COMPORTEMENT :
        - Réponds toujours en français simple.
        - Sois poli, professionnel et patient.
        - Donne des réponses courtes et faciles à comprendre.
        - Pose des questions si la demande manque de précision.
        - Ne prétends jamais être un agent humain.

        UTILISATION DE LA BASE DE CONNAISSANCES :

        - Utilise prioritairement les informations fournies dans la base.
        - Ne complète jamais une information manquante par une supposition.
        - Ne présente jamais une information inconnue comme une information officielle.
        - Si la réponse ne figure pas dans la base, indique que tu ne disposes pas de cette information.
        - Pour toute information bancaire sensible ou incertaine, oriente le client vers un agent.

        SÉCURITÉ :
        - N'invente jamais les tarifs, les taux ou les conditions bancaires.
        - Si tu ne connais pas une information, dis-le clairement.
        - Ne demande jamais le code PIN, le mot de passe ou le code secret
          d'une carte bancaire.
        - Pour les problèmes sensibles, oriente le client vers un agent humain.
        - Ne confirme jamais qu'une réclamation est enregistrée
          si elle n'a pas réellement été sauvegardée dans le système.
        
        BASE DE CONNAISSANCES :

        Voici les informations officielles de Banque Démo :

        """ + connaissances
    }
]

# Récupérer les anciens messages depuis SQLite
curseur.execute(
    "SELECT role, content FROM messages ORDER BY id ASC"
)

anciens_messages = curseur.fetchall()

# Restaurer les anciens messages dans l'historique
for message in anciens_messages:
    historique.append({
        "role": message[0],
        "content": message[1]
    })


while True:

    question = input("\nVous : ")

    if "réclamation" in question.lower() or "reclamation" in question.lower():

        traiter_reclamation()

        continue

    if question.lower() == "quit":
        print("MWALIMU AI : À bientôt !")
        break

    # Ajouter la question à l'historique
    historique.append({
        "role": "user",
        "content": question
    })

    # Enregistrer la question dans SQLite
    curseur.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        ("user", question)
    )
    connexion.commit()

    # Demander une réponse à l'IA
    reponse = ollama.chat(
        model="qwen2.5:1.5b",
        messages=historique,
        tools=outils
    )

    message = reponse["message"]
    print("Demande d'outil :", message.get("tool_calls"))
    
    # Vérifier si l'IA demande un outil
    if message.get("tool_calls"):

        # Conserver le message de demande d'outil
        historique.append(message)

        for outil in message["tool_calls"]:

            nom_fonction = outil["function"]["name"]
            arguments = outil["function"]["arguments"]

            if nom_fonction == "enregistrer_reclamation":

                numero = enregistrer_reclamation(
                    arguments["nom"],
                    arguments["description"]
                )

                resultat = (
                    f"La réclamation a été enregistrée. "
                    f"Numéro de suivi : {numero}"
                )

                historique.append({
                    "role": "tool",
                    "content": resultat
                })

                print("Réclamation enregistrée !")
                print("Numéro de suivi :", numero)

        # Renvoyer le résultat à l'IA
        reponse_finale = ollama.chat(
            model="qwen2.5:1.5b",
            messages=historique,
            tools=outils
        )

        message_ia = reponse_finale["message"]["content"]

    else:
        message_ia = message["content"]

    # Ajouter la réponse finale à l'historique
    historique.append({
        "role": "assistant",
        "content": message_ia
    })

    # Enregistrer la réponse dans SQLite
    curseur.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        ("assistant", message_ia)
    )
    connexion.commit()

    print("\nMWALIMU AI :", message_ia)







# curseur.execute("SELECT * FROM messages")

# messages = curseur.fetchall()

# for message in messages:
#     print(message)

# connexion.close()