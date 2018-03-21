from bs4 import BeautifulSoup
# http://www.ilo.org/dyn/natlex/natlex4.detail?p_lang=en&p_isn=101766&p_country=DJI&p_count=280&p_classification=03&p_classcount=3
html = """
<a href="http://www.presidence.dj/texte.php?ID=133&amp;ID2=2016-03-24&amp;ID3=Loi" onclick="return popup(this, 'notes')" title="Loi">
Loi 
<img src="http://www.ilo.org/webcommon/dyn/images/natlex4/images/externalLink.gif" 
    alt="Loi" 
    width="17" height="14">
</a> 
Site Officiel de la République de Djibouti, JO - Secrétariat général du Gouvernement, Djibouti 
<a href="docs/ELECTRONIC/101766/122772/F253643777/DJI-101766.pdf" onclick="return popup(this, 'notes')" title="PDF">PDF <img src="http://www.ilo.org/webcommon/dyn/images/natlex4/images/externalLink.gif" alt="PDF" width="17" height="14"></a> <font size="1">(consulted on 2016-04-22)</font><br>

"""

soup = BeautifulSoup(html)

all_links = soup.findAll('a')

last_link_is_always_the_pdf = all_links[-1]

print(last_link_is_always_the_pdf.previous_sibling)