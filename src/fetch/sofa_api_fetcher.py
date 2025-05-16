import requests
from datetime import datetime, timedelta

class SofaAPIFetcher:
    """
    Fetcher que usa la API pública de SofaScore para sacar
    los encuentros de mañana.
    """

    BASE_URL = "https://api.sofascore.com/api/v1/sport/football/events"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

    def get_tomorrow_fixtures(self):
        """
        Llama a /events/YYYY-MM-DD y devuelve una lista de dicts:
          { league, home, away, startTimestamp }
        """
        tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/{tomorrow}"
        try:
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️ Error al llamar a SofaScore API: {e}")
            return []

        data = r.json().get("events", [])
        fixtures = []
        for ev in data:
            fixtures.append({
                "league": ev.get("tournament", {}).get("name", "Desconocida"),
                "home": ev.get("homeTeam", {}).get("name", "Local"),
                "away": ev.get("awayTeam", {}).get("name", "Visitante"),
                "start": ev.get("startTimestamp")
            })
        return fixtures
