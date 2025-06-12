"""
Module pour implémenter des algorithmes de recherche utilisant l'index inversé.

2. Rechercher plusieurs mots (intersection ou union des listes de documents)
3. Calculer les scores de pertinence pour les résultats de recherche
"""

Ce module fournit des fonctionnalités pour :
1. Rechercher des mots simples dans l'index
from typing import Dict, List, Tuple

from indexer import InvertedIndex


class SearchEngine:
    """Classe pour rechercher des documents à l'aide d'un index inversé."""

    def __init__(self, index: InvertedIndex):
        """
        Initialise le moteur de recherche avec un index inversé.

        Args :
            index : L'index inversé à utiliser pour les recherches
        """
        self.index = index

    def search_single_term(self, term: str) -> List[Tuple[str, List[int]]]:
        """
        Recherche les documents contenant un terme unique.

        Args :
            term : Le terme à rechercher

        Returns :
            Liste de tuples (id_doc, positions) pour les documents contenant le terme
        """
        return self.index.get_documents_for_term(term)

    def search_all_terms(self, terms: List[str]) -> List[str]:
        """
        Recherche les documents contenant TOUS les termes spécifiés (opération ET).

        Args :
            terms : Liste des termes à rechercher

        Returns :
            Liste des identifiants de documents contenant tous les termes
        """
        if not terms:
            return []

        # Obtenir les identifiants de documents pour le premier terme
        doc_ids = {doc_id for doc_id, _ in self.index.get_documents_for_term(terms[0])}

        # Intersection avec les identifiants pour les autres termes
        for term in terms[1:]:
            term_doc_ids = {doc_id for doc_id, _ in self.index.get_documents_for_term(term)}
            doc_ids = doc_ids.intersection(term_doc_ids)

            # Arrêt anticipé si l'intersection est vide
            if not doc_ids:
                return []

        return list(doc_ids)

    def search_any_term(self, terms: List[str]) -> List[str]:
        """
        Recherche les documents contenant AU MOINS UN des termes spécifiés (opération OU).

        Args :
            terms : Liste des termes à rechercher

        Returns :
            Liste des identifiants de documents contenant au moins un terme
        """
        doc_ids = set()

        # Union des identifiants de documents pour tous les termes
        for term in terms:
            term_doc_ids = {doc_id for doc_id, _ in self.index.get_documents_for_term(term)}
            doc_ids = doc_ids.union(term_doc_ids)

        return list(doc_ids)

    def calculate_relevance_scores(self, terms: List[str], doc_ids: List[str]) -> Dict[str, float]:
        """
        Calcule les scores de pertinence des documents en fonction de la fréquence des termes.

        Args :
            terms : Liste des termes de la requête
            doc_ids : Liste des identifiants de documents à scorer

        Returns :
            Dictionnaire associant les identifiants de documents à leur score de pertinence
        """
        scores = {}

        for doc_id in doc_ids:
            # Score simple basé sur la fréquence des termes : somme des fréquences
            score = sum(self.index.get_term_frequency(term, doc_id) for term in terms)
            scores[doc_id] = score

        return scores

    def search(self, query: str, use_all_terms: bool = True) -> List[Tuple[str, float]]:
        """
        Recherche les documents correspondant à la requête et retourne les résultats classés.

        Args :
            query : Chaîne de requête de recherche
            use_all_terms : Si True, les documents doivent contenir tous les termes (recherche ET)
                            Si False, les documents peuvent contenir n'importe quel terme (recherche OU)

        Returns :
            Liste de tuples (id_doc, score) triés par score de pertinence (décroissant)
        """
        # Prétraiter la requête comme les documents
        terms = query.lower().split()

        # Trouver les documents correspondants
        if use_all_terms:
            doc_ids = self.search_all_terms(terms)
        else:
            doc_ids = self.search_any_term(terms)

        # Calculer les scores de pertinence
        scores = self.calculate_relevance_scores(terms, doc_ids)

        # Trier les résultats par score décroissant
        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranked_results