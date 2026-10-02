"""
Couche données — Connexion à SQLite.
Seul fichier qui touche à la base.
"""

import sqlite3
import sys
import os


def chemin_ressource(relatif):
    """Trouve un fichier inclus dans l'app (ex: sql/schema.sql).
    - En .exe (PyInstaller) : les fichiers sont dans sys._MEIPASS
    - En développement      : dans le dossier du projet
    """
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, relatif)
    return relatif


def chemin_base_defaut():
    """Où ranger le fichier .db (dossier accessible en écriture).
    - En .exe : à côté de l'exécutable
    - En dev  : dans ressources/
    """
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "edupaie.db")
    return "ressources/edupaie.db"


class BaseDonnees:
    """Gère la connexion SQLite."""

    def __init__(self, chemin=None):
        self.chemin = chemin or chemin_base_defaut()
        self.initialiser_schema()

    def connexion(self):
        """Ouvre une connexion bien configurée."""
        con = sqlite3.connect(self.chemin)
        con.row_factory = sqlite3.Row  # lire par nom
        con.execute("PRAGMA foreign_keys = ON")  # activer les clés étrangères
        return con

    def initialiser_schema(self):
        """Crée les tables au premier lancement, à partir de sql/schema.sql."""
        with open(chemin_ressource("sql/schema.sql"), encoding="utf-8") as fichier:
            schema = fichier.read()
        with self.connexion() as con:
            con.executescript(schema)


