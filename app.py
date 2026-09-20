# app.py
# Chatbot "MathBot" — Version Streamlit (compatible share.streamlit.io)
# Authentification (inscription / connexion) + chatbot sur les mathématiques,
# avec un style volontairement simple et clair (peu de couleurs, peu d'effets).

import os
import re
import time
import sqlite3
import hashlib
import secrets
from datetime import datetime

import streamlit as st

from chatbot_engine import get_response

# ============================================================================
# Configuration générale
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

st.set_page_config(
    page_title="MathBot — Chatbot Maths",
    page_icon="➗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# Base de données (SQLite) + hachage sécurisé des mots de passe
# ============================================================================
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hache le mot de passe avec PBKDF2-HMAC-SHA256 et un sel aléatoire.
    Format stocké : "sel_hex$hash_hex". On n'enregistre jamais le mot de
    passe en clair."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, digest_hex = stored_hash.split("$")
    except ValueError:
        return False
    check_digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000)
    return secrets.compare_digest(check_digest.hex(), digest_hex)


init_db()

# ============================================================================
# Icônes SVG simples (thème maths : calculatrice, livre, graphique)
# ============================================================================
ICON_CALC = """
<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="52" height="52">
  <rect x="8" y="4" width="32" height="40" rx="4" fill="#ffffff" stroke="#1d4ed8" stroke-width="2"/>
  <rect x="13" y="9" width="22" height="8" rx="1.5" fill="#1d4ed8"/>
  <circle cx="16" cy="24" r="2.3" fill="#1d4ed8"/>
  <circle cx="24" cy="24" r="2.3" fill="#1d4ed8"/>
  <circle cx="32" cy="24" r="2.3" fill="#1d4ed8"/>
  <circle cx="16" cy="31" r="2.3" fill="#1d4ed8"/>
  <circle cx="24" cy="31" r="2.3" fill="#1d4ed8"/>
  <circle cx="32" cy="31" r="2.3" fill="#1d4ed8"/>
  <circle cx="16" cy="38" r="2.3" fill="#1d4ed8"/>
  <circle cx="24" cy="38" r="2.3" fill="#1d4ed8"/>
  <circle cx="32" cy="38" r="2.3" fill="#1d4ed8"/>
</svg>
"""

ICON_BOT = """
<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="30" height="30">
  <circle cx="24" cy="24" r="24" fill="#1d4ed8"/>
  <text x="24" y="30" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#ffffff" font-weight="700">π</text>
</svg>
"""

# ============================================================================
# CSS intégré — style simple et clair (blanc, bleu, gris, sans dégradés)
# ============================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --blue: #1d4ed8; --blue-dark: #1e3a8a; --border: #e2e8f0;
  --text-muted: #64748b; --bg-soft: #f8fafc;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.block-container { max-width: 600px; padding-top: 2rem; }

/* ---- Boutons ---- */
.stButton > button, .stFormSubmitButton > button {
  width: 100%;
  border: none;
  border-radius: 8px;
  padding: 0.55rem 1rem;
  font-weight: 600;
  background: var(--blue);
  color: #ffffff;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: var(--blue-dark);
  color: #ffffff;
  border: none;
}

/* Boutons secondaires (liens de navigation entre pages) */
button[kind="secondary"] {
  background: transparent !important;
  color: var(--blue) !important;
  box-shadow: none !important;
  font-weight: 500 !important;
  text-decoration: underline;
}
button[kind="secondary"]:hover { color: var(--blue-dark) !important; }

/* ---- Champs texte ---- */
.stTextInput > div > div > input {
  border-radius: 8px !important;
  border: 1.5px solid var(--border) !important;
  padding: 0.5rem 0.75rem !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(29,78,216,0.12) !important;
}

/* ---- Carte d'authentification ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
  padding: 0.5rem;
}

.brand-title { text-align: center; color: var(--blue-dark); font-weight: 700; font-size: 1.35rem; margin: 6px 0 0; }
.brand-tagline { text-align: center; color: var(--text-muted); font-size: 0.85rem; margin: 0 0 18px; }
.auth-title { text-align: center; font-size: 1.1rem; margin: 4px 0 16px; }
.footer-note { text-align: center; font-size: 0.82rem; color: var(--text-muted); margin-top: 10px; }

/* ---- En-tête du chat ---- */
.chat-header {
  background: var(--blue);
  color: #ffffff;
  padding: 14px 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}
.chat-header h1 { margin: 0; font-size: 1.05rem; }
.chat-header p { margin: 0; font-size: 0.78rem; opacity: 0.85; }

/* ---- Bulles de messages ---- */
.msg-row { display: flex; gap: 10px; align-items: flex-end; margin-bottom: 12px; max-width: 88%; }
.msg-row.user { margin-left: auto; flex-direction: row-reverse; }
.msg-avatar { flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%; overflow: hidden; }
.msg-avatar.user-avatar {
  background: var(--blue-dark); color: #fff; display: flex; align-items: center;
  justify-content: center; font-size: 0.75rem; font-weight: 700;
}
.msg-bubble { padding: 9px 13px; border-radius: 12px; font-size: 0.92rem; line-height: 1.45; }
.msg-row.bot .msg-bubble { background: var(--bg-soft); border: 1px solid var(--border); }
.msg-row.user .msg-bubble { background: var(--blue); color: #fff; }
.msg-time { display: block; font-size: 0.66rem; margin-top: 4px; opacity: 0.65; }

[data-testid="stChatInput"] textarea { border-radius: 16px !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# État de session
# ============================================================================
if "view" not in st.session_state:
    st.session_state.view = "login"  # login | register | forgot | chat
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "messages" not in st.session_state:
    st.session_state.messages = []  # liste de (role, texte, heure)


def go_to(view: str):
    st.session_state.view = view


def logout():
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.session_state.messages = []
    st.session_state.view = "login"


# Si connecté, on force l'affichage du chat même si "view" pointait ailleurs
if st.session_state.user_id and st.session_state.view in ("login", "register", "forgot"):
    st.session_state.view = "chat"


# ============================================================================
# En-tête de marque (utilisé sur les pages d'authentification)
# ============================================================================
def brand_header():
    html = (
        f'<div style="text-align:center; margin-bottom: 8px;">{ICON_CALC}</div>'
        '<p class="brand-title">MathBot</p>'
        '<p class="brand-tagline">Le chatbot qui t\'aide à réviser les maths</p>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ============================================================================
# Page : Connexion
# ============================================================================
def render_login():
    brand_header()
    with st.container(border=True):
        st.markdown('<p class="auth-title">Connexion</p>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Adresse e-mail", placeholder="vous@exemple.com")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            remember_me = st.checkbox("Se souvenir de moi")
            submitted = st.form_submit_button("Se connecter")

        if submitted:
            errors = []
            email_clean = email.strip().lower()
            if not EMAIL_REGEX.match(email_clean):
                errors.append("Adresse e-mail invalide.")
            if not password:
                errors.append("Veuillez saisir votre mot de passe.")

            user = None
            if not errors:
                conn = get_connection()
                user = conn.execute("SELECT * FROM users WHERE email = ?", (email_clean,)).fetchone()
                conn.close()
                if not user or not verify_password(password, user["password_hash"]):
                    errors.append("E-mail ou mot de passe incorrect.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state.user_id = user["id"]
                st.session_state.user_name = user["full_name"]
                st.session_state.view = "chat"
                st.session_state.messages = []
                st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            st.button("Mot de passe oublié ?", key="go_forgot", type="secondary", on_click=go_to, args=("forgot",))
        with col2:
            st.button("Créer un compte", key="go_register", type="secondary", on_click=go_to, args=("register",))

    st.markdown(
        '<p class="footer-note">Remarque : la session reste active tant que cet onglet '
        'du navigateur reste ouvert (limite technique de Streamlit).</p>',
        unsafe_allow_html=True,
    )


# ============================================================================
# Page : Inscription
# ============================================================================
def render_register():
    brand_header()
    with st.container(border=True):
        st.markdown('<p class="auth-title">Créer un compte</p>', unsafe_allow_html=True)

        with st.form("register_form"):
            full_name = st.text_input("Nom complet", placeholder="Votre nom complet")
            email = st.text_input("Adresse e-mail", placeholder="vous@exemple.com")
            password = st.text_input("Mot de passe", type="password", placeholder="8 caractères minimum")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password", placeholder="Répétez le mot de passe")
            submitted = st.form_submit_button("Créer mon compte")

        if submitted:
            errors = []
            full_name_clean = full_name.strip()
            email_clean = email.strip().lower()

            if len(full_name_clean) < 2:
                errors.append("Le nom complet doit contenir au moins 2 caractères.")
            if not EMAIL_REGEX.match(email_clean):
                errors.append("Adresse e-mail invalide.")
            if len(password) < 8:
                errors.append("Le mot de passe doit contenir au moins 8 caractères.")
            if password != confirm_password:
                errors.append("Les mots de passe ne correspondent pas.")

            if not errors:
                conn = get_connection()
                existing = conn.execute("SELECT id FROM users WHERE email = ?", (email_clean,)).fetchone()
                if existing:
                    errors.append("Un compte existe déjà avec cet e-mail.")
                conn.close()

            if errors:
                for e in errors:
                    st.error(e)
            else:
                conn = get_connection()
                conn.execute(
                    "INSERT INTO users (full_name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (full_name_clean, email_clean, hash_password(password), datetime.utcnow().isoformat()),
                )
                conn.commit()
                conn.close()
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                time.sleep(1.1)
                go_to("login")
                st.rerun()

        st.button("← Déjà un compte ? Se connecter", key="go_login_from_register", type="secondary", on_click=go_to, args=("login",))


# ============================================================================
# Page : Mot de passe oublié
# ============================================================================
def render_forgot():
    brand_header()
    with st.container(border=True):
        st.markdown('<p class="auth-title">Mot de passe oublié</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center; color:#64748b; font-size:0.88rem;">'
            "Saisissez votre adresse e-mail, nous vous enverrons un lien pour "
            "réinitialiser votre mot de passe.</p>",
            unsafe_allow_html=True,
        )
        with st.form("forgot_form"):
            email = st.text_input("Adresse e-mail", placeholder="vous@exemple.com")
            submitted = st.form_submit_button("Envoyer le lien")

        if submitted:
            if EMAIL_REGEX.match(email.strip().lower()):
                # En production : envoyer un vrai e-mail avec un lien de réinitialisation.
                st.success(
                    "Si un compte existe avec cette adresse, un lien de "
                    "réinitialisation vient de lui être envoyé."
                )
            else:
                st.error("Adresse e-mail invalide.")

        st.button("← Retour à la connexion", key="go_login_from_forgot", type="secondary", on_click=go_to, args=("login",))


# ============================================================================
# Page : Chatbot (protégée)
# ============================================================================
def render_chat():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        header_html = (
            '<div class="chat-header">'
            f'{ICON_BOT}'
            '<div>'
            '<h1>MathBot</h1>'
            f'<p>Bonjour, {st.session_state.user_name} </p>'
            '</div>'
            '</div>'
        )
        st.markdown(header_html, unsafe_allow_html=True)
    with col_b:
        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            st.button("RESTART", key="restart_btn", help="Recommencer la conversation",
                       on_click=lambda: st.session_state.update(messages=[]))
        with c2:
            st.button("EXIT", key="logout_btn", help="Se déconnecter", on_click=logout)

    # Message de bienvenue au premier affichage
    if not st.session_state.messages:
        st.session_state.messages.append(("bot", "Salut ! Je suis MathBot . "
                                                    "Pose-moi une question sur l'algèbre, la géométrie, "
                                                    "les fractions ou tout autre sujet de mathématiques !",
                                           datetime.now().strftime("%H:%M")))

    messages_container = st.container()
    with messages_container:
        for role, text, ts in st.session_state.messages:
            if role == "user":
                row_html = (
                    '<div class="msg-row user">'
                    '<div class="msg-avatar user-avatar">Moi</div>'
                    f'<div class="msg-bubble">{text}<span class="msg-time">{ts}</span></div>'
                    '</div>'
                )
                st.markdown(row_html, unsafe_allow_html=True)
            else:
                row_html = (
                    '<div class="msg-row bot">'
                    f'<div class="msg-avatar">{ICON_BOT}</div>'
                    f'<div class="msg-bubble">{text}<span class="msg-time">{ts}</span></div>'
                    '</div>'
                )
                st.markdown(row_html, unsafe_allow_html=True)

    user_text = st.chat_input("Écrivez votre question de maths...")
    if user_text:
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append(("user", user_text, now))
        with st.spinner("MathBot réfléchit..."):
            time.sleep(0.5)  # petite pause pour un rendu plus naturel
            reply = get_response(user_text)
        st.session_state.messages.append(("bot", reply, datetime.now().strftime("%H:%M")))
        st.rerun()


# ============================================================================
# Routage principal
# ============================================================================
if st.session_state.view == "chat" and st.session_state.user_id:
    render_chat()
elif st.session_state.view == "register":
    render_register()
elif st.session_state.view == "forgot":
    render_forgot()
else:
    render_login()
