import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))

def envoyer_mail(destinataire: str, sujet: str, contenu: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = MAIL_FROM
        msg["To"] = destinataire
        msg["Subject"] = sujet
        msg.attach(MIMEText(contenu, "html"))

        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, destinataire, msg.as_string())
        return True
    except Exception as e:
        print(f"Erreur envoi mail : {e}")
        return False

def mail_bienvenue(email: str, prenom: str):
    sujet = "Bienvenue chez Vite & Gourmand !"
    contenu = f"""
    <h2>Bonjour {prenom},</h2>
    <p>Bienvenue chez <strong>Vite & Gourmand</strong> !</p>
    <p>Votre compte a été créé avec succès.</p>
    <p>À bientôt,<br>L'équipe Vite & Gourmand</p>
    """
    return envoyer_mail(email, sujet, contenu)

def mail_confirmation_commande(email: str, prenom: str, commande_id: int):
    sujet = "Confirmation de votre commande"
    contenu = f"""
    <h2>Bonjour {prenom},</h2>
    <p>Votre commande <strong>#{commande_id}</strong> a bien été enregistrée.</p>
    <p>Nous vous contacterons prochainement pour confirmer les détails.</p>
    <p>À bientôt,<br>L'équipe Vite & Gourmand</p>
    """
    return envoyer_mail(email, sujet, contenu)

def mail_commande_terminee(email: str, prenom: str, commande_id: int):
    sujet = "Votre commande est terminée - Donnez votre avis !"
    contenu = f"""
    <h2>Bonjour {prenom},</h2>
    <p>Votre commande <strong>#{commande_id}</strong> est terminée.</p>
    <p>Connectez-vous à votre espace pour laisser votre avis.</p>
    <p>À bientôt,<br>L'équipe Vite & Gourmand</p>
    """
    return envoyer_mail(email, sujet, contenu)