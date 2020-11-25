# GEL3021D4E1
DESIGN IV - projet Ali Quebec

dépendances à installer: 
> pip install -r requirements.txt

langages:
python
html
css
javascript
sql


# Lancer le serveur
> python manage.py runserver


# Utilisation 1 - GUI

## 1 - Aller sur le lien
http://127.0.0.1:8000/

## 2.1 - Vision artificielle
choisir reconnaissance par vision et le type traitement
## 2.2 - Code barre
chosir reconnaissance de code barre
## 3 - Upload
choisir une image depuis votre ordinateur ou faire un glisser-déposer de l'image
## 4 - cliquer sur soumettre
la reconnaissance par vision artificielle fais deux types de traitements:
- une reconnaissance de texte (ingrédients et valeurs nutritives)
- ue reconnaissance de logos utilisant du machine learning

Pour la reconnaissance de logos, il faut obligatoirement créer un dossier 'weights' dans la racine contenant le projet et y insérer les différents fichiers .weights :
> dir  
  
  >> GEL30211D4E1
  
  >> weights/*.weigts

  
# Utilisation 2 - API
S'assurer que le serveur est bien lancé;

Ouvrir le fichier main/test_api.py;

changer le file_path par le chemin de l'image que vous souhaitez traiter;

Lancer(run) le fichier test_api.py

Vous pouvez également faire votre propre fichier de requêtes pour l'api ou passer par un autre service comme Postman; les adresses pour les différents traitements sont dans le fichier.


# Utilisation 3 - lien web heroku (en développement)
Il est possible de réaliser la plupart des étapes ci-dessus en se rendant sur le lien : http://alivisiond4.herokuapp.com/

Le traitement de la reconnaissance de logos n'y ait pas supporté par contre.
