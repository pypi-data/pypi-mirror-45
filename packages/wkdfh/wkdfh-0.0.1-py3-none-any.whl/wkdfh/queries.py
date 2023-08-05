# -*- coding: UTF-8 -*-

from pywikibot.data.sparql import SparqlQuery

__all__ = ["query"]

def query(q):
    return SparqlQuery.select(q)
