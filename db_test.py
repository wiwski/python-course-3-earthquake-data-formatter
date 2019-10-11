from sqlalchemy.orm import sessionmaker
from db import engine
from sism.tables import create_tables, Earthquake
from sism.models import Catalog
from datetime import datetime

# create_tables(engine)
# Session = sessionmaker(bind=engine)

# session = Session()

all_list=[["time", "latitude", "longitude", "depth", "mag"],["2019-10-07T19:54:50.990Z","38.8356667","-122.8099976","2.08","08.56"],
["2017-10-07T19:54:50.990Z","39.8356667","-122.8099976","3.08","0.56"],["2017-10-07T19:54:50.990Z","37.8356667","-122.8099976","4.08","3.56"]]

# for mylist in all_list:
#     earthquake = Earthquake(time=datetime.strptime(mylist[0],'%Y-%m-%dT%H:%M:%S.%fZ'),latitude=float(mylist[1]),longitude=float(mylist[2]),depth=float(mylist[3]),mag=float(mylist[4]))
#     print(mylist)
    # session.add(earthquake)

# session.commit()

catalog=Catalog.from_csv_list(all_list)
# print(catalog)

# catalog=catalog.keep_biggest(2)
# # catalog.keep_biggest(2)
# print(catalog)
# print()
catalog.stats_catalog()
# print(catalog.stats_catalog())
