import json
import requests

def get_country_codes():
    with open('countryCodes.json', encoding='utf-8') as jsonCountryCodes:
        data = json.load(jsonCountryCodes)

    african_countries = list(
        filter(
            lambda country: country['region-code'] == '002',
            data['countries']['country']
        )
    )

    country_codes = [item['alpha-3'] for item in african_countries]
    return country_codes

def get_html_from_url(url_list):
    r = requests.get(url_list)
    data = r.text
    return data