import os
import document_urls as du
"""
Run this script as 

python entry_point.py to process all country urls.

you can set BREAK_AT to a single digit number for testing purposes. 
Otherwise set it to any number greater than 60
"""


BREAK_AT = 3

with open("country_urls.txt", "r") as fcountries:
    countries = fcountries.read()

li_countries = countries.split("\n")
i=0
for country_link in li_countries:
    print("Processing ", country_link)
    du.main(country_link)

    i=i+1
    if (i == BREAK_AT):
        break

