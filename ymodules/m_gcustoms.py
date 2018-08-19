#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
#
# life-tg-bot_google_custom_search
# Copyright (C) 2018  kmahyyg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Check here for API Reference:
# https://developers.google.com/custom-search/json-api/v1/overview
# https://developers.google.com/custom-search/

from urllib.parse import quote,unquote

import requests

from apikey import googleseo_key

baseurl = 'https://www.googleapis.com/customsearch/v1?c2coff=0&cr=countryUS&cx=005159781712139156125%3Aslanvqvnhwu\
&filter=0&num=1&safe=off&q='
gcse_apikey = '&key=' + googleseo_key
custom_header = {'Accept': 'application/json'}


def search_google(querystr):
    querystr = quote(str(querystr), safe='')
    fullreq = baseurl + querystr + gcse_apikey
    r = requests.get(fullreq, headers=custom_header)
    sear_resu = []
    outmsg = ''
    try:
        sear_resu = r.json()['items'][0]
        resu_title = sear_resu['title']
        resu_link = sear_resu['link']
        querystr = unquote(querystr)
        outmsg = str('The Google Result of ') + querystr + " is: \n \n" + str(resu_title) + " \n \n" + str(resu_link)
        outmsg += '\n \n Check Link Preview for more information.'
        return outmsg
    except:
        outmsg = 'Exception Occured @ internal files!'
        return outmsg
