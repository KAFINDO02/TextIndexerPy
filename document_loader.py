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
   
   



    
   