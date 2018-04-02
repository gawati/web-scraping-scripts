import sys
import json
import os
import uuid
from csv import DictReader
import pystache
import pandas as pd
from langdetect import detect
from bs4 import BeautifulSoup
import requests


def __delete_file(file_name):
    """
    Deletes a file
    :param file_name: path to the file
    :return: nothing
    """
    try:
        os.remove(file_name)
    except OSError:
        pass


def __load_template(template_name):
    """
    Loads the template from the file system './templates' folder
    :param template_name: name of the template file
    :return: a string containing the contents of the template
    """
    with open(os.path.join("templates", template_name)) as tmpl_file:
        return tmpl_file.read()


def get_html_from_url(html_page):
    """
    Gets the html from the passed in URL and returns it as a list
    :param url: url to the html page
    :return:
    """
    page = pd.read_html(html_page)[0]

    csv_file_name = str(uuid.uuid4()) + ".csv"

    page.to_csv(csv_file_name, header=["1", "2"], index=False)
    with open(csv_file_name) as csv_file:
        rows = [row["1"] for row in DictReader(csv_file)]
    with open(csv_file_name) as csv_file:
        values = [row["2"] for row in DictReader(csv_file)]

    __delete_file(csv_file_name)

    dictionary = dict((zip(rows, values)))

    data_list = []
    if "ISN:" in rows:
        data_list.insert(0, dictionary.get("ISN:"))
    if "Country:" in rows:
        data_list.insert(1, dictionary.get("Country:"))
    if "Name:" in rows:
        data_list.insert(2, dictionary.get("Name:"))
    if "Subject(s):" in rows:
        data_list.insert(3, dictionary.get("Subject(s):"))
    if "Adopted on:" in rows:
        data_list.insert(4, dictionary.get("Adopted on:"))
    if "Type of legislation:" in rows:
        data_list.insert(5, dictionary.get("Type of legislation:"))

    return data_list


def get_country_code(country_name):
    with open("countryCodes.json", encoding="utf-8") as countryCode:
        codes = json.load(countryCode)
        codeList = list(codes["countries"]["country"])
        country_code = ""
        for item in codeList:
            if item["name"] == country_name:
                country_code = (item["alpha-2"])
        return country_code


def get_language_code(detected_language):
    with open("languageCodes.json", encoding="utf-8") as langCode:
        lcodes = json.load(langCode)
        lcodeList = list(lcodes["langs"]["lang"])
        found_lang = ''
        for item in lcodeList:
            if item["alpha2"] == detected_language:
                found_lang = (item["alpha3b"])
        return found_lang


'''def get_doc_types(document_types):
    doc_types = []
    doc_types  = [ {"name": document_type} for document_type in document_types]
    return doc_types'''


def get_related_country_codes(country_names):
    with open("countryCodes.json", encoding="utf-8") as countryCode:
        codes = json.load(countryCode)
        codeList = list(codes["countries"]["country"])
        country_codes = []
        i = 0
        while i < len(country_names):
            for item in codeList:
                if item["name"] == country_names[i]:
                    country_codes.insert(i, (item["alpha-2"]))
            i = i + 1

    related_country_codes = [{"code": country_code} for country_code in country_codes]
    return related_country_codes


def get_bibliography_text(html_page):
    soup = BeautifulSoup(html_page, "html5lib")

    bibliography_links = soup.find("td", text="Bibliography:").find_next_sibling("td").find_all("a")
    if len(bibliography_links) != 0:
        last_bibliography_link = bibliography_links[-1]
        text = last_bibliography_link.previous_sibling
        bibliography_text = str(text)
        return bibliography_text
    else:
        return None


def get_origin_source_links(html_page):
    soup = BeautifulSoup(html_page, "html5lib")

    bibliography_links = soup.find("td", text="Bibliography:").find_next_sibling("td").find_all("a")
    list_of_bibliography_links = []
    i = 0
    for link in bibliography_links:
        list_of_bibliography_links.insert(i, (link["href"]))
        i = i + 1

    if len(list_of_bibliography_links) != 0:
        del list_of_bibliography_links[-1]
        list_of_origin_source_links = [{"link": link} for link in list_of_bibliography_links]
        return list_of_origin_source_links
    else:
        return None

def get_provider_source_link(html_page):
    soup = BeautifulSoup(html_page, "html5lib")

    bibliography_links = soup.find("td", text="Bibliography:").find_next_sibling("td").find_all("a")
    list_of_bibliography_links = []
    i = 0
    for link in bibliography_links:
        list_of_bibliography_links.insert(i, (link["href"]))
        i = i + 1

    if len(list_of_bibliography_links) != 0:
        provider_source_link = list_of_bibliography_links[-1]
        return provider_source_link
    else:
        return None

def download_provider_source_file(pdf_link, pdf_name, path):
    r = requests.get(pdf_link, stream=True)
    with open(path + pdf_name, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)


def get_html_page(url_or_path):
    if (url_or_path.startswith("http") or url_or_path.startswith("file:")):
        response_page = requests.get(url_or_path)
        return response_page.text
    else:
        with open(url_or_path, mode="r", encoding="utf-8") as f:
            return f.read()


def main(url):
    # grab the data and store it in a .csv file.
    print(" Getting metadata from url...")

    html_page = get_html_page(url)

    values = get_html_from_url(html_page)

    provider_source_link = get_provider_source_link(html_page)
    origin_source_links = get_origin_source_links(html_page)
    bibliography_text = get_bibliography_text(html_page)

    if provider_source_link is not None:
        country_list = [value.strip() for value in values[1].split(",")]
        country_names = country_list[1:]

        # fetch country's code.
        print(" Getting country and language info...")
        country_code = get_country_code(country_list[0])

        # detect the document's language from the language of the name field.
        detected_language = detect(values[2])  # fetch language's code.

        lang = get_language_code(detected_language)

        # document_types = [aType.strip() for aType in values[5].split(",")]
        country_names = [aType.strip() for aType in country_names]

        # document_types_for_template = get_doc_types(document_types)
        related_country_codes_for_template = get_related_country_codes(country_names)

        pdf_link = "http://www.ilo.org/dyn/natlex/" + provider_source_link
        pdf_name = "akn_" + country_code + "_act_" + values[4] + "_" + values[0] + "_" + lang + "_main.pdf"

        output_xml_file = values[0] + ".xml"

        print(" Generating XML... ", output_xml_file)

        # Converting to XML
        dict_for_template = {"name": values[2],
                             "country": country_list[0],
                             "subject": values[3],
                             "adoptedOn": values[4],
                             "ISN": values[0],
                             "URL": url,
                             "countrycode": country_code,
                             "languagecode": lang,
                             "docTypes": values[5],
                             "relatedCountries": related_country_codes_for_template,
                             "providerSource": provider_source_link,
                             "providerDocName": bibliography_text,
                             "originSources": origin_source_links,
                             "fileName": pdf_name}

        if (len(related_country_codes_for_template) > 0):
            dict_for_template["hasRelatedCountries"] = True
            dict_for_template["relatedCountries"] = related_country_codes_for_template

        if (len(origin_source_links) > 0):
            dict_for_template["hasOriginSourceLinks"] = True
            dict_for_template["originSources"] = origin_source_links

        doc_template = __load_template("doc.mxml")

        # apply the mustache template on dict_for_template
        generated_xml_file = pystache.render(doc_template, dict_for_template)

        path = os.path.join("processed_XML_files", country_code, values[0], output_xml_file)
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, "w+", encoding="UTF-8") as output_file:
            output_file.write(generated_xml_file)

        download_provider_source_file(pdf_link, pdf_name, path)

    else:
        print("Unnecessary document. Move on to the next.")


'''
Script takes a single argument: URL of the webpage or the path to the file.
python general_code.py <url_or_file_path>
'''
if __name__ == '__main__':
    main(sys.argv[1])
