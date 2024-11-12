# osint_panel/email_lookup.py
import requests

def osint_gmail_lookup(email):
    results = {}

    # Pipl
    try:
        url = f"https://pipl.com/search/?q={email}"
        response = requests.get(url)
        results['Pipl'] = response.url
    except Exception as e:
        results['Pipl'] = str(e)

    # Spokeo
    try:
        url = f"https://spokeo.com/search?q={email}"
        response = requests.get(url)
        results['Spokeo'] = response.url
    except Exception as e:
        results['Spokeo'] = str(e)

    return results
