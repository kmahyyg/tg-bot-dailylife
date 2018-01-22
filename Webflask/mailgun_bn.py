#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from apikey import mgcode
import requests
from winmagic import magic


def getfilemime(fileloc):
    mime = magic.Magic(mime=True)
    mimeget = mime.from_file(fileloc)
    return mimeget
