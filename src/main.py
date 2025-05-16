#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pista de arranque
print("⚙️  ¡main.py arrancó correctamente!")

from fetch.fbref_simple import FBrefSimpleFetcher

def main():
    # Pistas de depuración
    print("🔍 Iniciando la búsqueda de enlaces…")
    print("📁 Usando FBrefSimpleFetcher para La Liga 2024-2025")

    # URL de la temporada de La Liga 2024-25 en FBref
    liga_url = "https://fbref.com/en/comps/12/2024-2025/La-Liga-Stats"
    fetcher = FBrefSimpleFetcher(league_url=liga_url)

    print("📥 Descargando enlaces de partidos de mañana…")
    links = fetcher.get_tomorrow_links()

    print(f"✅ Se encontraron {len(links)} partidos para mañana.\n")
    if links:
        print("🔗 Enlaces:")
        for link in links:
            print(link)
    else:
        print("⚠️ No se encontraron enlaces para mañana.")

if __name__ == "__main__":
    main()
