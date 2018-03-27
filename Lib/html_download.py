import os
import sys
import json
import time
import functions_for_ilo_natlex as fin


def get_file_paths(country_codes):
    directory = os.path.join("process_config")
    file_paths = [directory + "\\" + item.lower()+".json" for item in country_codes]

    return file_paths

def get_document_urls(file_paths):
    with open(file_paths, encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)

    url_data = data["countries"]
    url_list = [item['url'] for item in url_data]
    return url_list

def write_html_to_file(url_list,country_codes,j,country_code_no):
    raw_html_data = fin.get_html_from_url(url_list[j])
    time.sleep(5)
    isn = url_list[j].split('p_isn=')[1].split('&')[0]

    file_name = isn + ".txt"
    file_path = os.path.join("unprocessed_outputs",country_codes[country_code_no].lower(),file_name)
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, "w+", encoding="utf-8") as textFile:
        textFile.write(raw_html_data)

def main(file_no,country_code_no):

    country_codes = fin.get_country_codes()
    file_paths = get_file_paths(country_codes)

    print("Fetching raw HTMl data for each document and saving it as a text file")
    url_list = get_document_urls(file_paths[file_no])

    j = 0
    while j < len(url_list):
        write_html_to_file(url_list,country_codes,j,country_code_no)
        j = j + 1

'''
Function takes two parameters: file no. and Country_code no.
Both parameters must be equal. That is, if file_no. is 0 then country_code_no. must also be 0.
Both parameters must be in quotes.

python html_download.py "0" "0" will download HTML data of all URLs in Algeria's JSON file (dza.json)
'''
if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))