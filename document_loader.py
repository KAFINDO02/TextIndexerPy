import os
import string
from typing import List, Dict

def load_documents(directory_path: str) -> Dict[str, str]:
   documents = {}
   if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Répertoire introuvable : {directory_path}")
   for filename in os.listdir(directory_path):
      if filename.endswith('.txt'):
         file_path = os.path.join(directory_path, filename)
         try:
            with open(file_path, 'r', encoding='utf-8') as file:
               content = file.read()
               documents[filename] = content
         except Exception as e:
            print(f"Erreur lors du chargement du fichier {filename} : {e}")
            
    return documents
def tokenize(text: str) -> List[str]:
    """
    Découpe le texte en tokens (mots).

    Args :
        text : Texte d'entrée à tokeniser

    Returns :
        Liste de tokens
    """
    # Mettre en minuscules
    text = text.lower()

    # Supprimer la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Découper en mots
    tokens = text.split()

    return tokens

def preprocess_documents(documents: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Prétraite tous les documents par tokenisation et normalisation.

    Args :
        documents : Dictionnaire associant les identifiants de documents à leur contenu brut

    Returns :
        Dictionnaire associant les identifiants de documents à des listes de tokens prétraités
    """
    preprocessed_docs = {}

    for doc_id, content in documents.items():
        tokens = tokenize(content)
        preprocessed_docs[doc_id] = tokens

    return preprocessed_docs

def get_token_positions(documents: Dict[str, str]) -> Dict[str, Dict[str, List[int]]]:
    """
    Récupère les positions de chaque token dans chaque document.

    Args :
        documents : Dictionnaire associant les identifiants de documents à leur contenu brut

    Returns :
        Dictionnaire associant les identifiants de documents à des dictionnaires associant les tokens à leurs positions
    """
    token_positions = {}

    for doc_id, content in documents.items():
        # Mettre en minuscules
        content = content.lower()

        # Supprimer la ponctuation
        content = content.translate(str.maketrans('', '', string.punctuation))

        # Découper en mots et suivre les positions
        tokens = content.split()
        positions = {}

        for position, token in enumerate(tokens):
            if token not in positions:
                positions[token] = []
            positions[token].append(position)

        token_positions[doc_id] = positions

    return token_positions



   
   



    
   