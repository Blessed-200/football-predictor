import os
import requests
from datetime import datetime, timedelta
import LanusStats as ls

# Desactivar fuentes externas (evita errores de visualización)
os.environ["MPLSOCCER_FONT"] = "off"

# TOKEN y CHAT_ID directamente aquí
TELEGRAM_BOT_TOKEN = "7852899849:AAHGe4o-19s0wQThBpIqDD0gJ_F1ZctaYSw"
TELEGRAM_CHAT_ID = "8083268965"

def fetch_fixtures_from_sofascore():
    print("Buscando partidos para mañana desde Sofascore...")
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%Y-%m-%d')

    ss = ls.SofaScore()  # CORREGIDO aquí
    fixtures = []

    try:
        data = ss.get_fixtures_by_date(date=date_str)
        for fixture in data:
            league = fixture.get("tournament", {}).get("name", "Desconocida")
            home = fixture.get("homeTeam", {}).get("name", "Local")
            away = fixture.get("awayTeam", {}).get("name", "Visitante")

            # Simulación de goles esperados (por ahora)
            fixture_obj = {
                "match": f"{home} vs {away}",
                "league": league,
                "expected_goals": 2.4
            }

            fixtures.append(fixture_obj)

    except Exception as e:
        print(f"Error obteniendo fixtures: {e}")

    return fixtures

def compute_picks(fixtures):
    picks = []

    for f in fixtures:
        if f["expected_goals"] < 3.5:
            picks.append({
                "match": f["match"],
                "league": f["league"],
                "market": "Under 3.5 goles",
                "odds": 1.60,
                "value": 0.70 - 1 / 1.60
            })

    picks = sorted(picks, key=lambda x: x["value"], reverse=True)[:4]
    combined = []

    for i in range(0, len(picks), 2):
        combined.append(picks[i:i + 2])

    return combined

def send_to_telegram(combos):
    if not combos:
        text = "⚠️ No se generaron picks “Under 3.5 goles” para mañana."
    else:
        text = "🎯 *Picks para mañana:*\n"
        for idx, combo in enumerate(combos, 1):
            cuota = combo[0]["odds"] * combo[1]["odds"]
            text += f"\n*Combinada {idx}* (cuota {cuota:.2f}):\n"
            for pick in combo:
                text += f"- {pick['match']} ({pick['league']}) | {pick['market']} | cuota {pick['odds']:.2f}\n"

    resp = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
    print(f"Telegram status: {resp.status_code}", resp.text)

if __name__ == "__main__":
    fixtures = fetch_fixtures_from_sofascore()
    if not fixtures:
        send_to_telegram([])
    else:
        combos = compute_picks(fixtures)
        send_to_telegram(combos)
