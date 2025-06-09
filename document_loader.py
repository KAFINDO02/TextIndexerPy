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

   
   



    
   