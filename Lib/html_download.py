import os
import sys
import time
import scrape_utils as su


def get_file_paths(country_codes):
    directory = os.path.join("process_config")
    file_names = [item.lower()+".json" for item in country_codes]
    file_paths = [os.path.join(directory,file_name) for file_name in file_names]

    return file_paths

def write_html_to_file(url, url_list, country_codes, country_code_no):

    raw_html_data = su.get_html_from_url(url)
    time.sleep(5)
    isn = url_list[url_list.index(url)].split('p_isn=')[1].split('&')[0]

    file_name = isn + ".txt"
    file_path = os.path.join("unprocessed_outputs",country_codes[country_code_no].lower(),file_name)
    print(file_path)
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, "w+", encoding="utf-8") as textFile:
        textFile.write(raw_html_data)

def main(country_code_no):

    country_codes = su.get_country_codes()
    file_paths = get_file_paths(country_codes)

    print("Fetching raw HTMl data for each document and saving it as a text file")
    url_list = su.get_document_urls(file_paths[country_code_no])

    for url in url_list:
        write_html_to_file(url, url_list, country_codes,country_code_no)

'''
Function takes one parameter: country_code_no. (0 to 57)
The parameter must be in quotes.

python html_download.py "0" will fetch raw HTML data of all URLs within Algeria's (country code: 0 (DZA)) JSON file (dza.json)
'''
if __name__ == '__main__':
    main(int(sys.argv[1]))