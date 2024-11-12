# osint_panel/telegram_lookup.py
import requests

def osint_telegram_lookup(username):
    results = {}

    # Telegram Directory
    try:
        url = f"https://telegram.directory/{username}"
        response = requests.get(url)
        results['Telegram Directory'] = response.url
    except Exception as e:
        results['Telegram Directory'] = str(e)

    # TGStat
    try:
        url = f"https://tgstat.com/search/{username}"
        response = requests.get(url)
        results['TGStat'] = response.url
    except Exception as e:
        results['TGStat'] = str(e)

    return results
