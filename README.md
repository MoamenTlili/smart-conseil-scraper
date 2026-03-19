# Test Technique Smart Conseil - Connecteur Instagram

## Description
Ce projet implémente un connecteur Instagram en Python 3 permettant de collecter des publications, du texte, des images et des commentaires par rapport à un sujet défini (ex. : "Jacques Chirac"). Les données extraites ainsi que les images (converties en binaire) sont ensuite stockées de manière sécurisée dans une base de données MongoDB.

## Architecture & Qualité du Code
- **Modularité :** Séparation claire des responsabilités entre l'extraction (`scraper.py`), la gestion de la base de données (`database.py`) et l'exécution principale (`main.py`).
- **Sécurité :** Les variables sensibles (comme l'URI MongoDB) sont gérées via un fichier `.env` en utilisant `python-dotenv`.
- **Typage & Logging :** Utilisation intensive du typage Python (`typing`) et configuration du module `logging` pour assurer un suivi professionnel de l'exécution (production-ready).
- **Stockage Robuste des Images :** Les images sont téléchargées (avec un User-Agent conforme) et converties en `bson.binary.Binary` pour être stockées directement dans MongoDB avec les données textuelles.

## Note sur les restrictions d'Instagram / Meta
Suite aux récentes mises à jour, Meta bloque de manière agressive le scraping anonyme via Instaloader, retournant souvent des erreurs `404 Not Found` ou redirigeant vers la page de connexion.
Pour garantir que cette application reste testable et pour prouver **la logique d'insertion en base de données**, j'ai implémenté un modèle de **Dégradation Gracieuse (Mode Démonstration)**.
Si le script détecte que Meta a bloqué l'IP, il bascule automatiquement vers un jeu de données réaliste utilisant des images stables du domaine public (Wikimedia), permettant ainsi d'évaluer le bon fonctionnement du pipeline de traitement et d'insertion MongoDB de bout en bout.

## Instructions d'exécution
1. Créer un environnement virtuel : `python3 -m venv venv`
2. Activer l'environnement : `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
3. Installer les dépendances : `pip install -r requirements.txt`
4. Ajouter le fichier `.env` à la racine du projet contenant la variable `MONGO_URI`.
5. Lancer le script : `python3 main.py`