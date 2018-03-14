import json

data = json.load(open('country_codes.json'))

african_countries = list(
        filter(
        lambda country: country['region-code'] == '002',
        data['countries']['country']
    )
)

ccList = []
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