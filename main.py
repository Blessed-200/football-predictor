import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import LanusStats as ls

load_dotenv()

def fetch_fixtures():
    fb = ls.Fbref()
    leagues = ['La Liga', 'Premier League', 'Serie A', 'Bundesliga', 'Ligue 1']
    season = '2024-2025'
    fixtures = []

    for league in leagues:
        try:
            print(f"Procesando: {league}")
            fav, ag = fb.get_vs_and_teams_season_stats(
                league=league,
                season=season,
                stat="stats"
            )

            # Usamos los nombres correctos de las columnas
            df = fav.rename(columns={"Squad": "team", "Gls": "gf"}).merge(
                ag.rename(columns={"Squad": "team", "Gls": "ga"}), on="team"
            )

            teams = df.to_dict(orient="records")
            for i in range(0, len(teams) - 1, 2):
                home = teams[i]
                away = teams[i+1]
                fixtures.append({
                    "match": f"{home['team']} vs {away['team']}",
                    "home_gf": home["gf"],
                    "away_gf": away["gf"]
                })
        except Exception as e:
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
    combined = []
    for i in range(0, len(picks), 2):
        combined.append(picks[i:i+2])
    return combined

def send_to_telegram(combos):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not combos:
        text = "⚠️ No se generaron picks para mañana."
    else:
        text = "🎯 *Picks para mañana:*\n"
        for idx, combo in enumerate(combos, 1):
            cuota = combo[0]["odds"] * combo[1]["odds"]
            text += f"\n*Combinada {idx}* (cuota {cuota:.2f}):\n"
            for pick in combo:
                text += f"- {pick['match']} | {pick['market']} | cuota {pick['odds']:.2f}\n"
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    )

if __name__ == "__main__":
    fixtures = fetch_fixtures()
    combos = compute_picks(fixtures)
    send_to_telegram(combos)
