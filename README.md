# Web application de collecte et d'analyse d'événements sismiques

### Description

Cette application a été développée au cours d'une semaine de formation dédiée à Python et à son utilisation scientifique et sur le web.
Elle permet la collecte de d'événements sismiques - précisément à partir du catalogue fournie par l'[USGS](arthquake.usgs.gov). La donnée est stockée dans une base de données afin de pouvoir être analysée via l'interface de requêtes.
Les données peuvent être analysées afin d'accéder à des résultats comprenant des statistiques, une visualisation cartographique, et des graphiques.

## Installation

### Création de l'environnement virtuel et installation des dépendances

```
python -m venv env
```
Ensuite, après activation de l'environnement:
```
pip install -r requirements.txt
```

### Lancement de l'application (développement)

```
flask run
```

## Stack
* flask
* sqlalchemy
* numpy
* folium
* matplotlib


## Paramètres de requête
Sélection selon les valeurs des attributs des séismes contenus 
dans le catalogue. Dictionnaire avec les clés:
* date_min (!! datetime object)
* date_min (!! datetime object)
* lat_min
* lat_max
* lon_min
* lon_max
* depth_min
* depth_max
* mag_min
* mag_max

