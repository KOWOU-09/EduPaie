"""
Service métier pour les élèves.
Contient les règles de validation et les opérations.
"""

from metiers.modeles import Eleve


class ServiceEleve:
    """Gère les opérations sur les élèves."""

    def __init__(self, repository):
        """Reçoit un repository (qui fera le SQL)."""
        self.repo = repository

    def _valider(self, eleve: Eleve):
        """Vérifie que les champs sont valides."""
        if not eleve.nom or not eleve.nom.strip():
            raise ValueError("Le nom est obligatoire.")
        if not eleve.prenom or not eleve.prenom.strip():
            raise ValueError("Le prénom est obligatoire.")
        if not eleve.classe or not eleve.classe.strip():
            raise ValueError("La classe est obligatoire.")
        if not eleve.annee_scolaire or not eleve.annee_scolaire.strip():
            raise ValueError("L'année scolaire est obligatoire.")
        if eleve.frais_total is None or eleve.frais_total < 0:
            raise ValueError("Les frais doivent être positifs.")

    def creer(self, eleve: Eleve) -> int:
        """Crée un élève. Retourne son id."""
        self._valider(eleve)
        return self.repo.creer(eleve)

    def modifier(self, eleve: Eleve) -> None:
        """Modifie un élève."""
        if not eleve.id:
            raise ValueError("Impossible de modifier sans id.")
        self._valider(eleve)
        self.repo.modifier(eleve)

    def supprimer(self, eleve_id: int) -> None:
        """Supprime un élève."""
        self.repo.supprimer(eleve_id)

    def obtenir(self, eleve_id: int):
        """Récupère un élève."""
        return self.repo.obtenir(eleve_id)

    def lister(self, recherche="", classe=None, statut=None):
        """Liste les élèves, avec filtres optionnels."""
        return self.repo.lister(recherche, classe, statut)

    def classes(self):
        """Retourne la liste des classes."""
        return self.repo.classes()

    def statistiques(self):
        """Retourne les stats du tableau de bord."""
        return self.repo.statistiques()
