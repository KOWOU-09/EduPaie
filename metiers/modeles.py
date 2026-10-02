"""
Modèles de données (objets métier).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Eleve:
    """Un élève et ses infos."""
    nom: str
    prenom: str
    classe: str
    annee_scolaire: str
    frais_total: float
    id: Optional[int] = None


@dataclass
class Paiement:
    """Un versement effectué par un élève."""
    eleve_id: int
    montant: float
    date_paiement: str  # "YYYY-MM-DD"
    mode_paiement: str  # "Espèces", "Chèque", "Virement", "Mobile Money"
    numero_recu: Optional[str] = None  # ex: "REC-2025-0001"
    id: Optional[int] = None
