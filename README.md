# TextIndexerPy

TextIndexerPy est un projet Python conçu pour indexer, rechercher et analyser efficacement des textes. Il permet de traiter de grands volumes de documents et d'effectuer des recherches textuelles rapides et précises.

## Fonctionnalités

- **Indexation de texte** : Analyse et indexe automatiquement les documents pour accélérer les recherches.
- **Recherche performante** : Permet de retrouver rapidement des documents ou des passages spécifiques grâce à des algorithmes optimisés.
- **Analyse de texte** : Statistiques, extraction de mots-clés, et autres outils d'analyse linguistique.
- **Support de plusieurs formats** : Prise en charge des fichiers texte courants (.txt, .md, etc.).
- **Interface simple** : Utilisation en ligne de commande ou intégrable dans d'autres projets Python.

## Installation

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/KAFINDO02/TextIndexerPy.git
cd TextIndexerPy
pip install -r requirements.txt
```

## Utilisation

Exemple d'utilisation en ligne de commande :

```bash
python text_indexer.py --index dossier_de_textes/
python text_indexer.py --search "mot-clé"
```

Ou dans un script Python :

```python
from textindexer import TextIndexer

indexer = TextIndexer("chemin/vers/dossier")
indexer.build_index()
results = indexer.search("votre recherche")
print(results)
```

## Structure du projet
-`document_loader.py`
- `indexer.py/` : fournit des fonctionalités pour :construire un index inveré(mot->liste de document et position )
- `main_cli.py`  
- `retrieval.py/` 
- `search_engine.py` 

## Contributeur
• KAFINDO KASANGU Emmanuel 
• KAJIMB KASHAL ronelle 
• KAKUDJI NGOY Arsène 
• KALALA TAMBWE Esaïe 
• KALEB KABANGE Caleb
## Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d’informations.

## Auteur

[KAFINDO02](https://github.com/KAFINDO02)
