"""
Module pour calculer et afficher des statistiques sur les documents et l'index.

Ce module fournit des fonctionnalités pour :
1. Calculer des statistiques globales (nombre de documents, nombre de mots uniques)
2. Identifier les mots les plus fréquents globalement et dans un document spécifique
3. Afficher les statistiques de façon lisible
"""

from typing import Dict, List, Tuple

from indexer import InvertedIndex


class Statistics:
    """Classe pour calculer et afficher des statistiques sur les documents et l'index."""

    def __init__(self, index: InvertedIndex, documents: Dict[str, str]):
        """
        Initialise avec un index inversé et une collection de documents.

        Args :
            index : L'index inversé
            documents : Dictionnaire associant les identifiants de documents à leur contenu brut
        """
        self.index = index
        self.documents = documents

    def get_document_count(self) -> int:
        """
        Retourne le nombre de documents dans la collection.

        Returns :
            Nombre de documents
        """
        return len(self.documents)

    def get_unique_word_count(self) -> int:
        """
        Retourne le nombre de mots uniques dans l'index.

        Returns :
            Nombre de mots uniques
        """
        return len(self.index.index)

    def get_total_word_count(self) -> int:
        """
        Retourne le nombre total de mots dans tous les documents.

        Returns :
            Nombre total de mots
        """
        return sum(self.index.document_lengths.values())

    def get_most_frequent_words(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Retourne les mots les plus fréquents dans l'ensemble des documents.

        Args :
            limit : Nombre maximal de mots à retourner

        Returns :
            Liste de tuples (mot, fréquence) triée par fréquence décroissante
        """
        word_frequencies = {}

        # Additionner les fréquences sur tous les documents
        for doc_id, term_freqs in self.index.term_frequencies.items():
            for term, freq in term_freqs.items():
                if term not in word_frequencies:
                    word_frequencies[term] = 0
                word_frequencies[term] += freq

        # Trier par fréquence décroissante
        sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

        return sorted_words[:limit]

    def get_document_most_frequent_words(self, doc_id: str, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Retourne les mots les plus fréquents dans un document spécifique.

        Args :
            doc_id : Identifiant du document
            limit : Nombre maximal de mots à retourner

        Returns :
            Liste de tuples (mot, fréquence) triée par fréquence décroissante
        """
        if doc_id not in self.index.term_frequencies:
            return []

        term_freqs = self.index.term_frequencies[doc_id]
        sorted_words = sorted(term_freqs.items(), key=lambda x: x[1], reverse=True)

        return sorted_words[:limit]

    def display_general_stats(self) -> str:
        """
        Affiche les statistiques générales sur la collection de documents.

        Returns :
            Chaîne formatée avec les statistiques
        """
        doc_count = self.get_document_count()
        unique_words = self.get_unique_word_count()
        total_words = self.get_total_word_count()

        stats = f"Statistiques de la collection de documents :\n"
        stats += f"  Nombre de documents : {doc_count}\n"
        stats += f"  Nombre de mots uniques : {unique_words}\n"
        stats += f"  Nombre total de mots : {total_words}\n"

        if doc_count > 0:
            avg_words = total_words / doc_count
            stats += f"  Moyenne de mots par document : {avg_words:.2f}\n"

        return stats

    def display_most_frequent_words(self, limit: int = 10) -> str:
        """
        Affiche les mots les plus fréquents dans l'ensemble des documents.

        Args :
            limit : Nombre maximal de mots à afficher

        Returns :
            Chaîne formatée avec les mots les plus fréquents
        """
        frequent_words = self.get_most_frequent_words(limit)

        result = f"Mots les plus fréquents (tous documents confondus) :\n"
        for i, (word, freq) in enumerate(frequent_words, 1):
            result += f"  {i}. '{word}' - {freq} occurrences\n"

        return result

    def display_document_stats(self, doc_id: str) -> str:
        """
        Affiche les statistiques pour un document spécifique.

        Args :
            doc_id : Identifiant du document

        Returns :
            Chaîne formatée avec les statistiques du document
        """
        if doc_id not in self.documents:
            return f"Document '{doc_id}' introuvable."

        doc_length = self.index.get_document_length(doc_id)
        frequent_words = self.get_document_most_frequent_words(doc_id, 5)

        stats = f"Statistiques pour le document '{doc_id}' :\n"
        stats += f"  Nombre de mots : {doc_length}\n"
        stats += f"  Mots les plus fréquents :\n"

        for i, (word, freq) in enumerate(frequent_words, 1):
            stats += f"    {i}. '{word}' - {freq} occurrences\n"

        return stats