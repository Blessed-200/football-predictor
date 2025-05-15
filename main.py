import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import LanusStats as ls

load_dotenv()

def fetch_fixtures_and_stats():
    fotmob = ls.FotMob()
    fbref = ls.Fbref()

    # 1. Calcular fecha de mañana
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

    # 2. Ligas que vamos a usar desde FotMob y FBRef
    ligas = {
        'La Liga': 'La Liga',
        'Premier League': 'Premier League',
        'Serie A': 'Serie A',
        'Bundesliga': 'Bundesliga',
        'Ligue 1': 'Ligue 1'
    }

    fixtures = []
    stats_cache = {}

    for league in ligas:
        try:
            print(f"Scrapeando liga: {league}")
            tabla = fotmob.get_season_tables(league=league, season='2024/2025', table_type='total')
            teams = tabla['team'].tolist()

            # Obtener estadísticas desde FBRef
            if league not in stats_cache:
                fav, ag = fbref.get_vs_and_teams_season_stats(
                    page='fbref',
                    league=league,
                    season='2024-2025',
                    stats_type='all'
                )
                df_stats = fav.rename(columns={'goals': 'gf'}).merge(
                    ag.rename(columns={'goals': 'ga'}), on='team'
                )[["team", "gf", "ga"]].set_index("team").to_dict(orient="index")
                stats_cache[league] = df_stats

            # Simulamos fixtures de mañana (con equipos emparejados arbitrariamente)
            for i in range(0, len(teams) - 1, 2):
                home = teams[i]
                away = teams[i + 1]
                home_stats = stats_cache[league].get(home, {"gf": 0, "ga": 0})
                away_stats = stats_cache[league].get(away, {"gf": 0, "ga": 0})
                fixtures.append({
                    "match": f"{home} vs {away}",
                    "league": league,
                    "date": tomorrow,
                    "home_gf": home_stats["gf"],
                    "away_gf": away_stats["gf"]
                })
        except Exception as e:
            print(f"Error en liga {league}: {e}")
            continue

    return fixtures

def compute_picks(fixtures):
    picks = []
    for f in fixtures:
        promedio_goles = f["home_gf"] + f["away_gf"]
        if promedio_goles <= 3.5:
            picks.append({
                "match": f["match"],
                "market": "Under 3.5 goles FT",
                "odds": 1.50,  # fijo por ahora
                "value": 0.70 - 1 / 1.50
            })
    # Tomamos los 4 con más value%
    picks = sorted(picks, key=lambda x: x["value"], reverse=True)[:4]
    # Creamos 2 combinadas de 2 picks
    combined = []
    for i in range(0, len(picks), 2):
        combined.append(picks[i:i+2])
    return combined

def send_to_telegram(combined):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    text = "🎯 *Picks para mañana:*\n"
    for idx, combo in enumerate(combined, 1):
        cuotas = combo[0]["odds"] * combo[1]["odds"]
        text += f"\n*Combinada {idx}* (cuota {cuotas:.2f}):\n"
        for p in combo:
            text += f"- {p['match']} | {p['market']} | cuota {p['odds']:.2f}\n"
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    )

if __name__ == "__main__":
    fixtures = fetch_fixtures_and_stats()
    combinadas = compute_picks(fixtures)
    send_to_telegram(combinadas)
