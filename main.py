import requests
from datetime import datetime, timedelta
from LanusStats.sofascore import Sofascore

# Telegram directo en el código
TELEGRAM_BOT_TOKEN = "7852899849:AAHGe4o-19s0wQThBpIqDD0gJ_F1ZctaYSw"
TELEGRAM_CHAT_ID = "8083268965"

def get_fixtures_for_tomorrow():
    sofascore = Sofascore()
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    date_str = tomorrow.strftime('%Y-%m-%d')

    print(f"Obteniendo partidos para el {date_str}...\n")
    matches = sofascore.get_fixtures_by_date(date_str)
    
    juegos = []
    for match in matches:
        equipos = match.get("teams")
        if equipos:
            home = equipos.get("home", {}).get("name", "")
            away = equipos.get("away", {}).get("name", "")
            league = match.get("tournament", {}).get("name", "")
            if home and away:
                juegos.append(f"{league}: {home} vs {away}")
    return juegos

def send_to_telegram(text):
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
    print("Estado del envío:", response.status_code)
    print("Respuesta de Telegram:", response.text)

if __name__ == "__main__":
    fixtures = get_fixtures_for_tomorrow()
    if fixtures:
        mensaje = "📅 *Partidos para mañana:*\n\n" + "\n".join(f"- {f}" for f in fixtures[:20])
    else:
        mensaje = "⚠️ No se encontraron partidos para mañana."

    send_to_telegram(mensaje)
