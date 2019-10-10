""" TODO: Implémentez deux classes Earthquake et Catalog

Earthquake comporte les attributs time, latitude, longitude, depth, mag
que l'on peut passé comme arguments lorsqu'on instancie la classe.

Catalog est une classe représentant un 
"""
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from sism.tables import Earthquake


class Catalog(list):
    
    def __add__(self, rhs):
        return Catalog(super().__add__(rhs))
    
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return Catalog(result)
        except TypeError:
            return result

    def append(self, object):
        if type(object) is not Earthquake:
            raise ValueError("Items in Catalog should be of type Earthquake")
        super().append(object)
    
    def sort(self, attribute: str):
        super().sort(key=lambda earthquake: getattr(earthquake, attribute))

    def save_to_db(self, session):
        for earthquake in self:
            session.add(earthquake)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
        return True

    @classmethod
    def earthquake_labels(cls):
        return ["time", "latitude", "longitude", "depth", "mag"]
