from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("reclamations/", views.liste_reclamations, name="liste_reclamations"),
    path(
        "reclamations/<int:id>/modifier/",
        views.modifier_statut,
        name="modifier_statut"
    ),

    path(
        "reclamations/<int:id>/repondre/",
        views.repondre_reclamation,
        name="repondre_reclamation"
        ),

    path(
        "deposer-reclamation/",
        views.deposer_reclamation,
        name="deposer_reclamation"
    ),
    path(
        "suivi/",
        views.suivre_reclamation,
        name="suivre_reclamation"
    ),
    path("chat/", views.chatbot, name="chatbot"),
    path("service-worker.js", views.service_worker, name="service_worker"),

    path("agent/connexion/", views.connexion_agent, name="connexion_agent"),
    path("agent/deconnexion/", views.deconnexion_agent, name="deconnexion_agent"),

    
]