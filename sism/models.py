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

    @classmethod
    def from_csv_list(cls,rows):
        """
        Gets csv list with first row usgs catalogue header followed by usgs catalogue data
        :return: Catalog
        """
        index_mapping = {label: index for index, label in enumerate(rows[0]) \
                         if label in cls.earthquake_labels()}

        earthquake_catalogue = Catalog()
        for index, row in enumerate(rows[1:]):
            try:
                earthquake = Earthquake(
                    **{label: row[index] for label, index in index_mapping.items()}
                )
            except IndexError:
                print(f"Element {index+1} in input csv list not correct!")
                continue
            earthquake_catalogue.append(earthquake)

        return earthquake_catalogue

    @classmethod
    def from_query(cls, session, dict_query_params):

        catalogue = session.query(Earthquake).filter(
            Earthquake.time >= dict_query_params['date_min'],
            Earthquake.time <= dict_query_params['date_max'],
            Earthquake.latitude >= dict_query_params['lat_min'],
            Earthquake.latitude <= dict_query_params['lat_max'],
            Earthquake.longitude >= dict_query_params['lon_min'],
            Earthquake.longitude <= dict_query_params['lon_max'],
            Earthquake.depth >= dict_query_params['depth_min'],
            Earthquake.depth <= dict_query_params['depth_max'],
            Earthquake.mag >= dict_query_params['mag_min'],
            Earthquake.mag <= dict_query_params['mag_max']
        )

        return catalogue
