-- ============================================================
--  EduPaie — Script de création de la base de données
--  Moteur : SQLite 3
-- ============================================================

-- Activer les clés étrangères (désactivées par défaut dans SQLite)
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
--  Table : eleves
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS eleves (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT    NOT NULL,
    prenom          TEXT    NOT NULL,
    classe          TEXT    NOT NULL,
    annee_scolaire  TEXT    NOT NULL,
    frais_total     REAL    NOT NULL CHECK (frais_total >= 0),
    date_creation   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
--  Table : paiements
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paiements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eleve_id        INTEGER NOT NULL,
    numero_recu     TEXT    NOT NULL UNIQUE,
    montant         REAL    NOT NULL CHECK (montant > 0),
    date_paiement   TEXT    NOT NULL,
    mode_paiement   TEXT    NOT NULL,
    date_creation   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (eleve_id) REFERENCES eleves(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
--  Index pour accélérer les recherches
-- ------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_paiements_eleve ON paiements(eleve_id);
CREATE INDEX IF NOT EXISTS idx_eleves_classe   ON eleves(classe);

-- ------------------------------------------------------------
--  Vue : solde et statut par élève
--  solde  = frais_total - somme des paiements
--  statut = Soldé / Non payé / Partiellement payé
-- ------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_eleves_solde AS
SELECT
    e.id,
    e.nom,
    e.prenom,
    e.classe,
    e.annee_scolaire,
    e.frais_total,
    COALESCE(SUM(p.montant), 0)                 AS total_paye,
    e.frais_total - COALESCE(SUM(p.montant), 0) AS solde,
    CASE
        WHEN COALESCE(SUM(p.montant), 0) >= e.frais_total THEN 'Soldé'
        WHEN COALESCE(SUM(p.montant), 0) = 0              THEN 'Non payé'
        ELSE 'Partiellement payé'
    END                                         AS statut
FROM eleves e
LEFT JOIN paiements p ON p.eleve_id = e.id
GROUP BY e.id;
