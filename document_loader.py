import os
import string
from typing import List, Dict

def load_documents(directory_path: str) -> Dict[str, str]:
   documents = {}
   if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Répertoire introuvable : {directory_path}")

    
   