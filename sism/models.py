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
                print(f"Couldn't save earthquake: {earthquake}")
                session.rollback()
        return True

    @classmethod
    def earthquake_labels(cls):
        return ["time", "latitude", "longitude", "depth", "mag"]

    @classmethod
    def from_csv_list(cls, rows):
        """
        Gets csv list with first row usgs catalogue header followed by usgs catalogue data
        :return: Catalog
        """
        index_mapping = {label: index for index, label in enumerate(rows[0])
                         if label in cls.earthquake_labels()}

        earthquake_catalogue = Catalog()
        for index, row in enumerate(rows[1:]):
            try:
                eq_dict = {label: row[index]
                           for label, index in index_mapping.items()}
                eq_dict['time'] = datetime.strptime(
                    eq_dict['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
                for float_label in ('latitude', 'longitude', 'depth', 'mag'):
                    eq_dict[float_label] = float(eq_dict[float_label])
                earthquake = Earthquake(**eq_dict)
            except IndexError:
                print(f"Element {index+1} in input csv list not correct!")
                continue
            earthquake_catalogue.append(earthquake)

        return earthquake_catalogue

    @classmethod
    def from_query(cls, session, query_params: dict):

        query = session.query(Earthquake)

        if query_params.get('date_min', None):
            query = query.filter(Earthquake.time >= query_params['date_min'])
        if query_params.get('date_max', None):
            query = query.filter(Earthquake.time <= query_params['date_max'])
        if query_params.get('lat_min', None):
            query = query.filter(Earthquake.latitude >= query_params['lat_min'])
        if query_params.get('lat_max', None):
            query = query.filter(Earthquake.latitude <= query_params['lat_max'])
        if query_params.get('lon_min', None):
            query = query.filter(Earthquake.longitude >= query_params['lon_min'])
        if query_params.get('lon_max', None):
            query = query.filter(Earthquake.longitude <= query_params['lon_max'])
        if query_params.get('depth_min', None):
            query = query.filter(Earthquake.depth >= query_params['depth_min'])
        if query_params.get('depth_max', None):
            query = query.filter(Earthquake.depth <= query_params['depth_max'])
        if query_params.get('mag_min', None):
            query = query.filter(Earthquake.mag >= query_params['mag_min'])
        if query_params.get('mag_max', None):
            query = query.filter(Earthquake.mag <= query_params['mag_max'])

        catalogue = Catalog(query.all())

        return catalogue
