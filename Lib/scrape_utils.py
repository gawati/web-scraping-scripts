import json
import requests
from fake_useragent import UserAgent

def get_country_codes(country_code):
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
    #if country_code in country_codes:


UA = UserAgent()

def get_html_from_url(url):
    header = {'User-Agent': str(UA.random)}
    r = requests.get(url, headers=header)
    data = r.text
    return data
	
def get_document_urls(file_path):
    with open(file_path, encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)

    url_data = data["countries"]
    url_list = [item['url'] for item in url_data]
    return url_list
	
