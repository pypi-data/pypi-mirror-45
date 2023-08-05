# Wikidata for humans

**wkdfh** is a Python module for humans who want to work with Wikidata.

It’s a wrapper around [`pywikibot`](https://www.mediawiki.org/wiki/Manual:Pywikibot)
that adds a couple shortcuts to ease data exploration.

**Note:** This is really experimental at this point.

## Example

```pycon
>>> import wkdfh
>>> p = wkdfh.Item("Q6756362")
>>> p.label
'Marcella Hazan'
>>> p.populate_attributes()
>>> p.given_name.label
'Marcella'
>>> p.family_name.label
'Hazan'
>>> p.sex_or_gender.label
'female'
>>> p.viaf_id
'79375768'
```

## Install

    pip install wkdfh

Requirement: Python 3.
