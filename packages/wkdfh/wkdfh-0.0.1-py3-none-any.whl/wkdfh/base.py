# -*- coding: UTF-8 -*-

import pywikibot

site = pywikibot.Site("en", "wikipedia")
repo = site.data_repository()

_defaults = {
    "language": "en",
}

def set_default_language(language):
    _defaults["language"] = language

def get_default_language():
    return _defaults["language"]
