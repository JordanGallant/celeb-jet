from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Replace with your bot token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram message failed: {str(e)}")

@app.route('/check_dates')
def check_dates():
    headers = {
        "Referer": "https://globe.adsbexchange.com",
        "Origin": "https://globe.adsbexchange.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    today_str = datetime.today().strftime("%Y/%m/%d")

    people = [
        {"name": "Bill", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/d6/trace_full_ac39d6.json"},
        {"name": "Drake", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/af/trace_full_a835af.json"},
        {"name": "Elon", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/46/trace_full_ab0a46.json"},
        {"name": "Kim", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/45/trace_full_a18845.json"},
        {"name": "Kylie", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/46/trace_full_ab0a46.json"},
        {"name": "Micheal Jordan", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/e6/trace_full_a21fe6.json"},
        {"name": "Travis", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/ec/trace_full_a988ec.json"},
        {"name": "Trump", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/10/trace_full_aa3410.json"},
        {"name": "Zuck", "url": f"https://globe.adsbexchange.com/globe_history/{today_str}/traces/7d/trace_full_a9247d.json"}
    ]

    successful_results = []

    for person in people:
        try:
            response = requests.get(person["url"], headers=headers, timeout=10)
            if response.status_code == 200:
                successful_results.append({
                    "name": person["name"],
                    "url": person["url"],
                    "status": 200
                })
                print(f"✓ found flight for {person['name']} - 200 OK")
            else:
                print(f"✗ no flight found for {person['name']} - Status {response.status_code}")
        except Exception as e:
            print(f"✗ {person['name']} - Error: {str(e)}")

    # Format message for Telegram
    if successful_results:
        print(f"\n✅ {len(successful_results)} flights found on {datetime.now().strftime('%Y-%m-%d')}:")
    for result in successful_results:
        print(f"- {result['name']} ({result['url']})")
        message = f"✈️ *Flight Check Results ({datetime.now().strftime('%Y-%m-%d')}):*\n"
    for result in successful_results:
        message += f"• {result['name']} - [View Flight]({result['url']})\n"
    else:
        print(f"\n⚠️ No valid flights found for {datetime.now().strftime('%Y-%m-%d')}.")
        message = f"⚠️ No valid flights found for {datetime.now().strftime('%Y-%m-%d')}."

    send_telegram_message(message)

    return jsonify({
        "message": f"Found {len(successful_results)} valid flights",
        "results": successful_results,
    })

if __name__ == '__main__':
    app.run(debug=True)
