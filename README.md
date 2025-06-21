# TextIndexerPy

TextIndexerPy est un projet Python destiné à l'indexation et à la recherche de texte. Ce projet propose des outils permettant de créer un index de documents textuels et d'effectuer des recherches efficaces à travers ces documents.

## Fonctionnalités

- Indexation de fichiers texte.
- Recherche rapide de mots ou d'expressions dans l'ensemble des documents indexés.
- Interface simple à utiliser et à étendre.

## Installation

Clonez le dépôt puis installez les dépendances requises, le cas échéant :

```bash
git clone https://github.com/KAFINDO02/TextIndexerPy.git
cd TextIndexerPy
# Installer les dépendances si un fichier requirements.txt est présent
# pip install -r requirements.txt
```

## Utilisation

Exemple d’indexation et de recherche :

```python
# Exemple d'utilisation à compléter selon la structure du projet
from textindexer import Indexer

indexer = Indexer()
indexer.index_folder("chemin/vers/les/fichiers")
resultats = indexer.search("mot_à_chercher")
print(resultats)
```

> Adapter ce bloc selon l’API réelle du projet.

## Structure du projet

- document_loader.py
- indexer.py
- main_cli.py
- retrieval.py
- searh_engine
- stat

## Contributeurs

 - KAFINDO KASANGU Emmanuel 
 - KAJIMB KASHAL ronelle 
 - KAKUDJI NGOY Arsène 
 - KALALA TAMBWE Esaïe 
 - KALEB KABANGE Caleb



## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
