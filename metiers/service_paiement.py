"""
Service métier pour les paiements.
Règles clés : génération numéro reçu unique, interdiction solde négatif.
"""

from metiers.modeles import Paiement


class ErreurSoldeInsuffisant(Exception):
    """Levée quand le montant dépasse le solde."""
    pass


class ServicePaiement:
    """Gère les opérations sur les paiements."""

    def __init__(self, repository_paiement, repository_eleve):
        """Reçoit deux repositories."""
        self.repo_paiement = repository_paiement
        self.repo_eleve = repository_eleve

    # --- Solde ---
    def solde_restant(self, eleve_id: int) -> float:
        """Retourne le solde encore dû par l'élève."""
        eleve = self.repo_eleve.obtenir(eleve_id)
        if eleve is None:
            raise ValueError("Élève introuvable.")
        # solde = frais_total - total_payé
        return eleve["solde"] if "solde" in eleve.keys() else eleve["frais_total"]

    # --- Numéro de reçu ---
    def _generer_numero_recu(self, annee: str) -> str:
        """Génère le prochain numéro pour une année."""
        prefixe = f"REC-{annee}-"
        dernier = self.repo_paiement.dernier_numero(prefixe)
        if dernier:
            sequence = int(dernier.split("-")[-1]) + 1
        else:
            sequence = 1
        return f"{prefixe}{sequence:04d}"

    # --- Enregistrement ---
    def enregistrer(self, eleve_id: int, montant: float, date_paiement: str, mode_paiement: str) -> Paiement:
        """
        Enregistre un paiement avec validation metiers.
        Règle clé : montant ne doit pas faire devenir le solde négatif.
        """
        # Validations
        if montant is None or montant <= 0:
            raise ValueError("Le montant doit être strictement positif.")
        if not date_paiement:
            raise ValueError("La date est obligatoire.")

        # Règle clé : solde ne doit pas devenir négatif
        solde = self.solde_restant(eleve_id)
        if montant > solde:
            raise ErreurSoldeInsuffisant(
                f"Le montant dépasse le solde restant ({solde:.0f} FCFA). "
                "Impossible de créer un solde négatif."
            )

        # Génération du numéro de reçu
        annee = str(date_paiement)[:4]
        numero = self._generer_numero_recu(annee)

        # Création
        paiement = Paiement(
            eleve_id=eleve_id, montant=montant,
            date_paiement=date_paiement, mode_paiement=mode_paiement,
            numero_recu=numero,
        )
        paiement.id = self.repo_paiement.creer(paiement)
        return paiement

    # --- Lecture ---
    def lister_par_eleve(self, eleve_id: int):
        """Historique des paiements d'un élève."""
        return self.repo_paiement.lister_par_eleve(eleve_id)

    def obtenir(self, paiement_id: int):
        """Récupère un paiement."""
        return self.repo_paiement.obtenir(paiement_id)

    def donnees_recu(self, paiement_row) -> dict:
        """Rassemble les infos pour imprimer/afficher un reçu."""
        eleve = self.repo_eleve.obtenir(paiement_row["eleve_id"])
        cumul = self.repo_paiement.cumul_jusqua(paiement_row["eleve_id"], paiement_row["id"])
        solde_apres = eleve["frais_total"] - cumul
        return {
            "numero_recu": paiement_row["numero_recu"],
            "date_paiement": paiement_row["date_paiement"],
            "eleve_nom": eleve["nom"],
            "eleve_prenom": eleve["prenom"],
            "classe": eleve["classe"],
            "annee_scolaire": eleve["annee_scolaire"],
            "frais_total": eleve["frais_total"],
            "montant": paiement_row["montant"],
            "mode_paiement": paiement_row["mode_paiement"],
            "solde_apres": solde_apres,
        }
