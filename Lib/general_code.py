import sys
import json
import pystache
from csv import DictReader

import pandas as pd
from langdetect import detect


def get_html_from_url(url):
    page = pd.read_html(url)[0]
    page.to_csv("metadata.csv", header=["1", "2"], index=False)
    with open("metadata.csv") as csv_file:
        rows = [row["1"] for row in DictReader(csv_file)]
    with open("metadata.csv") as csv_file:
        values = [row["2"] for row in DictReader(csv_file)]

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
    # fetch country's code.
    with open("country-codes.json") as countryCode:
        codes = json.load(countryCode)
        codeList = list(codes["countries"]["country"])
        for item in codeList:
            if item["name"] == country_name:
                country_code = (item["alpha-2"])
        return country_code


def get_language_code(detected_language):
    with open("language-Codes.json", encoding="ANSI") as langCode:
        lcodes = json.load(langCode)
        lcodeList = list(lcodes["langs"]["lang"])
        found_lang = ''
        for item in lcodeList:
            if item["alpha2"] == detected_language:
                found_lang = (item["alpha3b"])
        return found_lang


def get_doc_types(lType):
    i = 0
    doc_types = []
    while i < len(lType):
        if lType[i] in [
                "Law",
                " Law"
                "Act",
                " Act",
                "Constitution",
                "Regulation",
                " Regulation",
                "Decree",
                " Decree",
                "Ordinance",
                " Ordinance",
                "Miscellaneous"
            ]:
            doc_types.append("<docType>" + lType[i] + "</docType>")
        i = i + 1
    return '\n'.join(doc_types)


def main(url, xml):
    # grab the data and store it in a .csv file.
    values = get_html_from_url(url)

    # fetch country's code.
    country_code = get_country_code(values[1])

     # detect the document's language.
    detected_language = detect(values[2])  # fetch language's code.

    lang = get_language_code(detected_language)

    # Split "legislationType" field.
    lType = values[5].split(",")

    doc_types = get_doc_types(lType)

    # Converting to XML
    dict1 = {"name": values[2], "country": values[1], "subject": values[3], "adoptedOn": values[4], "ISN": values[0],
             "URL": url, "countrycode": country_code, "languagecode": lang, "docTypes": doc_types}

    doc_template = """<doc source="{{{URL}}}" identifier="{{ISN}}">
             <Country code="{{{countrycode}}}">{{country}}</Country>
             <Language code="{{{languagecode}}}">
             <name>{{{name}}}</name>
             <subjects>{{{subject}}}</subjects>
             <docTypes>
                {{{docTypes}}}
             </docTypes>
             <adoptedOn>{{{adoptedOn}}}</adoptedOn>
        </doc>
    """

    generated_xml_file = pystache.render(doc_template, dict1)

    with open(xml, "w+", encoding="UTF-8") as output_file:
        output_file.write(generated_xml_file)


'''
Script takes 2 arguments:
Argument 1 (url): URL of the webpage
Argument 2 (xmlFile) : Name of the XML file to store the metadata.
Both arguments must be within double quotes.
python general_code.py <url> <xml_file_name>
'''
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
