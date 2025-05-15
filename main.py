import LanusStats as ls

def debug_inspect():
    # 1) ¿Qué páginas (módulos) podemos usar?
    pages = ls.get_available_pages()
    print("PAGES:", pages)

    # 2) Para cada página, lista las ligas disponibles
    for p in pages:
        leagues = ls.get_available_leagues(p)
        print(f"LEAGUES in {p}:", leagues)

    # 3) Para un ejemplo, mira las temporadas de la primera página y liga
    if pages:
        example_page = pages[0]
        example_league = ls.get_available_leagues(example_page)[0]
        seasons = ls.get_available_season_for_leagues(example_page, example_league)
        print(f"SEASONS for {example_page}–{example_league}:", seasons)

if __name__ == "__main__":
    debug_inspect()
