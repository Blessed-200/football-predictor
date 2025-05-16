from datetime import datetime
from fetch.bbc_fetcher import BBCFetcher
# Si más adelante integras fbref_simple o sofa_api, impórtalos aquí
# from fetch.understat_fetcher import UnderstatFetcher

def fear_intuition_predict(fixtures):
    """
    Aplica tu algoritmo de 'miedo + intuición + estadística'.
    Recibe lista de fixtures:
      [{league, home, away}, ...]
    Devuelve dos combinadas, cada combinada es lista de 2 picks:
      [{'fixture': ..., 'market': ..., 'odds': ..., 'value': ...}, ...]
    """

    picks = []
    # Ejemplo de métrica sencilla: apostar Under 3.5 si partido de liga top
    for f in fixtures:
        liga = f['league'].lower()
        match = f"{f['home']} vs {f['away']}"
        # Regla de ejemplo: si es La Liga o Premier, under 3.5
        if 'la liga' in liga or 'premier' in liga:
            odds = 1.50
            # value = diferencia intuida vs cuota
            value = 0.65 - 1/odds
            picks.append({
                'fixture': match,
                'market': 'Under 3.5 goles',
                'odds': odds,
                'value': value
            })
        else:
            # fallback: ambos marcan (BTTS)
            odds = 1.80
            value = 0.55 - 1/odds
            picks.append({
                'fixture': match,
                'market': 'Ambos marcan',
                'odds': odds,
                'value': value
            })

    # Ordenamos por valor descendente y nos quedamos con los top 4
    top = sorted(picks, key=lambda x: x['value'], reverse=True)[:4]

    # Formamos 2 combinadas de 2 picks cada una
    combined = [ top[0:2], top[2:4] ]
    return combined


def build_whole_prediction():
    """
    Función auxiliar para integrarse directamente en main.py.
    """
    # 1) Obtener fixtures de mañana
    fixtures = BBCFetcher().get_tomorrow_fixtures()
    # 2) Calcular las dos combinadas
    combos = fear_intuition_predict(fixtures)
    return combos
