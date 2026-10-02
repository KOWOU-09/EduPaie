"""
Configuration et constantes de l'application.
"""

# École
ECOLE_NOM = "Établissement Scolaire"
ECOLE_ADRESSE = "Lomé, Togo"
DEVISE = "FCFA"

# Modes de paiement autorisés
MODES_PAIEMENT = ["Espèces", "Chèque", "Virement", "Mobile Money"]


def formater_montant(montant: float) -> str:
    """Formater un montant pour l'affichage."""
    try:
        return f"{montant:,.0f}".replace(",", " ") + f" {DEVISE}"
    except (ValueError, TypeError):
        return f"0 {DEVISE}"
