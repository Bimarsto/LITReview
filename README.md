# LITReview
>Ce programme a été créé dans le cadre du projet 9 du parcours "Développeur d'application - Python" d'OpenClassrooms.
Il s'agit d'une application web réalisée avec Django.  
L'application est un réseau social permettant de demander et poster des critiques de livres.
***

## Installation et utilisation :

### Prérequis:

Cette application a été développée avec : 
[<img src=https://img.shields.io/badge/Python-3.10.6-blue>](https://www.python.org/downloads/release/python-3106/)

### Etapes d'installation:

* Depuis votre console, placez-vous dans le dossier de votre choix 
puis clonez ce repository à l'aide le la commande :  

```git clone https://github.com/Bimarsto/LITReview.git```

* Placez-vous dans le dossier cloné, puis créez un environnement virtuel :  

```python -m venv <nom de l'environnement>```

* Activez le :
  * Sous windows:  
    ```<nom de l'environnement>\scripts\activate.bat```

  * Sous mac ou linux:  
    ```source <nom de l'environnement>/bin/activate```  
<br/>
* Installez les packages et frameworks requis :  

```pip install -r requirements.txt```

* Effectuez les migrations :

```python manage.py migrate```

* Il ne vous reste plus qu'à lancer le serveur :

```python manage.py runserver```

* Vous pouvez ensuite utiliser l'application depuis votre navigateur à l'adresse suivante :  

```http://127.0.0.1:8000```