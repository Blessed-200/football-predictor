import os
import LanusStats as ls
import requests
import pandas as pd
from dotenv import load_dotenv

# Carga variables TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID desde .env
load_dotenv()

def fetch_fixtures_and_stats():
    """
    Aquí pondremos el scraping con LanusStats:
      1. Listar partidos del día siguiente.
      2. Obtener estadísticas clave.
      3. Obtener cuotas de mercados.
    """
    fixtures = []
    odds = {}
    return fixtures, odds

def compute_picks(fixtures, odds):
    """
    Aquí aplicaremos nuestra estrategia:
      1. Perfil de partido.
      2. Cálculo p_modelo vs p_implícita.
      3. Value% y filtrado cuota≥1.40.
      4. Seleccionar 4 mejores y agrupar en 2 combinadas.
    """
    picks = []
    return picks

def send_to_telegram(picks):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id   = os.getenv("TELEGRAM_CHAT_ID")
    message = "🎯 *Picks para mañana:*\n"
    for m in picks:
        message += f"- {m['match']} | {m['market']} | cuota {m['odds']:.2f} | value {m['value']:.0%}\n"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    fixtures, odds = fetch_fixtures_and_stats()
    picks = compute_picks(fixtures, odds)
    send_to_telegram(picks)
