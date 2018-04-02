import os
import sys
import time
import json
import scrape_utils as su


def get_file_path(country_code):
    directory = os.path.join("process_config")
    file_name = country_code.lower()+".json"
    file_path = os.path.join(directory,file_name)

    return file_path


SLEEP_DELAY=4

def write_html_to_file(url, url_list, country_code):

    raw_html_data = su.get_html_from_url(url)
    time.sleep(SLEEP_DELAY)
    isn = url_list[url_list.index(url)].split('p_isn=')[1].split('&')[0]

    file_name = isn + ".txt"
    file_path = os.path.join("unprocessed_outputs",country_code.lower(),file_name)
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, "w+", encoding="utf-8") as textFile:
        textFile.write(raw_html_data)

    return file_name

def update_country_json_file(country_code, url, url_list, file_path, file_name):

    with open(file_path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        data["countries"][url_list.index(url)]["file"] = file_name
        #print(data)
    with open(file_path, "w", encoding="utf-8") as writeJsonFile:
        json.dump(data, writeJsonFile)


def main(country_code):

    file_path = get_file_path(country_code)

    print("Fetching raw HTMl data for each document and saving it as a text file")
    url_list = su.get_document_urls(file_path)
    print("Found %d urls to download for %s" % (len(url_list), country_code) )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for idx, url in enumerate(url_list):
        if "file" not in data["countries"][url_list.index(url)]:
            file_name = write_html_to_file(url, url_list, country_code)
            print("File %d of %d created successfully" % (idx+1, len(url_list)) )
            update_country_json_file(country_code, url, url_list, file_path, file_name)
        else:
            print("File %d for url %s already exists, ignoring" % (idx+1, url))

'''
Function takes one parameter: country_code
The parameter must be in quotes.

python html_download.py "dza" will fetch raw HTML data of all URLs within Algeria's JSON file (dza.json)
'''
if __name__ == '__main__':
    main(sys.argv[1])
