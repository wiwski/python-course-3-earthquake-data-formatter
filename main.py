#!/usr/bin/env python3
"""
Un extracteur de données sismiques au format CSV
"""

import argparse
from pathlib import Path


def main(args):
    """ Main entry point of the app """

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
    print(file_content[0:300])
    # TODO implement earthquake csv data printer


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