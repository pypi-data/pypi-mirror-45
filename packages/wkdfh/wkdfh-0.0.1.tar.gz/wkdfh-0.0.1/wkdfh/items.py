# -*- coding: UTF-8 -*-

import re

from pywikibot import ItemPage, PropertyPage

from wkdfh.base import repo, get_default_language

def _get_default_label(m):
    language = get_default_language()
    return m.get(language)

_properties_cache = {}

class Property(PropertyPage):
    def __init__(self, property_id, load=True):
        super().__init__(repo, property_id)
        if load:
            self.get()

    @classmethod
    def by_id(cls, item_id, load=True, cache=True):
        if cache and item_id in _properties_cache:
            return _properties_cache[item_id]
        p = cls(item_id, load=load)
        if cache:
            _properties_cache[item_id] = p
        return p


class Item(ItemPage):
    def __init__(self, item_id, load=True):
        super().__init__(repo, item_id)

        self.simple_claims = {}
        self.attributes = {}

        if load:
            self.get()

    def get(self):
        d = super().get()
        if self.claims and not self.simple_claims:
            for claim_id, claim_values in self.claims.items():
                values = []
                for v in claim_values:
                    t = v.target
                    if isinstance(t, ItemPage):
                        t = Item(t.id, load=False)
                    values.append(t)
                self.simple_claims[claim_id] = values
        return d

    @property
    def label(self):
        self.get()
        return _get_default_label(self.labels)

    def populate_attributes(self):
        """
        Create attributes on the item based on its claims. Each claim label is
        transformed into a Python attribute name whose value is the claim’s
        ones. If the claim has multiple values we use a list.

        It also fill those in the ``.attributes`` dictionary attribute.

        This is useful to play with the data but should be used with caution
        because the attribute names are dynamic based on the claim labels.

        >>> p = Item("Q6581072")
        >>> p.populate_attributes()
        >>> p.given_name.label
        'Marcella'
        >>> p.family_name.label
        'Hazan'
        >>> p.sex_or_gender.label
        'female'
        >>> p.viaf_id
        '79375768'
        >>> p.date_of_death
        datetime.date(2013, 9, 29)
        """
        for claim_id, values in self.simple_claims.items():
            p = Property.by_id(claim_id)
            label = p.labels["en"]
            attr = re.sub(r"[^a-z0-9]+", "_", label.lower())
            if not attr:
                continue

            if attr[0].isnumeric():
                attr = "_" + attr

            self.attributes[attr] = values[0] if len(values) == 1 else values

        for attr, claims in self.attributes.items():
            if hasattr(self, attr):
                continue
            setattr(self, attr, claims)
