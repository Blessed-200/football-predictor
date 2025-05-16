# Football Predictor

Proyecto para automatizar pronósticos de fútbol con scraping de estadísticas y notificaciones por Telegram.

## Estructura
- `src/fetch`: scrapers FBref, SofaScore, Understat…
- `src/store`: almacenamiento (CSV / SQLite)
- `src/features`: extracción de características (xG, córners, tarjetas…)
- `src/model`: algoritmo de “miedo + intuición”
- `src/notify`: envío a Telegram
- `data/`: datos guardados
- `.github/workflows`: configuración de GitHub Actions
