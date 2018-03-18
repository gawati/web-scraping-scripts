import json

with open('countryCodes.json', encoding='utf-8') as jsonCountryCodes:
    data = json.load(jsonCountryCodes)


african_countries = list(
        filter(
          lambda country: country['region-code'] == '002',
          data['countries']['country']
        )
    )

#
## ASHOK: Used String substituion for country code here to make it cleaerer
# see http://thomas-cokelaer.info/blog/2011/05/python-string-substitution-using-dictionaries/
#
iloSourceCountryLink = "http://www.ilo.org/dyn/natlex/natlex4.countrySubjects?p_lang=en&p_country=%(country)s"

ccList = [item['alpha-3'] for item in african_countries]

listOfLinksToPages = [ iloSourceCountryLink % {'country': countryCode}  for countryCode in ccList]

print("\n".join(listOfLinksToPages))

# ASHOK much easier doing list comprehension and string substitution like above than a for loop
""""
i = 0
for item in african_countries:
 ccList.insert(i,(item["alpha-3"]))
 i = i + 1

s1 = "http://www.ilo.org/dyn/natlex/natlex4.countrySubjects?p_lang=en&p_country="

urlList = []
i = 0
for item in ccList:
 urlList.insert(i,s1+ccList[i])
 i = i + 1

i = 0
while i != len(urlList):
 print(urlList[i])
 i = i + 1
"""
