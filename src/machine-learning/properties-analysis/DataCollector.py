#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from time import sleep

from src.miscellaneous import pseudoLogger as log


BASE_URL = "https://www.immoscout24.ch/de/immobilien/mieten/"
LOCATION_URL = "ort-{city}"
PAGE_N = "?pn={nbr}"

CITIES = ['bern', 'zuerich', 'basel']

response_string = ""

for city in CITIES:
    log.info("Collecting data from {city}".format(city=city))
    # Collecting 25 pages per city should be enough for now.
    # One page contains up to 24 articles
    for page_nbr in range(1, 25):
        url = BASE_URL + LOCATION_URL.format(city=city) + PAGE_N.format(nbr=page_nbr)
        log.info("Using URL: {url}".format(url=url))
        resp = requests.get(url)
        if resp.status_code == 200:
            log.success("Request succeeded")
            response_string += resp.text
        else:
            # Exceeded the maximum amount of pages
            log.fail("Request failed, continue with next city")
            break
        sleep(2)  # Don't spam them too much

with open("immo_data.raw", "w") as f:
    f.write(response_string)
