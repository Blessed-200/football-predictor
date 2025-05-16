#!/usr/bin/env python3
print("⚙️  main.py arrancó correctamente usando SofaScore API")

from fetch.sofa_api_fetcher import SofaAPIFetcher
from datetime import datetime

def main():
    print("🔍 Obteniendo fixtures de mañana vía SofaScore API…")
    fetcher = SofaAPIFetcher()
    fixtures = fetcher.get_tomorrow_fixtures()

    count = len(fixtures)
    print(f"✅ Se encontraron {count} partidos para mañana.\n")

    if not fixtures:
        print("⚠️ No hay partidos para mañana (o fallo de API).")
        return

    print("🔗 Lista de partidos:")
    for f in fixtures:
        # convertimos timestamp a fecha legible
        dt = datetime.utcfromtimestamp(f["start"]).strftime("%Y-%m-%d %H:%M UTC")
        print(f"- [{f['league']}] {f['home']} vs {f['away']} (horario: {dt})")

if __name__ == "__main__":
    main()
