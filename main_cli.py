#!/usr/bin/env python
"""
Interface CLI simple pour TextIndexerPy.

Ce module fournit une interface en ligne de commande interactive pour l'application TextIndexerPy,
permettant de charger des documents, de rechercher des termes et de consulter des statistiques.
"""

import sys

import document_loader
from indexer import InvertedIndex
from retrieval import ResultRetriever
from stats import Statistics


def main():
    """Fonction principale de l'interface CLI simple."""
    print("TextIndexerPy : Un outil simple d'indexation et de recherche de texte")
    print("---------------------------------------------------------------------")

    # Demander le répertoire contenant les documents
    directory = input("Entrez le chemin du dossier contenant les fichiers texte à indexer : ")

    # Charger les documents
    try:
        print(f"Chargement des documents depuis {directory}...")
        documents = document_loader.load_documents(directory)

        if not documents:
            print("Aucun fichier texte trouvé dans le dossier spécifié.")
            return 1

        print(f"{len(documents)} documents chargés.")
    except Exception as e:
        print(f"Erreur lors du chargement des documents : {e}")
        return 1

    # Construire l'index
    try:
        print("Construction de l'index inversé...")
        index = InvertedIndex()
        index.build_index(documents)
        print("Index construit avec succès.")
    except Exception as e:
        print(f"Erreur lors de la construction de l'index : {e}")
        return 1

    # Créer les objets statistiques et récupération
    stats = Statistics(index, documents)
    retriever = ResultRetriever(index, documents)

    # Afficher les statistiques générales après chargement
    print("\nDocuments chargés et indexés avec succès.")
    print(stats.display_general_stats())

    # Boucle principale d'interaction
    while True:
        print("\nQue souhaitez-vous faire ?")
        print("1. Rechercher des termes")
        print("2. Voir les statistiques générales")
        print("3. Voir les statistiques d'un document")
        print("4. Quitter")

        choice = input("Entrez votre choix (1-4) : ")

        if choice == '1':
            # Fonctionnalité de recherche
            query = input("Entrez votre requête de recherche : ")

            search_logic = input("Utiliser la logique OU pour la recherche ? (o/n, défaut : ET) : ").lower()
            use_all_terms = search_logic != 'o'
            search_mode = "OU" if not use_all_terms else "ET"

            max_results = input("Nombre maximal de résultats à afficher (défaut : 10) : ")
            max_results = int(max_results) if max_results.isdigit() else 10

            print(f"\nRecherche de '{query}' en mode {search_mode}...")
            results = retriever.display_results(query, use_all_terms, max_results)
            print(results)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '2':
            # Statistiques générales
            print("\n" + stats.display_general_stats())
            print(stats.display_most_frequent_words(10))
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '3':
            # Statistiques d'un document
            doc_name = input("Entrez le nom du document : ")
            print("\n" + stats.display_document_stats(doc_name))
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '4':
            # Quitter
            print("Merci d'avoir utilisé TextIndexerPy !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

    return 0


if __name__ == "__main__":
    sys.exit(main())