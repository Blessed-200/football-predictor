from fetch.fbref import FBrefFetcher

def main():
    # Parámetros de prueba
    season = "2024-2025"
    league = "La Liga"

    print(f"Obteniendo partidos de mañana para {league} {season}...")
    fetcher = FBrefFetcher(wait_time=7)
    links = fetcher.get_tomorrow_match_links(season=season, league=league)

    count = len(links)
    print(f"Se encontraron {count} partidos para mañana.\n")
    if count > 0:
        print("Primeros 5 enlaces:")
        for link in links[:5]:
            print(link)
    else:
        print("No se encontraron partidos de mañana. Revisa la temporada o liga.")

if __name__ == "__main__":
    main()
