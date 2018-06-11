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
    except KeyError as e1:
        str1 = "Latitude: Failed to get. \n"
    except UnboundLocalError as ubd1:
        pass

    try:
        str2 = "Longtitude: " + str(resp['longitude']) + '\n'
    except KeyError as e2:
        str2 = "Longtitude: Failed to get. \n"
    except UnboundLocalError as ubd2:
        pass

    try:
        str3 = "AS: " + str(resp['organization']) + '\n'
    except KeyError as e4:
        str3 = "AS: Failed to get. \n"
    except UnboundLocalError as ubd3:
        pass

    try:
        str4 = "Country: " + str(resp['country']) + '\n'
    except KeyError as e4:
        str4 = "Country: Failed to get. \n"
    except UnboundLocalError as ubd4:
        pass

    try:
        str5 = "Region: " + str(resp['region']) + '\n'
    except KeyError as e5:
        str5 = "Region: Failed to get. \n"
    except UnboundLocalError as ubd5:
        pass

    try:
        str6 = "City: " + str(resp['city']) + '\n'
    except KeyError as e6:
        str6 = "City: Failed to get. \n"
    except UnboundLocalError as ubd6:
        pass

    result = str1 + str2 + str3 + str4 + str5 + str6
    return result
