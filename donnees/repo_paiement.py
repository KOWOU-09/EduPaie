"""
Repository des paiements (DAO).
Contient TOUT le SQL des paiements.
"""

from metiers.modeles import Paiement


class RepositoryPaiement:
    def __init__(self, base):
        self.base = base

    # --- ÉCRITURE ---
    def creer(self, paiement: Paiement) -> int:
        """Crée un paiement. Retourne son id."""
        sql = """
            INSERT INTO paiements (eleve_id, numero_recu, montant, date_paiement, mode_paiement)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.base.connexion() as con:
            curseur = con.execute(sql, (
                paiement.eleve_id, paiement.numero_recu, paiement.montant,
                paiement.date_paiement, paiement.mode_paiement,
            ))
            return curseur.lastrowid

    # --- LECTURE ---
    def lister_par_eleve(self, eleve_id: int):
        """Historique des paiements d'un élève."""
        sql = """
            SELECT * FROM paiements
            WHERE eleve_id = ?
            ORDER BY date_paiement, id
        """
        with self.base.connexion() as con:
            return con.execute(sql, (eleve_id,)).fetchall()

    def obtenir(self, paiement_id: int):
        """Récupère un paiement."""
        with self.base.connexion() as con:
            return con.execute(
                "SELECT * FROM paiements WHERE id = ?", (paiement_id,)
            ).fetchone()

    def total_paye(self, eleve_id: int) -> float:
        """Somme totale des paiements d'un élève."""
        sql = "SELECT COALESCE(SUM(montant), 0) AS total FROM paiements WHERE eleve_id = ?"
        with self.base.connexion() as con:
            return con.execute(sql, (eleve_id,)).fetchone()["total"]

    def cumul_jusqua(self, eleve_id: int, paiement_id: int) -> float:
        """Somme cumulée jusqu'à un paiement (pour reçu réimprimable)."""
        sql = """
            SELECT COALESCE(SUM(montant), 0) AS cumul
            FROM paiements
            WHERE eleve_id = ? AND id <= ?
        """
        with self.base.connexion() as con:
            return con.execute(sql, (eleve_id, paiement_id)).fetchone()["cumul"]

    def dernier_numero(self, prefixe: str):
        """Retourne le dernier numéro de reçu pour un prefixe."""
        sql = """
            SELECT numero_recu FROM paiements
            WHERE numero_recu LIKE ?
            ORDER BY numero_recu DESC
            LIMIT 1
        """
        with self.base.connexion() as con:
            ligne = con.execute(sql, (prefixe + "%",)).fetchone()
            return ligne["numero_recu"] if ligne else None
