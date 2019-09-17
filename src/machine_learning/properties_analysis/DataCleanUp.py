# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from pprint import pprint
import re
from src.miscellaneous import pseudoLogger as log
from src.machine_learning.properties_analysis.CSVHandler import write_csv, validate_csv


html_example_articles = """
<article class="sc-efAmGo hXkPzi sc-jDwBTQ bIOWur" title="Studios mit grosszÃ¼gigem Balkon">
 <div class="sc-gPEVay gBFLWc">
  <div class="sc-jAaTju etDKqz">
   <div class="sc-jWBwVP eCWReP">
   </div>
  </div>
  <div class="sc-iAyFgw eHJCNZ">
   <span class="sc-keVrkP YzdFL">
    <svg class="sc-iFMziU gdRKbA" sizes="" viewbox="0 0 56 29">
     <defs>
      <path d="M52 24H0V3c0-1.7 1.3-3 3-3h49l-7 12 7 12z" id="s-4a4b70101a-b">
      </path>
      <filter filterunits="objectBoundingBox" height="145.8%" id="s-4a4b70101a-a" width="121.2%" x="-10.6%" y="-18.8%">
       <feoffset in="SourceAlpha" result="shadowOffsetOuter1">
       </feoffset>
       <fegaussianblur in="shadowOffsetOuter1" result="shadowBlurOuter1" stddeviation="1">
       </fegaussianblur>
       <fecolormatrix in="shadowBlurOuter1" result="shadowMatrixOuter1" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.12 0">
       </fecolormatrix>
       <feoffset dy="1" in="SourceAlpha" result="shadowOffsetOuter2">
       </feoffset>
       <fegaussianblur in="shadowOffsetOuter2" result="shadowBlurOuter2" stddeviation="1">
       </fegaussianblur>
       <fecolormatrix in="shadowBlurOuter2" result="shadowMatrixOuter2" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.24 0">
       </fecolormatrix>
       <femerge>
        <femergenode in="shadowMatrixOuter1">
        </femergenode>
        <femergenode in="shadowMatrixOuter2">
        </femergenode>
       </femerge>
      </filter>
     </defs>
     <g fill="none" fill-rule="nonzero">
      <path d="M4 28v-2H2" fill="#975D00">
      </path>
      <g transform="translate(2 2)">
       <use fill="#000" filter="url(#s-4a4b70101a-a)" xlink:href="#s-4a4b70101a-b">
       </use>
       <use fill="#F39C12" fill-rule="evenodd" xlink:href="#s-4a4b70101a-b">
       </use>
      </g>
      <path d="M15.3 19h-2.1v-8.2h-2.7V9H18v1.8h-2.7zM29 14c0 1.7-.4 2.9-1.2 3.8-.8.9-2 1.3-3.5 1.3s-2.7-.4-3.5-1.3c-.8-.9-1.2-2.2-1.2-3.8 0-1.6.4-2.9 1.2-3.8.8-.9 2-1.3 3.5-1.3s2.7.4 3.5 1.3c.8.9 1.2 2.1 1.2 3.8zm-7.3 0c0 1.1.2 2 .6 2.5.4.5 1.1.8 1.9.8 1.7 0 2.5-1.1 2.5-3.4s-.8-3.4-2.5-3.4c-.8 0-1.5.3-1.9.9-.4.6-.6 1.5-.6 2.6zM38.4 12.1c0 1.1-.3 1.9-1 2.5-.7.6-1.6.9-2.9.9h-.9V19h-2.1V9h3.2c1.2 0 2.1.3 2.8.8.6.5.9 1.3.9 2.3zm-4.8 1.6h.7c.7 0 1.1-.1 1.5-.4.4-.3.5-.6.5-1.1 0-.5-.1-.9-.4-1.1-.3-.2-.7-.4-1.3-.4h-1v3z" fill="#FFF">
      </path>
     </g>
    </svg>
   </span>
   <div class="sc-dqvjwr jJiMmN">
    <h3 class="sc-dRFBHB sc-kSFxNF evUype">
     <a class="sc-kGXeez kGCUgG" href="/de/d/wohnung-mieten-bern/5598752?s=1&amp;t=1&amp;l=436&amp;ct=508&amp;ci=6&amp;pn=1">
      1 Zimmer
     </a>
    </h3>
    <h2 class="sc-bUIkmT sc-dsaGNW jmRuKs">
     Â«
     <!-- -->
     Studios mit grosszÃ¼gigem Balkon
     <!-- -->
     Â»
    </h2>
    <div class="sc-hmAwuO sc-fNFDGM MaXUG">
     <a class="sc-kGXeez kGCUgG" href="#">
      <svg class="sc-itybZL hTzQrx" sizes="" viewbox="0 0 24 24">
       <path d="M12 2C8.13 2 5 5.13 5 9c0 4.17 4.42 9.92 6.24 12.11a1 1 0 0 0 1.41.12l.12-.12C14.58 18.92 19 13.17 19 9c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z">
       </path>
      </svg>
      GÃ¼terstrasse 16, 3008 Bern, BE
     </a>
    </div>
    <h3 class="sc-eKQksS sc-hJfILt jWzJWn">
     CHF 1'120.â4 3 1.2.4.4.9.9 1.2 1.4.1.1.3.1.4 0 .3-.4.7-.9 1.2-1.3zM7.5 3c-3 .1-5.4 2.5-5.5 5.5 0 4.1 3.4 6.9 8.6 11.5l.8.7c.4.3.9.3 1.3 0l.8-.7c5.1-4.6 8.5-7.4 8.5-11.5-.1-3.1-2.7-5.6-5.9-5.5-1.6.1-3.1.8-4.1 2-1.1-1.3-2.8-2.1-4.5-2z"&gt;
    </h3>
   </div>
  </div>
 </div>
</article>
<article class="sc-efAmGo hXkPzi sc-jDwBTQ bIOWur" title="Altstadt Studio/BÃ¼ro/Wohnen">
 <div class="sc-gPEVay gBFLWc">
  <div class="sc-jAaTju etDKqz">
   <div class="sc-jWBwVP eCWReP">
   </div>
  </div>
  <div class="sc-iAyFgw eHJCNZ">
   <span class="sc-keVrkP YzdFL">
    <svg class="sc-iFMziU gdRKbA" sizes="" viewbox="0 0 56 29">
     <defs>
      <path d="M52 24H0V3c0-1.7 1.3-3 3-3h49l-7 12 7 12z" id="s-4a4b70101a-b">
      </path>
      <filter filterunits="objectBoundingBox" height="145.8%" id="s-4a4b70101a-a" width="121.2%" x="-10.6%" y="-18.8%">
       <feoffset in="SourceAlpha" result="shadowOffsetOuter1">
       </feoffset>
       <fegaussianblur in="shadowOffsetOuter1" result="shadowBlurOuter1" stddeviation="1">
       </fegaussianblur>
       <fecolormatrix in="shadowBlurOuter1" result="shadowMatrixOuter1" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.12 0">
       </fecolormatrix>
       <feoffset dy="1" in="SourceAlpha" result="shadowOffsetOuter2">
       </feoffset>
       <fegaussianblur in="shadowOffsetOuter2" result="shadowBlurOuter2" stddeviation="1">
       </fegaussianblur>
       <fecolormatrix in="shadowBlurOuter2" result="shadowMatrixOuter2" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.24 0">
       </fecolormatrix>
       <femerge>
        <femergenode in="shadowMatrixOuter1">
        </femergenode>
        <femergenode in="shadowMatrixOuter2">
        </femergenode>
       </femerge>
      </filter>
     </defs>
     <g fill="none" fill-rule="nonzero">
      <path d="M4 28v-2H2" fill="#975D00">
      </path>
      <g transform="translate(2 2)">
       <use fill="#000" filter="url(#s-4a4b70101a-a)" xlink:href="#s-4a4b70101a-b">
       </use>
       <use fill="#F39C12" fill-rule="evenodd" xlink:href="#s-4a4b70101a-b">
       </use>
      </g>
      <path d="M15.3 19h-2.1v-8.2h-2.7V9H18v1.8h-2.7zM29 14c0 1.7-.4 2.9-1.2 3.8-.8.9-2 1.3-3.5 1.3s-2.7-.4-3.5-1.3c-.8-.9-1.2-2.2-1.2-3.8 0-1.6.4-2.9 1.2-3.8.8-.9 2-1.3 3.5-1.3s2.7.4 3.5 1.3c.8.9 1.2 2.1 1.2 3.8zm-7.3 0c0 1.1.2 2 .6 2.5.4.5 1.1.8 1.9.8 1.7 0 2.5-1.1 2.5-3.4s-.8-3.4-2.5-3.4c-.8 0-1.5.3-1.9.9-.4.6-.6 1.5-.6 2.6zM38.4 12.1c0 1.1-.3 1.9-1 2.5-.7.6-1.6.9-2.9.9h-.9V19h-2.1V9h3.2c1.2 0 2.1.3 2.8.8.6.5.9 1.3.9 2.3zm-4.8 1.6h.7c.7 0 1.1-.1 1.5-.4.4-.3.5-.6.5-1.1 0-.5-.1-.9-.4-1.1-.3-.2-.7-.4-1.3-.4h-1v3z" fill="#FFF">
      </path>
     </g>
    </svg>
   </span>
   <div class="sc-dqvjwr jJiMmN">
    <h3 class="sc-dRFBHB sc-kSFxNF evUype">
     <a class="sc-kGXeez kGCUgG" href="/de/d/wohnung-mieten-bern/5598445?s=1&amp;t=1&amp;l=436&amp;ct=511&amp;ci=8&amp;pn=1">
      2 Zimmer
      <!-- -->
      ,
      <!-- -->
      75 mÂ²
     </a>
    </h3>
    <h2 class="sc-bUIkmT sc-dsaGNW jmRuKs">
     Â«
     <!-- -->
     Altstadt Studio/BÃ¼ro/Wohnen
     <!-- -->
     Â»
    </h2>
    <div class="sc-hmAwuO sc-fNFDGM MaXUG">
     <a class="sc-kGXeez kGCUgG" href="#">
      <svg class="sc-itybZL hTzQrx" sizes="" viewbox="0 0 24 24">
       <path d="M12 2C8.13 2 5 5.13 5 9c0 4.17 4.42 9.92 6.24 12.11a1 1 0 0 0 1.41.12l.12-.12C14.58 18.92 19 13.17 19 9c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z">
       </path>
      </svg>
      MÃ¼nstergasse 66, 3011 Bern, BE
     </a>
    </div>
    <h3 class="sc-eKQksS sc-hJfILt jWzJWn">
     CHF 1'990.â
    </h3>
    <button class="sc-VigVT kOGvyo sc-bZQynM fiDOJL" type="button">
     Favorit
     <svg class="sc-gZMcBi gFubBx" sizes="" viewbox="0 0 24 24">
      <path d="M13.4 6.3c.8-.9 2-1.4 3.3-1.3 1.9.1 3.3 1.6 3.4 3.5 0 3-3.1 5.7-7.9 10l-.2.1-.1-.1C7.1 14.2 4 12 4 8.5 4.1 6.6 5.7 5.1 7.6 5c1.1 0 2.2.4 3 1.2.4.4.9.9 1.2 1.4.1.1.3.1.4 0 .3-.4.7-.9 1.2-1.3zM7.5 3c-3 .1-5.4 2.5-5.5 5.5 0 4.1 3.4 6.9 8.6 11.5l.8.7c.4.3.9.3 1.3 0l.8-.7c5.1-4.6 8.5-7.4 8.5-11.5-.1-3.1-2.7-5.6-5.9-5.5-1.6.1-3.1.8-4.1 2-1.1-1.3-2.8-2.1-4.5-2z">
      </path>
     </svg>
    </button>
   </div>
  </div>
 </div>
</article>
"""


def clean_umlaut(string):
    """
    # Ã¤ = ä
    # Ã¶ = ö
    # Ã¼ = ü
    :param string:
    :return:
    """
    # TODO: This would still fail for é,è ê etc. -> Encode this properly! (e.g UTF-8)
    return string.replace('Ã¤', 'ä').replace('Ã¶', 'ö').replace('Ã¼', 'ü')


def clean_address(address_txt):
    """
    Extracts the street, streen number, PLZ, and place out of a given address.
    Just consider happy-path. IndexError gets raised if the address_txt is not complete.

    :param address_txt: Address string. E.g "Hebelstrasse 109, 4056 Basel, BS"
    :raises IndexError, ValueError
    :return:
    """
    partitioned_address = address_txt.split(', ')

    street = clean_umlaut(re.findall('[^0-9]+', partitioned_address[0])[0].strip())
    # Does not include possible characters after the street number like: 13a
    street_nbr = re.findall('\d+', partitioned_address[0])[0]
    plz = re.findall('\d{4}', partitioned_address[1])[0]
    place = clean_umlaut(re.findall('[^0-9]+', partitioned_address[1])[0].strip())
    canton = partitioned_address[2]
    return street, street_nbr, plz, place, canton


def clean_room_info(room_info_txt):
    """
    Extracts the number of rooms and the area (square meters) out of a given room info string.
    Just consider happy-path. IndexError gets raised if the room_info_txt is not complete.

    :param room_info_txt: Room info string. E.g "3.5 Zimmer, 86 mÂ²"
    :raises IndexError
    :return:
    """
    partitioned_room_info = room_info_txt.split(', ')
    rooms = partitioned_room_info[0].split(' ')[0]
    area = re.findall('\d+', partitioned_room_info[1]).pop()
    return rooms, area


def clean_price(price_txt):
    """
    Extracts the price as a number out of a given price string.
    Just consider happy-path. IndexError gets raised if the room_info_txt is not complete.

    :param price_txt: Price text string. E.g "CHF 2'110.â"
    :raises IndexError, ValueError
    :return:
    """
    price_str = re.findall('\d*\'?\d+', price_txt)[0]
    price = int(price_str.replace('\'', ''))  # Remove the thousands separator
    return price


def get_cleaned_data(soup, limit=-1):
    limit_counter = 0
    failures = 0
    # Street, Number, PLZ, place, canton, rooms, area, price
    data_list = []

    # !!! Beware !!! These strings have to be adjusted to a given data set!
    address_identify_class_string = 'sc-kGXeez kGCUgG'
    rooms_identify_class_string = 'sc-dRFBHB sc-kSFxNF evUype'
    price_identify_class_string = 'sc-eKQksS sc-hJfILt jWzJWn'

    articles = soup.find_all('article')
    articles_size = len(articles)
    limit = articles_size if limit < 0 else limit

    log.info("Total articles: {na}".format(na=articles_size))
    log.info("Limit of articles: {la}".format(la=limit))

    for article in articles:
        #print(article['title'])
        #print('-------------')
        try:
            # Do room info cleaning first! Some articles do not display the amount of square meters -> fail fast!
            room_info_txt = article.find_all('h3', {'class': rooms_identify_class_string}).pop().text
            # print(room_info_txt)
            nbr_of_rooms, area = clean_room_info(room_info_txt)

            address_txt = article.find_all('a', {'class': address_identify_class_string}).pop().text
            # print(address_txt)
            if address_txt == room_info_txt:
                # It may happen, that there is no street (and number) given in the address
                # In that case, the address tag is no <a> but a <span> tag.
                # So the class-string does match wrong and address_txt becomes the same value as room_info_txt
                raise ValueError
            street, street_nbr, plz, place, canton = clean_address(address_txt)

            price_txt = article.find_all('h3', {'class': price_identify_class_string}).pop().text
            # print(price_txt)
            price = clean_price(price_txt)

        except IndexError:
            failures += 1
            continue
        except ValueError:
            failures += 1
            continue

        data_list.append((street, street_nbr, plz, place, canton, nbr_of_rooms, area, price))

        limit_counter += 1
        if limit_counter == limit:
            break

    treated_articles = limit_counter + failures

    log.info(f"Treated {treated_articles} articles")
    log.info(f"Number of failures: {failures}")
    log.info("Fail-rate: {fr}%".format(fr=str(round((failures/treated_articles)*100, 2))))
    return data_list


if __name__ == '__main__':
    # About 1600 articles
    #with open("properties_html_data_BE_BS_ZH_26.07.19.raw", "r") as file_handler:
    with open("properties_html_data_LU_WT_TH_BI_27.07.19.raw", "r") as file_handler:
        soup = BeautifulSoup(file_handler, features="html.parser")

    #print(soup.find_all('article').pop(9).prettify())
    data = get_cleaned_data(soup)
    print(data)
    print(len(data))

    write_csv('properties_data_2.csv', data, data_description=('street', 'number', 'plz',
                                                               'place', 'canton', 'rooms',
                                                               'area', 'price'))
    validate_csv('properties_data_2.csv', (str, int, int, str, str, float, int, int))




