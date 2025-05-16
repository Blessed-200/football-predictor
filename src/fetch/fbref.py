import re
from datetime import datetime, timedelta
from LanusStats.scraperfc.fbref import FBref

class FBrefFetcher:
    """
    Clase para obtener partidos de FBref filtrados por fecha (mañana)
    """

    def __init__(self, wait_time: int = 7):
        # tiempo de espera entre peticiones (por defecto 7s)
        self.scraper = FBref(wait_time=wait_time)

    def get_tomorrow_match_links(self, season: str, league: str):
        """
        Devuelve la lista de URLs de partidos de mañana para la temporada y liga dadas.
        """
        # 1) obtenemos todos los enlaces de la temporada
        all_links = self.scraper.get_match_links(year=season, league=league)

        # 2) calculamos la fecha de mañana en formato YYYY-MM-DD
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # 3) filtramos enlaces que contienen la fecha de mañana
        tomorrow_links = [link for link in all_links if tomorrow in link]
        return tomorrow_links

    def scrape_match(self, link: str):
        """
        Scrapea un partido concreto y devuelve un DataFrame con todas las stats disponibles.
        """
        return self.scraper.scrape_match(link=link)
