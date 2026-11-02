from django.shortcuts import render
from .models import Reclamation
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from assistant_web import obtenir_reponse, obtenir_connexion
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test



def liste_reclamations(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("connexion_agent")

    reclamations = Reclamation.objects.all().order_by("-created_at")

    return render(
        request,
        "agents/reclamations.html",
        {"reclamations": reclamations}
    )


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def modifier_statut(request, id):

    reclamation = get_object_or_404(Reclamation, id=id)

    nouveau_statut = request.POST.get("status")

    statuts_autorises = [
        "En attente",
        "En cours",
        "Résolue"
    ]

    if nouveau_statut in statuts_autorises:
        reclamation.status = nouveau_statut
        reclamation.save()

    return redirect("liste_reclamations")



@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def repondre_reclamation(request, id):

    reclamation = get_object_or_404(Reclamation, id=id)

    reponse = request.POST.get("agent_response", "").strip()

    if reponse:
        reclamation.agent_response = reponse
        reclamation.save()

    return redirect("liste_reclamations")


def accueil(request):
    return render(request, "agents/accueil.html")



def deposer_reclamation(request):

    erreur = None

    if request.method == "POST":

        nom = request.POST.get("nom")
        description = request.POST.get("description")

        if nom and description:

            reclamation = Reclamation.objects.create(
                client_name=nom,
                description=description
            )

            return render(
                request,
                "agents/deposer_reclamation.html",
                {
                    "numero": reclamation.id,
                    "success": True
                }
            )

        else:
            erreur = "Veuillez remplir tous les champs."

    return render(
        request,
        "agents/deposer_reclamation.html",
        {"erreur": erreur}
    )


def suivre_reclamation(request):

    reclamation = None
    erreur = None

    if request.method == "POST":

        numero = request.POST.get("numero")

        try:
            reclamation = Reclamation.objects.get(id=numero)

        except Reclamation.DoesNotExist:
            erreur = "Aucune réclamation trouvée avec ce numéro."

        except ValueError:
            erreur = "Veuillez entrer un numéro valide."

    return render(
        request,
        "agents/suivi.html",
        {
            "reclamation": reclamation,
            "erreur": erreur
        }
    )

@require_POST
def nouvelle_conversation(request):

    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    # Supprimer les anciens messages
    curseur.execute("DELETE FROM messages")

    connexion.commit()
    connexion.close()

    # Retourner vers le chatbot vide
    return redirect("chatbot")

def chatbot(request):

    question = ""

    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    if request.method == "POST":

        question = request.POST.get("question", "").strip()

        if question:

            # Récupérer l'historique
            curseur.execute(
                "SELECT role, content FROM messages ORDER BY id ASC"
            )

            historique = [
                {"role": ligne[0], "content": ligne[1]}
                for ligne in curseur.fetchall()
            ]

            # Obtenir la réponse de l'IA
            question_min = question.lower()

            if any(mot in question_min for mot in [
                "suivi", "suivre", "état d'avancement",
                "numero de suivi", "numéro de suivi"
            ]):
                reponse = (
                    "Pour suivre votre réclamation, rendez-vous sur la page "
                    "'Suivre une réclamation' de notre plateforme. "
                    "Saisissez le numéro de suivi reçu après le dépôt "
                    "de votre demande pour consulter son statut et la "
                    "réponse éventuelle de notre agent."
                )
            else:
                reponse = obtenir_reponse(question, historique)

            # Enregistrer les deux messages
            curseur.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                ("user", question)
            )

            curseur.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                ("assistant", reponse)
            )

            connexion.commit()

    # Récupérer tous les messages pour les afficher
    curseur.execute(
        "SELECT role, content FROM messages ORDER BY id ASC"
    )

    messages = [
        {"role": ligne[0], "content": ligne[1]}
        for ligne in curseur.fetchall()
    ]

    connexion.close()

    return render(
        request,
        "agents/chat.html",
        {"messages": messages}
    )


def service_worker(request):

    fichier = Path(settings.BASE_DIR) / "agents" / "static" / "agents" / "service-worker.js"

    contenu = fichier.read_text(encoding="utf-8")

    return HttpResponse(
        contenu,
        content_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )


def connexion_agent(request):

    erreur = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        utilisateur = authenticate(
            request,
            username=username,
            password=password
        )

        if utilisateur is not None and utilisateur.is_staff:

            login(request, utilisateur)

            return redirect("liste_reclamations")

        else:
            erreur = "Identifiants incorrects ou accès non autorisé."

    return render(
        request,
        "agents/connexion_agent.html",
        {"erreur": erreur}
    )


def deconnexion_agent(request):

    if request.method == "POST":
        logout(request)

    return redirect("accueil")