import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_to_telegram(combos):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not combos:
        text = "⚠️ No se generaron picks para mañana.\nRevisa si los promedios de goles eran altos."
    else:
        text = "🎯 *Picks simulados para prueba:*\n"
        for idx, combo in enumerate(combos, 1):
            cuota = combo[0]["odds"] * combo[1]["odds"]
            text += f"\n*Combinada {idx}* (cuota {cuota:.2f}):\n"
            for pick in combo:
                text += f"- {pick['match']} | {pick['market']} | cuota {pick['odds']:.2f}\n"

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    )
    
    print("Estado del envío:", response.status_code)
    print("Respuesta de Telegram:", response.text)

if __name__ == "__main__":
    # Simulación de picks para forzar el envío
    picks_simulados = [[
        {
            "match": "Real Madrid vs Barcelona",
            "market": "Under 3.5 goles",
            "odds": 1.55,
            "value": 0.03
        },
        {
            "match": "Liverpool vs Chelsea",
            "market": "Under 3.5 goles",
            "odds": 1.50,
            "value": 0.03
        }
    ]]
    
    send_to_telegram(picks_simulados)
