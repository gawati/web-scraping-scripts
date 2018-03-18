import sys
import json
import os
import uuid
from csv import DictReader

import pystache
import pandas as pd
from langdetect import detect


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


def get_html_from_url(url):
    """
    Gets the html from the passed in URL and returns it as a list
    :param url: url to the html page
    :return:
    """
    page = pd.read_html(url)[0]

    # ASHOK: randomized the name of the temporary metadata.csv file
    csv_file_name = str(uuid.uuid4()) + ".csv"

    page.to_csv(csv_file_name, header=["1", "2"], index=False)
    with open(csv_file_name) as csv_file:
        rows = [row["1"] for row in DictReader(csv_file)]
    with open(csv_file_name) as csv_file:
        values = [row["2"] for row in DictReader(csv_file)]

    ## ASHOK: Delete the file, when you call this script from a bigger script
    ## if you don't delete the file it will cause problems e.g. get picked up
    ## even it was not generated simply because it was created by a previous run

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
    #
    # ASHOK: You don't need to do this... you already have the alpha-3 country code in the url.
    #  http://..... 67&p_country=ETH&p_count=164&p_classification=01&p_classcount=79
    #                            ^^^
    #                         See above you just need to the get the country code out of that.
    # fetch country's code.
    with open("countryCodes.json", encoding="utf-8") as countryCode:
        codes = json.load(countryCode)
        codeList = list(codes["countries"]["country"])
        for item in codeList:
            if item["name"] == country_name:
                country_code = (item["alpha-2"])
        return country_code


def get_language_code(detected_language):
    # NEVER use ANSI encoding, always utf-8
    with open("languageCodes.json", encoding="utf-8") as langCode:
        lcodes = json.load(langCode)
        lcodeList = list(lcodes["langs"]["lang"])
        found_lang = ''
        for item in lcodeList:
            if item["alpha2"] == detected_language:
                found_lang = (item["alpha3b"])
        return found_lang

"""
Generates an array of doctype objects like: 

[ {"name": "Law"}, {"name": "Regulation"} .... ]

"""
def get_doc_types(document_types):

    doc_types = []
    doc_types  = [ {"name": document_type} for document_type in document_types]
    return doc_types

    """
    i = 0
    while i < len(lType):
        if lType[i] in [
                "Law",
                "Act",
                "Constitution",
                "Regulation",
                "Decree",
                "Ordinance",
                "Miscellaneous"
            ]:
            doc_types.append("<docType>" + lType[i] + "</docType>")
        i = i + 1
    return '\n'.join(doc_types)
    """

def main(url, output_xml):
    # grab the data and store it in a .csv file.
    print(" Getting metadata from url...")
    values = get_html_from_url(url)

    # fetch country's code.
    print(" Getting country and language info...")
    country_code = get_country_code(values[1])

     # detect the document's language from the language of the citation
    detected_language = detect(values[2])  # fetch language's code.

    lang = get_language_code(detected_language)

    # Split "legislationType" field.
    ## ASHOK: use list comprehension https://www.datacamp.com/community/tutorials/python-list-comprehension
    ## 'lType' is a bit vague changed it to documentTypes
    print(" Generating XML ... ", output_xml)
    document_types = [aType.strip() for aType in values[5].split(",")]

    document_types_for_template = get_doc_types(document_types)

    # Converting to XML
    dict_for_template = {"name": values[2], "country": values[1], "subject": values[3], "adoptedOn": values[4], "ISN": values[0],
             "URL": url, "countrycode": country_code, "languagecode": lang, "docTypes": document_types_for_template}
    #
    ## ASHOK: Load template from file system
    #
    doc_template = __load_template("doc.mxml")

    # apply the mustache template on dict_for_template
    generated_xml_file = pystache.render(doc_template, dict_for_template)

    with open(output_xml, "w+", encoding="UTF-8") as output_file:
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
