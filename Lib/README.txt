This repository contains general code only.

The encoding of the original JSON files was changed to be compatible with ElementTree.
country-codes.json : Encoding utf-8-sig (changed from utf-8 BOM)
language-Codes.json : Encoding ANSI (changed from utf-8)

Python version: 3.6

Libraries: pandas, lxml, html5lib, BeautifulSoup4, pystache, langdetect, requests

Installing:

 # install Python 3.6 ; Install pip.
 # then run :

    ```
    pip install lxml html5lib BeautifulSoup4 pystache langdetect requests fake-useragent
    pip install pandas
    ```
