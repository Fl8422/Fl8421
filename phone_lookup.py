# osint_panel/phone_lookup.py
import requests
from bs4 import BeautifulSoup

def osint_phone_lookup(phone_number):
    results = {}
    
    # UkrTel
    try:
        url = f"https://ukrtel.com/search?query={phone_number}"
        response = requests.get(url)
        results['UkrTel'] = response.url
    except Exception as e:
        results['UkrTel'] = str(e)

    # Telefonnyjdovidnyk.com.ua
    try:
        url = f"https://telefonnyjdovidnyk.com.ua/search/{phone_number}"
        response = requests.get(url)
        results['Telefonnyjdovidnyk'] = response.url
    except Exception as e:
        results['Telefonnyjdovidnyk'] = str(e)

    # Call Insider
    try:
        url = f"https://callinsider.com/search?number={phone_number}"
        response = requests.get(url)
        results['Call Insider'] = response.url
    except Exception as e:
        results['Call Insider'] = str(e)

    return results
