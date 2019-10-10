""" TODO: Implémentez deux classes Earthquake et Catalog

Earthquake comporte les attributs time, latitude, longitude, depth, mag
que l'on peut passé comme arguments lorsqu'on instancie la classe.

Catalog est une classe représentant un 
"""

class Earthquake:

    def __init__(self, time, latitude, longitude, depth, mag):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.mag = mag

    def __repr__(self):
        return f"Earthquake, mag {self.mag} / {self.time} / {self.latitude},{self.longitude}"


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
    
    @classmethod
    def earthquake_labels(cls):
        return ["time", "latitude", "longitude", "depth", "mag"]
