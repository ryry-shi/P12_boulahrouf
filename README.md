### Prérequis
- `installer mysql server`
- ``créer un fichier env avec ces paramètre`
- 
- `PROTOCOL = "mysql"`
- `USERNAME = "root"`
-  `PASSWORD = "MDP_DU_SERVER_MYSQL"`
-  `HOST = "localhost"`
- `DATABASE = "data"`

### Description
- `CRM d'Epic`

### Version
- `1.00`

### Version de Python

- `3.12`

#### Cloner le repository

- `git clone https://github.com/ryry-shi/P12_boulahrouf.git`

### Aller dans le répertoire

- `cd P12_boulahrouf`

#### Créer l'environnement virtuel

- `python -m venv venv`

#### Activer l'environnement virtuel

- `source venv/scripts/activate`

#### Installer les dépendances

- `pip install --requirement requirements.txt`

#### Lancer l'application

- `python main.py`

#### Linting

- `flake8`

#### Coverage

- `coverage report`

#### Tests unitaires

- `pytest`
