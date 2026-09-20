# ➗ MathBot — Chatbot Maths (Streamlit)

Chatbot pédagogique sur les mathématiques (arithmétique, algèbre, géométrie,
trigonométrie, mathématiciens célèbres...), avec inscription/connexion et une
interface **simple et claire** — déployable directement sur `share.streamlit.io`.

C'est exactement la même architecture que le projet "Lions de l'Atlas" :
seul le sujet du chatbot et le style visuel ont changé.

---

## 1. Arborescence du projet (3 fichiers, aucun dossier)

```
mathbot/
├── app.py               # Application Streamlit complète (pages, auth, CSS intégré)
├── chatbot_engine.py     # Logique du chatbot (règles NLTK sur les maths)
└── requirements.txt      # Dépendances (streamlit + nltk)
```

`database.db` (SQLite) est créé automatiquement au premier lancement.

---

## 2. Déploiement sur share.streamlit.io

1. Poussez les 3 fichiers (`app.py`, `chatbot_engine.py`, `requirements.txt`)
   à la racine de votre dépôt GitHub.
2. Sur la page de déploiement (`https://share.streamlit.io/deploy`) :
   - **Branch** : `main`
   - **Main file path** : `app.py`
3. Cliquez sur **Deploy**.

---

## 3. Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ouvrez ensuite `http://localhost:8501`.

---

## 4. Ce qui a changé par rapport à la version "Lions de l'Atlas"

- `chatbot_engine.py` : nouvelles règles sur les maths (addition, fractions,
  racine carrée, théorème de Pythagore, algèbre, dérivées, mathématiciens
  célèbres...).
- `app.py` : thème visuel simplifié (blanc / bleu, sans dégradés ni ombres
  marquées), icônes remplacées (calculatrice, symbole π) et textes adaptés
  au sujet "maths".
- La logique d'authentification (inscription, connexion, mot de passe
  haché avec PBKDF2-HMAC-SHA256, "mot de passe oublié") est **inchangée**.

---

## 5. Limites techniques (identiques à la version précédente)

- Pas de vrais cookies persistants : la session dure tant que l'onglet reste ouvert.
- Sur l'offre gratuite de Streamlit Cloud, `database.db` peut être réinitialisée
  au redémarrage de l'application.
- Pas d'icône "afficher/masquer le mot de passe" (limite de Streamlit).

## 6. Pistes d'amélioration possibles

- Ajouter des exercices interactifs avec correction automatique.
- Remplacer SQLite par une base de données externe persistante.
- Sauvegarder l'historique des conversations par utilisateur en base de données.
