import pandas as pd
import csv
from csv import DictReader
from xml.etree.ElementTree import Element, SubElement, tostring
import json
from langdetect import detect

def main(url,xml):
 #grab the data and store it in a .csv file.
 page = pd.read_html(url)[0]
 page.to_csv("metadata.csv", header = ["1","2"], index = False) #A csv file with name "metadata" will be created.
 with open("metadata.csv") as f:
  values = [row["2"] for row in DictReader(f)]
 
 #fetch country's code.
 with open("country-codes.json") as countryCode:
  codes = json.load(countryCode)
  countryCode.close()
  codeList = list(codes["countries"]["country"])
  for item in codeList:
   if item["name"] == values[1]:
    cc = (item["alpha-2"])
 
 #detect the document's language.
 l = detect(values[8])
 
 #fetch language's code.
 with open("language-Codes.json",encoding="ANSI") as langCode:
  lcodes = json.load(langCode)
  langCode.close()
  lcodeList = list(lcodes["langs"]["lang"])
  for item in lcodeList:
   if item["alpha2"] == l:
    lang = (item["alpha3b"])
 
 #Split "legislationType" field.
 lType = values[3].split(",")
 
 #build XML and store in a separate file.
 root = Element("doc source="+url+" identifier="+values[6])
 r = SubElement(root, "country code="+cc)
 r.text = values[1]
 a = SubElement(root, "language code="+lang)
 b = SubElement(root, "name")
 b.text = values[0]
 c = SubElement(root, "subjects")
 c.text = values[2]
 d = SubElement(root, "legislationType")
 d1 = SubElement(d, "docType")
 d1.text = lType[0]
 d2 = SubElement(d, "docType")
 d2.text = lType[1]
 e = SubElement(root, "adoptedOn")
 e.text = values[4]
 f = SubElement(root, "EntryIntoForce")
 f.text = values[5]
 g = SubElement(root, "ISN")
 g.text = values[6]
 h = SubElement(root, "bibliography")
 h.text = values[7]
 i = SubElement(root, "abstractOrCitation")
 i.text = values[8]
 j = SubElement(root, "repealedTexts")
 j.text = values[9]
 data = tostring(root,encoding="utf-8",method="xml").decode("utf-8")
 file = open(xml,"w+") #An XML file with the name passed by the user will be created.
 file.write(data)
 file.close()

#function call. Pass two parameters: the webpage's URL and the name of the XML (with extension) file where the XML metadata will be stored.
#both parameters must be within quotes.
#main(,)