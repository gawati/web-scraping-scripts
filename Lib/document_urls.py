from bs4 import BeautifulSoup
import requests
import json
import sys
import os

#This gets the relative path to the documents
def get_relative_links_of_documents(url):
    response = requests.get(url)
    html_page = response.text
    soup = BeautifulSoup(html_page,"html5lib")
    li = soup.select("ol > li > p > a")
    links = []

    for link in li:
        links.append(link.get('href'))

    return links

#The first half of the URL, combining this with the relative path gives the complete URL.
def get_full_links_of_documents(links):

    s1 = "http://www.ilo.org/dyn/natlex/"
    document_url_list = [s1 + item for item in links]

    return document_url_list

def create_json_data(full_document_links,country_code):
    links_as_objects = [{"url": link} for link in full_document_links]
    country_dict = {"code": country_code}
    country_dict['countries'] = links_as_objects
    print(len(country_dict['countries']))
    data = json.dumps(country_dict, ensure_ascii=False)
    return data

def write_to_json_file(data,country_code):
    file_name = country_code + ".json"
    with open(file_name, "w+", encoding="utf-8") as jsonFile:
        jsonFile.write(data)

    print("File created successfully")

def main(url):

    country_code = url.split('p_country=')[1].split('&')[0]

    relative_document_links = get_relative_links_of_documents(url)
    full_document_links = get_full_links_of_documents(relative_document_links)

    print("Creating JSON data...")
    data = create_json_data(full_document_links,country_code)

    print("Creating and writing the JSON data to a JSON file...")
    write_to_json_file(data,country_code)

'''
Script takes 1 argument: URL of the webpage (must be within double quotes).
python document_urls.py <url>
'''
if __name__ == '__main__':
    main(sys.argv[1])