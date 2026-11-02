# 

### Assistant intelligent de service client bancaire

**** (Assistant de Traitement Harmonisé et d'Enseignement Numérique Automatisé par Intelligence Artificielle) est une application intelligente conçue pour améliorer la gestion du service client bancaire.

Elle utilise l'intelligence artificielle pour répondre aux questions courantes des clients, les orienter dans leurs démarches et faciliter le traitement des réclamations.

## Fonctionnalités

- **Assistant IA :** répond aux questions des clients en français.
- **Base de connaissances locale :** fournit des informations sur les services de Banque Démo.
- **Gestion des réclamations :** permet aux clients de déposer et suivre leurs réclamations.
- **Espace agent :** permet aux agents de consulter les réclamations, modifier leur statut et répondre aux clients.
- **Mode Offline-First :** permet d'accéder aux fonctionnalités principales sans connexion Internet, lorsque l'application et ses ressources sont déjà installées sur la machine.

## Technologies utilisées

- Python
- Django
- Ollama
- Qwen 2.5 (1.5B)
- SQLite
- HTML / CSS / JavaScript
- Service Workers (PWA)

## Installation

### 1. Récupérer le projet

```bash
git clone https://github.com/BenDev07/ATHENA-AI.git
cd ATHENA-AI
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

Sous Windows :

```powershell
.\venv\Scripts\Activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer la clé secrète

Créer un fichier `.env` à la racine du projet :

```env
DJANGO_SECRET_KEY=votre_cle_secrete
```

Générer une clé avec :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Installer Ollama et le modèle IA

Installer Ollama, puis télécharger le modèle :

```bash
ollama pull qwen2.5:1.5b
```

### 7. Lancer l'application

```bash
python manage.py migrate
python initialiser_db.py
python manage.py runserver
```

Ouvrir ensuite :

http://127.0.0.1:8000/

## Mode Offline-First

 est conçu pour fonctionner localement. Après installation et mise en cache des ressources nécessaires, les principales fonctionnalités peuvent être utilisées sans connexion Internet.

Le serveur Django et Ollama doivent toutefois rester actifs sur la machine.

## Projet

**Nom :**   
**Organisation :** Banque Démo  
**Dépôt GitHub :** https://github.com/BenDev07/ATHENA-AI

---

* — La sagesse au service de la relation client.*