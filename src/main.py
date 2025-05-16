import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin

class FBrefSimpleFetcher:
    """
    Scraper ligero de FBref para obtener enlaces de partidos
    filtrados por fecha (mañana).
    """

    BASE_URL = "https://fbref.com"

    def __init__(self, league_url: str):
        """
        league_url: URL de la página de temporada de la liga en FBref,
                    p.ej. https://fbref.com/en/comps/12/La-Liga-Stats
        """
        self.league_url = league_url

    def get_all_match_links(self):
        """
        Descarga la página de la liga y extrae todos los enlaces de partidos.
        """
        resp = requests.get(self.league_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        links = []
        # En FBref, los enlaces de partidos suelen estar en <a> con href que contenga '/en/matches/'
        for a in soup.select("a"):
            href = a.get("href", "")
            if "/en/matches/" in href:
                full = urljoin(self.BASE_URL, href)
                links.append(full)
        # Eliminamos duplicados
        return sorted(set(links))

    def get_tomorrow_links(self):
        """
        Filtra los enlaces que contienen la fecha de mañana.
        FBref pone la fecha en el URL: YYYY-MM-DD
        """
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        all_links = self.get_all_match_links()
        return [l for l in all_links if tomorrow in l]
