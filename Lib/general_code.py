import pandas as pd
from csv import DictReader
import json
from langdetect import detect
import pystache

def main(url,xml):
 #grab the data and store it in a .csv file.
 page = pd.read_html(url)[0]
 page.to_csv("metadata.csv", header = ["1","2"], index = False)
 with open("metadata.csv") as f:
  values = [row["2"] for row in DictReader(f)]

 with open("metadata.csv") as f:
  rows = [row["1"] for row in DictReader(f)]

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

 #Converting to XML
 dict = {"name": values[0], "country": values[1], "subject": values[2], "lType0": lType[0], "lType1": lType[1],
         "adoptedOn": values[4], "entryIntoForce": values[5], "ISN": values[6], "bibliography": values[7],
         "abstractOrCitation": values[8], "repealedTexts": values[9], "URL": url, "countrycode": cc,
         "languagecode": lang}

 root = pystache.render("<doc source={{{URL}}} identifier={{ISN}}>", dict)
 t1 = pystache.render("<Country code={{{countrycode}}}>{{country}}</Country>", dict)
 t2 = pystache.render("<Language code={{{languagecode}}}>", dict)
 t3 = pystache.render("<name>{{{name}}}</name>", dict)
 t4 = pystache.render("<subject(s)>{{{subject}}}</subject(s)>", dict)
 t6 = pystache.render("<legislationType>")
 t7 = pystache.render("</legislationType>")
 t8 = pystache.render("<adoptedOn>{{{adoptedOn}}}</adoptedOn>", dict)
 t9 = pystache.render("<entryIntoForce>{{{entryIntoForce}}}</entryIntoForce>", dict)
 t10 = pystache.render("<bibliography>{{{bibliography}}}</bibliography>", dict)
 t11 = pystache.render("<abstractOrCitation>{{{abstractOrCitation}}}</abstractOrCitation>", dict)
 t12 = pystache.render("<repealedTexts>{{{repealedTexts}}}</repealedTexts>", dict)
 rootend = pystache.render("</doc>")

 file = open(xml, "w+", encoding="UTF-8")
 file.write(root)
 file.write("\n" + t1)
 file.write("\n" + t2)
 file.write("\n" + t3)
 file.write("\n" + t4)
 file.write("\n" + t5)
 i = 0
 while i < len(lType):
  if lType[i] in ["Law", " Act", "Constitution", " Regulation", " Decree", " Ordinance", "Miscellaneous"]:
   file.write("\n<docType>"+lType[i]+"</docType>")
  i = i + 1
 file.write("\n" + t7)
 file.write("\n" + t8)
 file.write("\n" + t9)
 file.write("\n" + t10)
 file.write("\n" + t11)
 file.write("\n" + t12)
 file.write("\n" + rootend)
 file.close()

'''Function takes 2 arguments:
Argument 1 (url): URL of the webpage
Argument 2 (xmlFile) : Name of the XML file to store the metadata.
Both arguments must be within double quotes.
'''
main(url,xmlFile)