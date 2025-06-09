"""
Module pour trier et afficher les résultats de recherche.

Ce module fournit des fonctionnalités pour :
1. Trier les documents récupérés selon leur score de pertinence
2. Afficher les résultats avec nom du document, score et extraits (snippets) montrant le contexte des mots-clés
"""

from typing import Dict, List, Tuple

from indexer import InvertedIndex
from search_engine import SearchEngine


def highlight_all_terms(snippet: str, terms: List[str]) -> str:
    """
    Met en évidence toutes les occurrences des termes donnés dans l'extrait.
    Gère à la fois les termes simples et les expressions multi-mots.

    Args :
        snippet : L'extrait de texte
        terms : Liste des termes à mettre en évidence

    Returns :
        Extrait avec tous les termes surlignés
    """
    tokens = snippet.split()

    # D'abord, gérer les expressions multi-mots
    i = 0
    while i < len(tokens):
        for term in terms:
            term_words = term.lower().split()
            if len(term_words) <= 1:
                continue
            if i + len(term_words) > len(tokens):
                continue
            match = True
            for j, term_word in enumerate(term_words):
                clean_token = ''.join(c for c in tokens[i+j] if c.isalnum()).lower()
                if clean_token != term_word:
                    match = False
                    break
            if match:
                original_phrase = ' '.join(tokens[i:i+len(term_words)])
                tokens[i] = f"**{original_phrase}**"
                for _ in range(len(term_words) - 1):
                    tokens.pop(i + 1)
                break
        i += 1

    # Ensuite, gérer les termes simples
    for i, token in enumerate(tokens):
        if token.startswith('**') and token.endswith('**'):
            continue
        clean_token = ''.join(c for c in token if c.isalnum()).lower()
        for term in terms:
            if ' ' not in term and clean_token == term.lower():
                tokens[i] = f"**{token}**"
                break

    return ' '.join(tokens)


class ResultRetriever:
    """Classe pour récupérer et afficher les résultats de recherche."""

    def __init__(self, index: InvertedIndex, documents: Dict[str, str]):
        """
        Initialise avec un index inversé et une collection de documents.

        Args :
            index : L'index inversé
            documents : Dictionnaire associant les identifiants de documents à leur contenu brut
        """
        self.index = index
        self.documents = documents
        self.search_engine = SearchEngine(index)

    def search(self, query: str, use_all_terms: bool = True, max_results: int = 10) -> List[Tuple[str, float]]:
        """
        Recherche les documents correspondant à la requête et retourne les résultats classés.

        Args :
            query : Chaîne de requête de recherche
            use_all_terms : Si True, les documents doivent contenir tous les termes (recherche ET)
                            Si False, les documents peuvent contenir n'importe quel terme (recherche OU)
            max_results : Nombre maximal de résultats à retourner

        Returns :
            Liste de tuples (id_doc, score) triés par score de pertinence (décroissant)
        """
        results = self.search_engine.search(query, use_all_terms)
        return results[:max_results] if max_results > 0 else results

    def get_snippet(self, doc_id: str, term: str, context_size: int = 5) -> str:
        """
        Extrait un extrait du document montrant le contexte autour d'un terme.

        Args :
            doc_id : Identifiant du document
            term : Terme à mettre en contexte
            context_size : Nombre de mots à inclure avant et après le terme

        Returns :
            Extrait montrant le terme dans son contexte
        """
        if doc_id not in self.documents:
            return ""

        contenu = self.documents[doc_id]
        terme = term.lower()
        tokens = contenu.lower().split()
        positions = []
        for i, token in enumerate(tokens):
            clean_token = ''.join(c for c in token if c.isalnum())
            if clean_token == terme:
                positions.append(i)
        if not positions:
            return ""
        pos = positions[0]
        start = max(0, pos - context_size)
        end = min(len(tokens), pos + context_size + 1)
        snippet_tokens = tokens[start:end]
        for i in range(len(snippet_tokens)):
            clean_token = ''.join(c for c in snippet_tokens[i] if c.isalnum())
            if clean_token == terme:
                snippet_tokens[i] = f"**{snippet_tokens[i]}**"
        snippet = ' '.join(snippet_tokens)
        if start > 0:
            snippet = f"...{snippet}"
        if end < len(tokens):
            snippet = f"{snippet}..."
        return snippet

    def get_multi_term_snippet(self, doc_id: str, terms: List[str], context_size: int = 5) -> str:
        """
        Extrait un extrait du document montrant le contexte autour de plusieurs termes.

        Args :
            doc_id : Identifiant du document
            terms : Liste des termes à mettre en contexte
            context_size : Nombre de mots à inclure avant et après les termes

        Returns :
            Extrait montrant les termes dans leur contexte
        """
        if not terms or doc_id not in self.documents:
            return ""
        for term in terms:
            snippet = self.get_snippet(doc_id, term, context_size)
            if snippet:
                contains_other_terms = False
                for other_term in terms:
                    if other_term != term and other_term.lower() in snippet.lower():
                        contains_other_terms = True
                        break
                if contains_other_terms or term == terms[-1]:
                    snippet = snippet.replace('**', '')
                    return highlight_all_terms(snippet, terms)
        return ""

    def display_result(self, doc_id: str, score: float, query_terms: List[str]) -> str:
        """
        Formate un résultat de recherche pour l'affichage.

        Args :
            doc_id : Identifiant du document
            score : Score de pertinence
            query_terms : Liste des termes de la requête

        Returns :
            Chaîne formatée représentant le résultat de recherche
        """
        snippet = self.get_multi_term_snippet(doc_id, query_terms)
        result = f"Document : {doc_id}\n"
        result += f"Score : {score:.2f}\n"
        if snippet:
            result += f"Extrait : {snippet}\n"
        return result

    def display_results(self, query: str, use_all_terms: bool = True, max_results: int = 10) -> str:
        """
        Recherche des documents et affiche les résultats formatés.

        Args :
            query : Chaîne de requête de recherche
            use_all_terms : Si True, recherche ET ; sinon, recherche OU
            max_results : Nombre maximal de résultats à afficher

        Returns :
            Chaîne formatée avec les résultats de recherche
        """
        query_terms = query.lower().split()
        results = self.search(query, use_all_terms, max_results)
        if not results:
            return f"Aucun résultat trouvé pour la requête : '{query}'"
        output = f"Résultats de la recherche pour la requête : '{query}'\n"
        output += f"Mode de recherche : {'ET' if use_all_terms else 'OU'}\n\n"
        for i, (doc_id, score) in enumerate(results, 1):
            output += f"Résultat {i} :\n"
            output += self.display_result(doc_id, score, query_terms)
            output += "\n"
        return output