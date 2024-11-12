# osint_panel/car_lookup.py
import requests

def osint_car_lookup(plate_number):
    results = {}

    # AUTO.RIA
    try:
        url = f"https://auto.ria.com/search/{plate_number}"
        response = requests.get(url)
        results['AUTO.RIA'] = response.url
    except Exception as e:
        results['AUTO.RIA'] = str(e)

    # Ukr.zone
    try:
        url = f"https://ukr.zone/search?query={plate_number}"
        response = requests.get(url)
        results['Ukr.zone'] = response.url
    except Exception as e:
        results['Ukr.zone'] = str(e)

    # Carsua.net
    try:
        url = f"https://carsua.net/search/{plate_number}"
        response = requests.get(url)
        results['Carsua.net'] = response.url
    except Exception as e:
        results['Carsua.net'] = str(e)

    return results
