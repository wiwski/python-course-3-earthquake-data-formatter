""" TODO: Implémentez deux classes Earthquake et Catalog

Earthquake comporte les attributs time, latitude, longitude, depth, mag
que l'on peut passé comme arguments lorsqu'on instancie la classe.

Catalog est une classe représentant un 
"""
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from random import randrange
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

    def sort(self, attribute: str,*args,**kwargs):
        super().sort(key=lambda earthquake: getattr(earthquake, attribute),*args,**kwargs)

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

    def keep_biggest(self,N=5):
        N=min(len(self),N)
        # print(f"  keep N={N} biggest earthquakes, starting from biggest")
        new_catalog=Catalog(self)
        new_catalog.sort("mag",reverse=True)
        return new_catalog[0:N]

    def stats_catalog(self,attribute_histo="mag"):
        from tempfile import TemporaryDirectory
        import base64
        cat2mat=list()
        for i, eqk in enumerate(self):
            cat2mat.append([0,eqk.latitude,eqk.longitude,eqk.depth,eqk.mag])
        mean_var=np.mean(cat2mat,axis=0)
        min_var=np.min(cat2mat,axis=0)
        max_var=np.max(cat2mat,axis=0)
        std_var=np.std(cat2mat,axis=0)
        dico=dict()
        labels_list=self.earthquake_labels()
        arrondi=[0,4,4,3,1]
        for i, attribute in enumerate(labels_list):
            print(type(cat2mat[0][i]))
            if type(cat2mat[0][i])!=type(datetime):
                dico["mean_"+attribute]=round(float(mean_var[i]),arrondi[i])
                dico["min_"+attribute]=round(float(min_var[i]),arrondi[i])
                dico["max_"+attribute]=round(float(max_var[i]),arrondi[i])
                dico["std_"+attribute]=round(float(std_var[i]),arrondi[i])

        nb_bin=10
        imag=labels_list.index(attribute_histo)
        cat2mat=np.array(cat2mat)
        aa=cat2mat[:,imag]
        fig=plt.figure(figsize=[12,8])
        mag_ybins,mag_xbins,patches=plt.hist(aa)
        fig.suptitle(f"Histogrammes des {attribute_histo} pour les {len(self)} séismes sélectionnés", fontsize=14 )
        plt.title (f"Distribués sur {nb_bin} paniers", fontsize=12)
        plt.xlabel(attribute_histo)
        plt.ylabel("Nombre d'occurences")

        suff="png"
        with TemporaryDirectory() as temp_folder:
            fname="{3}/histogramme{0:d}_{1}.{2}".format(randrange(100000),attribute,suff, str(temp_folder))
            fig.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                orientation='paysage', papertype="A4", format=suff,
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
            with open(fname, "rb") as fig_file:
                encoded_fig = base64.b64encode(fig_file.read()).decode('utf-8')
        dico["nb_bin"]=nb_bin

        return (dico, encoded_fig)
