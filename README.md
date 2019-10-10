# Exercice d'extraction et de formattage de données sismiques à partir d'un fichier CSV

### Objectif
L'objectif est d'extraire la donnée de fichiers CSV contenant des relevés sismiques à partir du site [earthquake.usgs.gov](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php).

Pour lancer le script, on utilise:
```shell
python main.py <path/csv/file>
```

Le script doit extraire l'information du fichier et la mettre en forme en l'affichant sur le terminal. Une première ligne indique les labels de chaque colonne, 
on affiche ensuite les 15 premiers résultats.
Les différents paramètres sont listé [ici](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php). On retiendra seulement `time`, `latitude`, `longitude`, `depth`, et `mag`.

La mise en forme peut se faire dans ce style:<br><br>
![Image](https://i.ytimg.com/vi/qZMX2qUJRoU/hqdefault.jpg)


#### Optionnel

L'utilisateur peut passer un flag `-s` ou `--sort` pour trier les résultats par un paramètre précis.

# Sélection dans la BDD
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

