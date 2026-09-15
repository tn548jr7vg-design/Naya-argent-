
        
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from tavily import TavilyClient

# Initialisation des clés via les variables d'environnement
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
DESTINATION_EMAIL = os.environ.get("DESTINATION_EMAIL")

# Clients API
ai_client = genai.Client(api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = DESTINATION_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, DESTINATION_EMAIL, msg.as_string())
        server.quit()
        print("Rapport envoyé par e-mail avec succès.")
    except Exception as e:
        print(f"Erreur d'envoi e-mail : {e}")

def run_agent():
    print("Agent Naya Business en cours d'exécution...")
    
    # 1. Recherche web via Tavily
    search_query = "micro SaaS opportunities pain points small businesses reddit indiehackers"
    search_results = tavily_client.search(query=search_query, max_results=5)
    
    # 2. Analyse via Gemini API
    prompt = f"""
    Tu es Naya Business, un agent autonome d'analyse d'opportunités Micro-SaaS.
    Voici les données récentes collectées sur le web :
    {search_results}
    
    Rédige un rapport synthétique et structuré en HTML avec :
    1. Résumé des besoins/problèmes détectés.
    2. 3 idées précises de Micro-SaaS rentables.
    3. Plan d'action pour le lancement.
    """
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    # 3. Envoi du rapport
    send_email("📊 Rapport Naya Business - Opportunités Micro-SaaS", response.text)

if __name__ == "__main__":
    run_agent()
