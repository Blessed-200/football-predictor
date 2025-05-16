from datetime import datetime, timedelta
from LanusStats import SofaScore

class SofaFetcher:
    """
    Fetcher que utiliza SofaScore (via LanusStats) para obtener
    fixtures de una fecha concreta.
    """

    def __init__(self):
        self.scraper = SofaScore()

    def get_fixtures_for_tomorrow(self):
        """
        Devuelve una lista de dicts con 'league', 'home', 'away' para mañana.
        """
        tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        matches = self.scraper.get_fixtures_by_date(date=tomorrow)

        fixtures = []
        for m in matches:
            liga = m.get("tournament", {}).get("name", "Desconocida")
            home = m.get("homeTeam", {}).get("name", "Local")
            away = m.get("awayTeam", {}).get("name", "Visitante")
            fixtures.append({
                "league": liga,
                "home": home,
                "away": away
            })
        return fixtures
