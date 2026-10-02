"""
Génération des reçus en PDF.
Utilise fpdf2 (lite et simple).
"""

from datetime import datetime
from metiers.config import ECOLE_NOM, ECOLE_ADRESSE, DEVISE


def generer_recu_pdf(donnees_recu, chemin_sortie):
    """
    Génère un reçu PDF à partir des données du paiement.
    donnees_recu : dict avec keys (numero_recu, date_paiement, eleve_nom, eleve_prenom,
                   classe, annee_scolaire, frais_total, montant, mode_paiement, solde_apres)
    chemin_sortie : chemin où sauvegarder le PDF
    """
    try:
        from fpdf import FPDF
    except ImportError:
        print("fpdf2 n'est pas installé. Installez-le : pip install fpdf2")
        return False

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)

    # En-tête
    pdf.cell(0, 10, f"RECU DE PAIEMENT", 0, 1, "C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, ECOLE_NOM, 0, 1, "C")
    pdf.cell(0, 5, ECOLE_ADRESSE, 0, 1, "C")
    pdf.ln(5)

    # Info reçu
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 5, f"N° Reçu :")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, donnees_recu["numero_recu"], 0, 1)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 5, f"Date :")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, donnees_recu["date_paiement"], 0, 1)

    pdf.ln(5)

    # Infos élève
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "ÉLÈVE", 0, 1)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(40, 5, "Nom :")
    pdf.cell(0, 5, f"{donnees_recu['eleve_nom']} {donnees_recu['eleve_prenom']}", 0, 1)

    pdf.cell(40, 5, "Classe :")
    pdf.cell(0, 5, donnees_recu["classe"], 0, 1)

    pdf.cell(40, 5, "Année :")
    pdf.cell(0, 5, donnees_recu["annee_scolaire"], 0, 1)

    pdf.ln(5)

    # Détails paiement
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "PAIEMENT", 0, 1)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(40, 5, "Frais totaux :")
    pdf.cell(0, 5, f"{donnees_recu['frais_total']:,.0f} {DEVISE}".replace(",", " "), 0, 1)

    pdf.cell(40, 5, "Montant payé :")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, f"{donnees_recu['montant']:,.0f} {DEVISE}".replace(",", " "), 0, 1)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(40, 5, "Mode :")
    pdf.cell(0, 5, donnees_recu["mode_paiement"], 0, 1)

    pdf.ln(5)

    # Solde
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 5, "Solde restant :")
    pdf.set_font("Helvetica", "B", 11)
    couleur_solde = (10, 125, 40) if donnees_recu["solde_apres"] <= 0 else (176, 106, 0)
    pdf.set_text_color(*couleur_solde)
    pdf.cell(0, 5, f"{donnees_recu['solde_apres']:,.0f} {DEVISE}".replace(",", " "), 0, 1)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # Pied
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", 0, 1, "C")

    try:
        pdf.output(chemin_sortie)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PDF : {e}")
        return False


def ouvrir_recu_pdf(chemin):
    """Ouvre le PDF avec l'application par défaut (Windows)."""
    try:
        import os
        os.startfile(chemin)
        return True
    except:
        return False
