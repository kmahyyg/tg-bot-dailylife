#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# curl -L 'https://api.ip.sb/geoip/98.142.140.24'
# {"offset":"-7","longitude":-121.9621,"city":"Fremont","timezone":"America\/Los_Angeles",
# "latitude":37.5497,"area_code":"0","region":"California","dma_code":"0",
# "organization":"AS25820 IT7 Networks Inc","country":"United States","ip":"98.142.140.24",
# "country_code3":"USA","postal_code":"94539","continent_code":"NA","country_code":"US",
# "region_code":"CA"}

import requests


def ipsbgeo(ip):
    base = 'https://api.ip.sb/geoip/'
    query = base + str(ip)
    r = requests.get(url=query)
    resp = r.json()
    try:
        str1 = "Latitude: " + str(resp['latitude']) + '\n'
        str2 = "Longtitude: " + str(resp['longitude']) + '\n'
        str4 = "AS: " + resp['organization']
        str3 = "Address: " + resp['country'] + ' ' + resp['region'] + ' ' + resp['city'] + '\n'
    except UnboundLocalError as ubd:
        str3 = "Country: " + resp['country'] + '\n'
    except KeyError as e:
        str3 = "Country: " + resp['country'] + '\n'

    result = str1 + str2 + str3 + str4
    return result
