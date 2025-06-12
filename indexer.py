"""
Module pour construire un index inversé à partir de documents prétraités.

Ce module fournit des fonctionnalités pour :
1. Construire un index inversé (mot -> liste de documents et positions)
2. Calculer la fréquence des termes (TF) pour chaque mot dans chaque document
"""

from typing import Dict, List, Tuple
import document_loader


class InvertedIndex:
    """Classe représentant un index inversé pour la recherche de documents."""

    def __init__(self):
        """Initialise un index inversé vide."""
        self.index = {}  # mot -> [(id_doc, [positions])]
        self.document_lengths = {}  # id_doc -> nombre de tokens
        self.term_frequencies = {}  # id_doc -> {mot -> fréquence}

    def build_index(self, documents: Dict[str, str]):
        """
        Construit l'index inversé à partir d'une collection de documents.

        Args :
            documents : Dictionnaire associant les identifiants de documents à leur contenu brut
        """
        # Récupérer les positions des tokens pour tous les documents
        token_positions = document_loader.get_token_positions(documents)

        # Calculer la longueur des documents
        preprocessed_docs = document_loader.preprocess_documents(documents)
        for doc_id, tokens in preprocessed_docs.items():
            self.document_lengths[doc_id] = len(tokens)

        # Construire l'index inversé
        for doc_id, positions_dict in token_positions.items():
            # Initialiser les fréquences des termes pour ce document
            self.term_frequencies[doc_id] = {}

            for token, positions in positions_dict.items():
                # Mettre à jour la fréquence du terme
                self.term_frequencies[doc_id][token] = len(positions)

                # Mettre à jour l'index inversé
                if token not in self.index:
                    self.index[token] = []
                self.index[token].append((doc_id, positions))

    def get_documents_for_term(self, term: str) -> List[Tuple[str, List[int]]]:
        """
        Récupère tous les documents contenant le terme spécifié.

        Args :
            term : Le terme à rechercher

        Returns :
            Liste de tuples (id_doc, positions) pour les documents contenant le terme
        """
        term = term.lower()  # Normaliser le terme
        return self.index.get(term, [])

    def get_term_frequency(self, term: str, doc_id: str) -> int:
        """
        Récupère la fréquence d'un terme dans un document spécifique.

        Args :
            term : Le terme dont on veut la fréquence
            doc_id : L'identifiant du document

        Returns :
            La fréquence du terme dans le document
        """
        term = term.lower()  # Normaliser le terme
        return self.term_frequencies.get(doc_id, {}).get(term, 0)

    def get_document_length(self, doc_id: str) -> int:
        """
        Récupère la longueur (nombre de tokens) d'un document.

        Args :
            doc_id : L'identifiant du document

        Returns :
            Le nombre de tokens dans le document
        """
        return self.document_lengths.get(doc_id, 0)