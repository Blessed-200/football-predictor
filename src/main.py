#!/usr/bin/env python3
print("⚙️  main.py arrancó correctamente usando SofaScore")

from fetch.sofascore_fetcher import SofaFetcher

def main():
    print("🔍 Obteniendo fixtures de mañana desde SofaScore…")
    fetcher = SofaFetcher()
    fixtures = fetcher.get_fixtures_for_tomorrow()

    count = len(fixtures)
    print(f"✅ Se encontraron {count} partidos para mañana.\n")

    if count:
        print("🔗 Lista de partidos:")
        for f in fixtures:
            print(f"- {f['league']}: {f['home']} vs {f['away']}")
    else:
        print("⚠️ No se encontraron partidos para mañana.")

if __name__ == "__main__":
    main()
