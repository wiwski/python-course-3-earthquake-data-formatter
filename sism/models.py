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

    @property
    def time(self):
        return self.__time
    @time.setter
    def time(self, time):
        """
        Check date_time value
        """
        if isinstance(time,str):
            self.__time = time
        else:
            raise ValueError('Date-time must be a string!')

    @property
    def latitude(self):
        return self.__latitude
    @latitude.setter
    def latitude(self, latitude):
        """
        Check latitude value
        """
        if isinstance(latitude,float) or isinstance(latitude,int) or (isinstance(latitude,str) and latitude.isnumeric()):
            self.__latitude = latitude
        else:
            raise ValueError('latitude must be a value!')


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

    @classmethod
    def from_csv_list(cls,rows):
        """
        Gets csv list with first row usgs catalogue header followed by usgs catalogue data
        :return:
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
