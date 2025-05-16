#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Aseguramos que 'src/' esté en sys.path para importar paquetes locales
SRC_DIR = os.path.dirname(__file__)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

print("⚙️  main.py: orquestador completo")

from model.predictor import build_whole_prediction
import requests

def send_to_telegram(combos):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not combos or not any(combos):
        text = "⚠️ No se generaron picks para mañana."
    else:
        text = "🎯 *Picks para mañana:*\n"
        for idx, combo in enumerate(combos, 1):
            cuota = combo[0]['odds'] * combo[1]['odds']
            text += f"\n*Combinada {idx}* (cuota {cuota:.2f}):\n"
            for pick in combo:
                text += f"- {pick['fixture']} | {pick['market']} | cuota {pick['odds']:.2f}\n"

    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    )
    print("Telegram status:", resp.status_code, resp.text)

def main():
    # 1) Calcular las combinadas
    combos = build_whole_prediction()
    # 2) Enviar notificación
    send_to_telegram(combos)

if __name__ == "__main__":
    main()
