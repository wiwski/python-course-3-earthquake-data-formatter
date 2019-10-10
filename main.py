#!/usr/bin/env python3
"""
Un extracteur de données sismiques au format CSV
"""

import argparse
from pathlib import Path

from sism.models import Earthquake, Catalog

def main(args):
    """ Main entry point of the app """

    labels_wanted = ["time", "latitude", "longitude", "depth", "mag"]

    # On récupère le path du fichier à partir des arguments entrés par l'utilisateur
    file_path = Path(args.file)
    # On peut utilisé cet argument pour trié les résultats
    sort_by = args.sort_by

    # On essaie d'ouvrir le fichier à partir du path
    try:
        # Utilisation du block with qui referme le fichier une fois qu'on en a plus besoin
        with open(str(file_path), 'r') as f:
            file_content = f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError("The file you gave do not exist. Pass a real file as argument.")

    # On vérifie le contenu récupéré
    rows = file_content.split("\n")
    rows = [[col for col in row.split(",")] for row in rows]

    index_mapping = {label: index for index, label in enumerate(rows[0]) \
                       if label in labels_wanted}
    earthquake_catalog = Catalog()
    for index, row in enumerate(rows[1:]):
        try:
            earthquake = Earthquake(
                **{label: row[index] for label, index in index_mapping.items()}
            )
        except IndexError:
            continue
        earthquake_catalog.append(earthquake)
        

    # [time, latitude, longitude, ...]
    filtered_labels = Catalog.earthquake_labels()

    print("\t\t".join(filtered_labels))
    print("_" * 50)
    print("\n")

    rows_to_display = rows[1:15]
    if sort_by:
        earthquake_catalog.sort(sort_by)

    for earthquake in earthquake_catalog[:15]:
        print(earthquake)

    print("_" * 50)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Argument requis
    # i.e "venv" dans python -m venv
    parser.add_argument("file", help="Le path vers le fichier contenant la donnée")

    # Flag optionnel avec paramètre
    parser.add_argument("-s", "--sorted", action="store", dest="sort_by")
    
    args = parser.parse_args()
    main(args)