import os
os.environ["MPLSOCCER_FONT"] = "off"
import requests
from datetime import datetime, timedelta
import LanusStats as ls

# Token y chat ID insertados para prueba
TELEGRAM_BOT_TOKEN = "7852899849:AAHGe4o-19s0wQThBpIqDD0gJ_F1ZctaYSw"
TELEGRAM_CHAT_ID = "8083268965"

def fetch_fixtures():
    fb = ls.Fbref()
    leagues = ['La Liga', 'Premier League', 'Serie A', 'Bundesliga', 'Ligue 1']
    season = '2024-2025'
    fixtures = []

    for league in leagues:
        try:
            fav, ag = fb.get_vs_and_teams_season_stats(
                league=league,
                season=season,
                stat="stats"
            )
            # Renombrar columnas correctas
            df = fav.rename(columns={"Squad": "team", "Gls": "gf"}).merge(
                ag.rename(columns={"Squad": "team", "Gls": "ga"}), on="team"
            )
            teams = df.to_dict(orient="records")
            # Empareja consecutivos
            for i in range(0, len(teams) - 1, 2):
                home = teams[i]
                away = teams[i+1]
                fixtures.append({
                    "match": f"{home['team']} vs {away['team']}",
                    "home_gf": home["gf"],
                    "away_gf": away["ga"] if "ga" in away else away["gf"]
                })
        except Exception as e:
            # si falla una liga, sigue con la siguiente
            print(f"Error en {league}: {e}")
            continue

    return fixtures

def compute_picks(fixtures):
    picks = []
    for f in fixtures:
        total = f["home_gf"] + f["away_gf"]
        if total <= 3.5:
            picks.append({
                "match": f["match"],
                "market": "Under 3.5 goles",
                "odds": 1.50,
                "value": 0.70 - 1/1.50
            })
    picks = sorted(picks, key=lambda x: x["value"], reverse=True)[:4]
    combined = [picks[i:i+2] for i in range(0, len(picks), 2)]
    return combined

def send_message(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
    print("Telegram status:", r.status_code, r.text)

if __name__ == "__main__":
    # 1) Sacar fixtures reales
    fixtures = fetch_fixtures()
    if fixtures:
        msg = "📅 *Partidos para mañana:*\n\n" + "\n".join(f"- {f['match']}" for f in fixtures)
    else:
        msg = "⚠️ No se encontraron partidos para mañana."
    send_message(msg)

    # 2) Generar picks
    combos = compute_picks(fixtures)
    if not combos:
        send_message("⚠️ No se generaron picks “Under 3.5 goles” para mañana.")
    else:
        text = "🎯 *Picks para mañana (Under 3.5):*\n"
        for idx, combo in enumerate(combos, 1):
            cuota = combo[0]["odds"] * combo[1]["odds"]
            text += f"\n*Combinada {idx}* (cuota {cuota:.2f}):\n"
            for p in combo:
                text += f"- {p['match']} | {p['market']} | cuota {p['odds']:.2f}\n"
        send_message(text)
