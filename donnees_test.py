"""
Script de données de test.
Crée une base avec ~16 élèves et des paiements variés.
Lancer : python donnees_test.py
"""

import os
from donnees.base import BaseDonnees
from donnees.repo_eleve import RepositoryEleve
from donnees.repo_paiement import RepositoryPaiement
from metiers.service_eleve import ServiceEleve
from metiers.service_paiement import ServicePaiement
from metiers.modeles import Eleve

DONNEES = [
    # (nom, prenom, classe, frais, [(montant, date, mode), ...])
    # Lycée seulement (TL, 1ère, 2nde)
    # Tous les frais : 80 000 FCFA
    # Certains paient tout, certains partiellement, certains rien
    ("Kodjo", "Ama", "2nde", 80000, [(80000, "2024-10-05", "Especes")]),  # Soldé
    ("Mensah", "Kofi", "2nde", 80000, [(80000, "2024-09-20", "Virement")]),  # Soldé
    ("Agbeko", "Eyram", "1ère", 80000, [(15000, "2024-10-01", "Especes")]),  # Partiel
    ("Sossou", "Afi", "TL", 80000, [(80000, "2024-09-15", "Virement")]),  # Soldé
    ("Adjovi", "Sena", "1ère", 80000, [(25000, "2024-10-10", "Mobile Money")]),  # Partiel
    ("Tetteh", "Yao", "TL", 80000, []),  # Non payé
    ("Amoussou", "Delali", "2nde", 80000, []),  # Non payé
    ("Lawson", "Koffi", "1ère", 80000, [(80000, "2024-11-01", "Mobile Money")]),  # Soldé
    ("Bruce", "Enam", "TL", 80000, []),  # Non payé
    ("Akakpo", "Mawuli", "2nde", 80000, [(35000, "2025-01-05", "Especes")]),  # Partiel
    ("Dossou", "Akossiwa", "1ère", 80000, []),  # Non payé
    ("Fiawoo", "Elom", "TL", 80000, [(80000, "2024-12-10", "Cheque")]),  # Soldé
    ("Kponton", "Nathan", "2nde", 80000, []),  # Non payé
    ("Zinsou", "Ayaba", "1ère", 80000, [(40000, "2024-11-20", "Virement")]),  # Partiel
    ("Gbegnon", "Selom", "TL", 80000, []),  # Non payé
    ("Houngbo", "Komi", "2nde", 80000, [(80000, "2025-01-15", "Especes")]),  # Soldé
]

def main():
    # Vider les tables existantes
    base = BaseDonnees()

    with base.connexion() as con:
        con.execute("DELETE FROM paiements")
        con.execute("DELETE FROM eleves")
    service_eleve = ServiceEleve(RepositoryEleve(base))
    service_paiement = ServicePaiement(RepositoryPaiement(base), RepositoryEleve(base))

    # Remplir
    for nom, prenom, classe, frais, paiements_data in DONNEES:
        eid = service_eleve.creer(Eleve(nom, prenom, classe, "2024-2025", frais))
        for montant, date, mode in paiements_data:
            service_paiement.enregistrer(eid, montant, date, mode)

    # Stats
    stats = service_eleve.statistiques()
    print(f"Base de test creee")
    print(f"  Eleves      : {stats['nb_eleves']}")
    print(f"  Encaisse    : {stats['total_encaisse']:.0f}")
    print(f"  Restant     : {stats['total_restant']:.0f}")
    print(f"  Non soldes  : {stats['nb_non_soldes']}")

if __name__ == "__main__":
    main()
