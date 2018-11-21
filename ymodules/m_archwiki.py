#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

def archwikilink(req):
    import requests
    from urllib.parse import quote
    req = quote(req)
    fullurl = 'https://wiki.archlinux.org/index.php?search=' + req + '&title=Special%3ASearch&go=Go'
    r = requests.get(fullurl, allow_redirects=True, timeout=6)
    if 'search' in r.url:
        return 'No proper result!'
    else:
        return r.url
