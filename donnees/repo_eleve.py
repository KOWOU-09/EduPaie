"""
Repository des élèves (DAO).
Contient TOUT le SQL des élèves.
"""

from metiers.modeles import Eleve


class RepositoryEleve:
    def __init__(self, base):
        self.base = base

    # --- ÉCRITURE ---
    def creer(self, eleve: Eleve) -> int:
        """Crée un élève. Retourne son id."""
        sql = """
            INSERT INTO eleves (nom, prenom, classe, annee_scolaire, frais_total)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.base.connexion() as con:
            curseur = con.execute(sql, (
                eleve.nom, eleve.prenom, eleve.classe,
                eleve.annee_scolaire, eleve.frais_total,
            ))
            return curseur.lastrowid

    def modifier(self, eleve: Eleve) -> None:
        """Modifie un élève."""
        sql = """
            UPDATE eleves
            SET nom = ?, prenom = ?, classe = ?, annee_scolaire = ?, frais_total = ?
            WHERE id = ?
        """
        with self.base.connexion() as con:
            con.execute(sql, (
                eleve.nom, eleve.prenom, eleve.classe,
                eleve.annee_scolaire, eleve.frais_total, eleve.id,
            ))

    def supprimer(self, eleve_id: int) -> None:
        """Supprime un élève (et ses paiements via ON DELETE CASCADE)."""
        with self.base.connexion() as con:
            con.execute("DELETE FROM eleves WHERE id = ?", (eleve_id,))

    # --- LECTURE ---
    def obtenir(self, eleve_id: int):
        """Récupère un élève avec son solde/statut."""
        with self.base.connexion() as con:
            return con.execute(
                "SELECT * FROM v_eleves_solde WHERE id = ?", (eleve_id,)
            ).fetchone()

    def lister(self, recherche="", classe=None, statut=None):
        """Liste les élèves avec filtres."""
        sql = "SELECT * FROM v_eleves_solde WHERE 1 = 1"
        params = []

        if recherche:
            sql += " AND (nom LIKE ? OR prenom LIKE ?)"
            motif = f"%{recherche}%"
            params += [motif, motif]

        if classe:
            sql += " AND classe = ?"
            params.append(classe)

        if statut:
            sql += " AND statut = ?"
            params.append(statut)

        sql += " ORDER BY nom, prenom"

        with self.base.connexion() as con:
            return con.execute(sql, params).fetchall()

    def classes(self):
        """Liste les classes distinctes."""
        with self.base.connexion() as con:
            lignes = con.execute(
                "SELECT DISTINCT classe FROM eleves ORDER BY classe"
            ).fetchall()
            return [ligne["classe"] for ligne in lignes]

    def statistiques(self):
        """Stats du tableau de bord."""
        sql = """
            SELECT
                COUNT(*) AS nb_eleves,
                COALESCE(SUM(total_paye), 0) AS total_encaisse,
                COALESCE(SUM(CASE WHEN solde > 0 THEN solde ELSE 0 END), 0) AS total_restant,
                COALESCE(SUM(CASE WHEN statut <> 'Soldé' THEN 1 ELSE 0 END), 0) AS nb_non_soldes
            FROM v_eleves_solde
        """
        with self.base.connexion() as con:
            return con.execute(sql).fetchone()
