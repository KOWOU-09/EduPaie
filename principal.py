"""
EduPaie — Gestion des paiements scolaires
Interface graphique complète, stylée (QSS) et branchée aux services.
"""

import sys
from PySide6 import QtWidgets, QtCore, QtGui, QtSvg

from donnees.base import BaseDonnees
from donnees.repo_eleve import RepositoryEleve
from donnees.repo_paiement import RepositoryPaiement
from metiers.service_eleve import ServiceEleve
from metiers.service_paiement import ServicePaiement
from metiers.modeles import Eleve
from metiers.config import formater_montant

# Couleurs des statuts
COULEURS = {
    "Soldé": "#0a7d28",
    "Partiellement payé": "#b26a00",
    "Non payé": "#b00020",
}

# ----------------------------------------------------------------------------
#  Icônes Material (Google) dessinées en SVG — marchent même dans l'exe
# ----------------------------------------------------------------------------
ICONES_SVG = {
    "dashboard": '<path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>',
    "eleves": '<path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>',
    "fiche": '<path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>',
}


def icone(nom, couleur="#e2e8f0", taille=22):
    """Construit une QIcon à partir d'une icône Material SVG."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
           f'fill="{couleur}">{ICONES_SVG[nom]}</svg>')
    rendu = QtSvg.QSvgRenderer(QtCore.QByteArray(svg.encode("utf-8")))
    pixmap = QtGui.QPixmap(taille, taille)
    pixmap.fill(QtCore.Qt.transparent)
    peintre = QtGui.QPainter(pixmap)
    rendu.render(peintre)
    peintre.end()
    return QtGui.QIcon(pixmap)


# ----------------------------------------------------------------------------
#  Feuille de style (QSS) — le "CSS" de l'application
# ----------------------------------------------------------------------------
STYLE = """
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #1e293b;
}
QStackedWidget, QMainWindow { background: #f1f5f9; }
QStackedWidget > QWidget { background: #f1f5f9; }

/* ---- Barre latérale ---- */
QListWidget#sidebar {
    background: #1e293b;
    border: none;
    outline: 0;
    padding-top: 12px;
}
QListWidget#sidebar::item {
    color: #cbd5e1;
    padding: 14px 18px;
    margin: 4px 10px;
    border-radius: 8px;
}
QListWidget#sidebar::item:selected { background: #2563eb; color: white; }
QListWidget#sidebar::item:hover:!selected { background: #334155; }

/* ---- Titres de page ---- */
QLabel#titrePage {
    font-size: 22px;
    font-weight: bold;
    color: #0f172a;
    padding: 6px 0 10px 0;
}
QLabel#sousTitre { font-size: 14px; font-weight: 600; color: #334155; padding-top: 6px; }

/* ---- Cartes du tableau de bord ---- */
QFrame#carte {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
QLabel#carteTitre { color: #64748b; font-size: 12px; border: none; }
QLabel#carteValeur { color: #2563eb; font-size: 22px; font-weight: bold; border: none; }

/* ---- Boutons ---- */
QPushButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    font-weight: 600;
}
QPushButton:hover { background: #1d4ed8; }
QPushButton:pressed { background: #1e40af; }
QPushButton#btnDanger { background: #dc2626; }
QPushButton#btnDanger:hover { background: #b91c1c; }

/* ---- Champs de saisie ---- */
QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 7px 10px;
    background: white;
    selection-background-color: #2563eb;
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
    border: 1px solid #2563eb;
}

/* ---- Tableaux ---- */
QTableWidget {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    gridline-color: #f1f5f9;
    selection-background-color: #dbeafe;
    selection-color: #0f172a;
}
QTableWidget::item { padding: 6px; }
QHeaderView::section {
    background: #f8fafc;
    color: #475569;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-weight: 600;
}
QTableCornerButton::section { background: #f8fafc; border: none; }
"""


# ============================================================================
#  PAGE 1 : Tableau de bord
# ============================================================================
class TableauDeBord(QtWidgets.QWidget):
    def __init__(self, service_eleve):
        super().__init__()
        self.service_eleve = service_eleve
        self.init_ui()
        self.rafraichir()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(14)

        titre = QtWidgets.QLabel("Tableau de bord")
        titre.setObjectName("titrePage")
        layout.addWidget(titre)

        cartes = QtWidgets.QHBoxLayout()
        cartes.setSpacing(14)
        self.lbl_nb = QtWidgets.QLabel("0")
        self.lbl_encaisse = QtWidgets.QLabel("0 FCFA")
        self.lbl_restant = QtWidgets.QLabel("0 FCFA")
        self.lbl_non_solde = QtWidgets.QLabel("0")

        for lbl, titre_carte in [
            (self.lbl_nb, "Élèves"),
            (self.lbl_encaisse, "Encaissé"),
            (self.lbl_restant, "Restant"),
            (self.lbl_non_solde, "Non soldés"),
        ]:
            carte = QtWidgets.QFrame()
            carte.setObjectName("carte")
            lay = QtWidgets.QVBoxLayout(carte)
            lay.setContentsMargins(16, 14, 16, 14)
            t = QtWidgets.QLabel(titre_carte)
            t.setObjectName("carteTitre")
            lbl.setObjectName("carteValeur")
            lay.addWidget(t)
            lay.addWidget(lbl)
            cartes.addWidget(carte)
        layout.addLayout(cartes)

        filtre_layout = QtWidgets.QHBoxLayout()
        filtre_layout.addWidget(QtWidgets.QLabel("Filtrer par statut :"))
        self.filtre_statut = QtWidgets.QComboBox()
        self.filtre_statut.addItems(["Tous", "Soldé", "Partiellement payé", "Non payé"])
        self.filtre_statut.currentTextChanged.connect(self.rafraichir_tableau)
        filtre_layout.addWidget(self.filtre_statut)
        filtre_layout.addStretch()
        layout.addLayout(filtre_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nom", "Classe", "Solde", "Statut"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def rafraichir(self):
        s = self.service_eleve.statistiques()
        self.lbl_nb.setText(str(s["nb_eleves"]))
        self.lbl_encaisse.setText(formater_montant(s["total_encaisse"]))
        self.lbl_restant.setText(formater_montant(s["total_restant"]))
        self.lbl_non_solde.setText(str(s["nb_non_soldes"]))
        self.rafraichir_tableau()

    def rafraichir_tableau(self):
        statut = self.filtre_statut.currentText()
        statut = None if statut == "Tous" else statut
        eleves = self.service_eleve.lister(statut=statut) if statut else self.service_eleve.lister()

        self.table.setRowCount(0)
        for e in eleves:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(e["nom"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(e["classe"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(formater_montant(e["solde"])))

            item_statut = QtWidgets.QTableWidgetItem(e["statut"])
            couleur = COULEURS.get(e["statut"])
            if couleur:
                item_statut.setForeground(QtGui.QColor(couleur))
            self.table.setItem(row, 3, item_statut)


# ============================================================================
#  PAGE 2 : Élèves
# ============================================================================
class PageEleves(QtWidgets.QWidget):
    def __init__(self, service_eleve):
        super().__init__()
        self.service_eleve = service_eleve
        self.init_ui()
        self.rafraichir_liste()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(12)

        titre = QtWidgets.QLabel("Élèves")
        titre.setObjectName("titrePage")
        layout.addWidget(titre)

        barre = QtWidgets.QHBoxLayout()
        self.recherche = QtWidgets.QLineEdit()
        self.recherche.setPlaceholderText("Rechercher par nom ou prénom…")
        self.recherche.textChanged.connect(self.rafraichir_liste)
        barre.addWidget(self.recherche, 2)

        barre.addWidget(QtWidgets.QLabel("Classe :"))
        self.filtre_classe = QtWidgets.QComboBox()
        self.filtre_classe.addItem("Toutes")
        for classe in self.service_eleve.classes():
            self.filtre_classe.addItem(classe)
        self.filtre_classe.currentTextChanged.connect(self.rafraichir_liste)
        barre.addWidget(self.filtre_classe, 1)
        layout.addLayout(barre)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prénom", "Classe", "Année", "Frais", "Payé", "Solde", "Statut"])
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, 1)

        boutons_layout = QtWidgets.QHBoxLayout()
        self.btn_ajouter = QtWidgets.QPushButton("Ajouter")
        self.btn_modifier = QtWidgets.QPushButton("Modifier")
        self.btn_supprimer = QtWidgets.QPushButton("Supprimer")
        self.btn_supprimer.setObjectName("btnDanger")
        self.btn_paiement = QtWidgets.QPushButton("Enregistrer paiement")
        self.btn_fiche = QtWidgets.QPushButton("Fiche détail")

        for btn in [self.btn_ajouter, self.btn_modifier, self.btn_supprimer,
                    self.btn_paiement, self.btn_fiche]:
            boutons_layout.addWidget(btn)
        layout.addLayout(boutons_layout)

    def rafraichir_liste(self):
        recherche = self.recherche.text().strip()
        classe = self.filtre_classe.currentText()
        classe = None if classe == "Toutes" else classe

        eleves = self.service_eleve.lister(recherche=recherche, classe=classe)

        self.table.setRowCount(0)
        for e in eleves:
            row = self.table.rowCount()
            self.table.insertRow(row)

            items = [
                str(e["id"]),
                e["nom"],
                e["prenom"],
                e["classe"],
                e["annee_scolaire"],
                formater_montant(e["frais_total"]),
                formater_montant(e["total_paye"]),
                formater_montant(e["solde"]),
                e["statut"],
            ]

            for col, text in enumerate(items):
                item = QtWidgets.QTableWidgetItem(text)
                if col == 8:
                    couleur = COULEURS.get(e["statut"])
                    if couleur:
                        item.setForeground(QtGui.QColor(couleur))
                self.table.setItem(row, col, item)

    def eleve_selectionne(self):
        rows = self.table.selectedIndexes()
        if rows:
            return int(self.table.item(rows[0].row(), 0).text())
        return None


# ============================================================================
#  PAGE 3 : Fiche élève
# ============================================================================
class FicheEleve(QtWidgets.QWidget):
    def __init__(self, service_eleve, service_paiement):
        super().__init__()
        self.service_eleve = service_eleve
        self.service_paiement = service_paiement
        self.eleve_id = None
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(12)

        titre = QtWidgets.QLabel("Fiche élève")
        titre.setObjectName("titrePage")
        layout.addWidget(titre)

        self.lbl_nom = QtWidgets.QLabel("—")
        self.lbl_classe = QtWidgets.QLabel("—")
        self.lbl_frais = QtWidgets.QLabel("—")
        self.lbl_paye = QtWidgets.QLabel("—")
        self.lbl_solde = QtWidgets.QLabel("—")
        self.lbl_statut = QtWidgets.QLabel("—")

        carte_infos = QtWidgets.QFrame()
        carte_infos.setObjectName("carte")
        infos = QtWidgets.QGridLayout(carte_infos)
        infos.setContentsMargins(16, 14, 16, 14)
        infos.addWidget(QtWidgets.QLabel("Nom :"), 0, 0)
        infos.addWidget(self.lbl_nom, 0, 1)
        infos.addWidget(QtWidgets.QLabel("Classe :"), 0, 2)
        infos.addWidget(self.lbl_classe, 0, 3)
        infos.addWidget(QtWidgets.QLabel("Frais totaux :"), 1, 0)
        infos.addWidget(self.lbl_frais, 1, 1)
        infos.addWidget(QtWidgets.QLabel("Payé :"), 1, 2)
        infos.addWidget(self.lbl_paye, 1, 3)
        infos.addWidget(QtWidgets.QLabel("Solde :"), 2, 0)
        infos.addWidget(self.lbl_solde, 2, 1)
        infos.addWidget(QtWidgets.QLabel("Statut :"), 2, 2)
        infos.addWidget(self.lbl_statut, 2, 3)
        layout.addWidget(carte_infos)

        sous_titre = QtWidgets.QLabel("Historique des paiements")
        sous_titre.setObjectName("sousTitre")
        layout.addWidget(sous_titre)

        self.table_historique = QtWidgets.QTableWidget()
        self.table_historique.setColumnCount(5)
        self.table_historique.setHorizontalHeaderLabels(
            ["Numéro reçu", "Date", "Montant", "Mode", "Solde après"])
        self.table_historique.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_historique.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_historique.verticalHeader().setVisible(False)
        self.table_historique.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_historique, 1)

        self.btn_recu = QtWidgets.QPushButton("Réimprimer le reçu")
        layout.addWidget(self.btn_recu, alignment=QtCore.Qt.AlignLeft)

    def afficher_eleve(self, eleve_id):
        self.eleve_id = eleve_id
        eleve = self.service_eleve.obtenir(eleve_id)

        self.lbl_nom.setText(f"{eleve['nom']} {eleve['prenom']}")
        self.lbl_classe.setText(eleve['classe'])
        self.lbl_frais.setText(formater_montant(eleve['frais_total']))
        self.lbl_paye.setText(formater_montant(eleve['total_paye']))
        self.lbl_solde.setText(formater_montant(eleve['solde']))
        self.lbl_statut.setText(eleve['statut'])

        paiements = self.service_paiement.lister_par_eleve(eleve_id)
        self.table_historique.setRowCount(0)
        for p in paiements:
            row = self.table_historique.rowCount()
            self.table_historique.insertRow(row)

            cumul = self.service_paiement.repo_paiement.cumul_jusqua(eleve_id, p['id'])
            solde_apres = eleve['frais_total'] - cumul

            self.table_historique.setItem(row, 0, QtWidgets.QTableWidgetItem(p['numero_recu']))
            self.table_historique.setItem(row, 1, QtWidgets.QTableWidgetItem(p['date_paiement']))
            self.table_historique.setItem(row, 2, QtWidgets.QTableWidgetItem(formater_montant(p['montant'])))
            self.table_historique.setItem(row, 3, QtWidgets.QTableWidgetItem(p['mode_paiement']))
            self.table_historique.setItem(row, 4, QtWidgets.QTableWidgetItem(formater_montant(solde_apres)))


# ============================================================================
#  DIALOGUES
# ============================================================================
class DialogueAjoutEleve(QtWidgets.QDialog):
    def __init__(self, parent=None, eleve_data=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        self.setWindowTitle("Modifier un élève" if eleve_data else "Ajouter un élève")

        layout = QtWidgets.QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.nom = QtWidgets.QLineEdit()
        self.prenom = QtWidgets.QLineEdit()
        self.classe = QtWidgets.QLineEdit()
        self.annee = QtWidgets.QLineEdit()
        self.annee.setText("2024-2025")
        self.frais = QtWidgets.QDoubleSpinBox()
        self.frais.setMaximum(10000000)

        if eleve_data:
            self.nom.setText(eleve_data["nom"])
            self.prenom.setText(eleve_data["prenom"])
            self.classe.setText(eleve_data["classe"])
            self.annee.setText(eleve_data["annee_scolaire"])
            self.frais.setValue(eleve_data["frais_total"])

        layout.addRow("Nom :", self.nom)
        layout.addRow("Prénom :", self.prenom)
        layout.addRow("Classe :", self.classe)
        layout.addRow("Année scolaire :", self.annee)
        layout.addRow("Frais (FCFA) :", self.frais)

        boutons = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton("OK")
        annuler = QtWidgets.QPushButton("Annuler")
        annuler.setObjectName("btnDanger")
        ok.clicked.connect(self.accept)
        annuler.clicked.connect(self.reject)
        boutons.addStretch()
        boutons.addWidget(annuler)
        boutons.addWidget(ok)
        layout.addRow(boutons)


class DialoguePaiement(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enregistrer un paiement")
        self.setMinimumWidth(400)

        layout = QtWidgets.QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.montant = QtWidgets.QDoubleSpinBox()
        self.montant.setMaximum(10000000)

        self.date = QtWidgets.QDateEdit()
        self.date.setDate(QtCore.QDate.currentDate())
        self.date.setCalendarPopup(True)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItems(["Especes", "Cheque", "Virement", "Mobile Money"])

        layout.addRow("Montant (FCFA) :", self.montant)
        layout.addRow("Date :", self.date)
        layout.addRow("Mode de paiement :", self.mode)

        boutons = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton("Enregistrer")
        annuler = QtWidgets.QPushButton("Annuler")
        annuler.setObjectName("btnDanger")
        ok.clicked.connect(self.accept)
        annuler.clicked.connect(self.reject)
        boutons.addStretch()
        boutons.addWidget(annuler)
        boutons.addWidget(ok)
        layout.addRow(boutons)


# ============================================================================
#  FENÊTRE PRINCIPALE
# ============================================================================
class FenetrePrincipale(QtWidgets.QMainWindow):
    def __init__(self, service_eleve, service_paiement):
        super().__init__()
        self.service_eleve = service_eleve
        self.service_paiement = service_paiement

        self.setWindowTitle("EduPaie — Gestion des paiements scolaires")
        self.resize(1200, 700)
        self.init_ui()

    def init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.menu = QtWidgets.QListWidget()
        self.menu.setObjectName("sidebar")
        self.menu.setFixedWidth(210)
        self.menu.setIconSize(QtCore.QSize(22, 22))
        self.menu.addItem(QtWidgets.QListWidgetItem(icone("dashboard"), "Tableau de bord"))
        self.menu.addItem(QtWidgets.QListWidgetItem(icone("eleves"), "Élèves"))
        self.menu.addItem(QtWidgets.QListWidgetItem(icone("fiche"), "Fiche élève"))
        self.menu.setCurrentRow(0)
        layout.addWidget(self.menu)

        self.pages = QtWidgets.QStackedWidget()
        layout.addWidget(self.pages, 1)

        self.page_dashboard = TableauDeBord(self.service_eleve)
        self.page_eleves = PageEleves(self.service_eleve)
        self.page_fiche = FicheEleve(self.service_eleve, self.service_paiement)

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_eleves)
        self.pages.addWidget(self.page_fiche)

        self.menu.currentRowChanged.connect(self.pages.setCurrentIndex)

        # Connexions
        self.page_eleves.btn_ajouter.clicked.connect(self.ajouter_eleve)
        self.page_eleves.btn_modifier.clicked.connect(self.modifier_eleve)
        self.page_eleves.btn_supprimer.clicked.connect(self.supprimer_eleve)
        self.page_eleves.btn_paiement.clicked.connect(self.enregistrer_paiement)
        self.page_eleves.btn_fiche.clicked.connect(self.afficher_fiche)
        self.page_fiche.btn_recu.clicked.connect(self.reimprimer_recu)

    def ajouter_eleve(self):
        dialog = DialogueAjoutEleve(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                e = Eleve(
                    dialog.nom.text(),
                    dialog.prenom.text(),
                    dialog.classe.text(),
                    dialog.annee.text(),
                    float(dialog.frais.value()),
                )
                self.service_eleve.creer(e)
                self.page_eleves.rafraichir_liste()
                self.page_dashboard.rafraichir()
                QtWidgets.QMessageBox.information(self, "Succès", "Élève ajouté.")
            except ValueError as ex:
                QtWidgets.QMessageBox.critical(self, "Erreur", str(ex))

    def modifier_eleve(self):
        eid = self.page_eleves.eleve_selectionne()
        if not eid:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un élève.")
            return

        eleve_data = self.service_eleve.obtenir(eid)
        dialog = DialogueAjoutEleve(self, eleve_data)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                e = Eleve(
                    dialog.nom.text(),
                    dialog.prenom.text(),
                    dialog.classe.text(),
                    dialog.annee.text(),
                    float(dialog.frais.value()),
                    id=eid,
                )
                self.service_eleve.modifier(e)
                self.page_eleves.rafraichir_liste()
                self.page_dashboard.rafraichir()
                QtWidgets.QMessageBox.information(self, "Succès", "Élève modifié.")
            except ValueError as ex:
                QtWidgets.QMessageBox.critical(self, "Erreur", str(ex))

    def supprimer_eleve(self):
        eid = self.page_eleves.eleve_selectionne()
        if not eid:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un élève.")
            return

        reponse = QtWidgets.QMessageBox.question(
            self, "Confirmation",
            "Êtes-vous sûr de vouloir supprimer cet élève ?")
        if reponse == QtWidgets.QMessageBox.Yes:
            self.service_eleve.supprimer(eid)
            self.page_eleves.rafraichir_liste()
            self.page_dashboard.rafraichir()
            QtWidgets.QMessageBox.information(self, "Succès", "Élève supprimé.")

    def enregistrer_paiement(self):
        eid = self.page_eleves.eleve_selectionne()
        if not eid:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un élève.")
            return

        dialog = DialoguePaiement(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                montant = float(dialog.montant.value())
                date_str = dialog.date.date().toString("yyyy-MM-dd")
                mode = dialog.mode.currentText()

                paiement = self.service_paiement.enregistrer(eid, montant, date_str, mode)
                self.page_eleves.rafraichir_liste()
                self.page_dashboard.rafraichir()

                donnees = self.service_paiement.donnees_recu(
                    self.service_paiement.obtenir(paiement.id))

                # Générer le reçu PDF automatiquement
                from recus import generer_recu_pdf
                import os
                chemin_pdf = f"recu_{donnees['numero_recu']}.pdf"
                pdf_ok = generer_recu_pdf(donnees, chemin_pdf)

                msg = "Paiement enregistré !\n\n"
                msg += f"Reçu n° {donnees['numero_recu']}\n"
                msg += f"Élève : {donnees['eleve_nom']} {donnees['eleve_prenom']}\n"
                msg += f"Montant : {formater_montant(donnees['montant'])}\n"
                msg += f"Solde après : {formater_montant(donnees['solde_apres'])}"
                if pdf_ok:
                    msg += "\n\nLe reçu PDF va s'ouvrir (Ctrl+P pour imprimer)."
                QtWidgets.QMessageBox.information(self, "Paiement enregistré", msg)

                # Ouvrir le reçu PDF (pour impression immédiate)
                if pdf_ok:
                    try:
                        os.startfile(chemin_pdf)
                    except Exception:
                        pass
            except Exception as ex:
                QtWidgets.QMessageBox.critical(self, "Erreur", str(ex))

    def afficher_fiche(self):
        eid = self.page_eleves.eleve_selectionne()
        if not eid:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un élève.")
            return

        self.page_fiche.afficher_eleve(eid)
        self.menu.setCurrentRow(2)

    def reimprimer_recu(self):
        """Réimprime le reçu du paiement sélectionné."""
        if not self.page_fiche.eleve_id:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un élève d'abord.")
            return

        selected = self.page_fiche.table_historique.selectedIndexes()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Info", "Sélectionnez un paiement dans l'historique.")
            return

        paiements = self.service_paiement.lister_par_eleve(self.page_fiche.eleve_id)
        row = selected[0].row()
        if row >= len(paiements):
            QtWidgets.QMessageBox.warning(self, "Info", "Paiement invalide.")
            return

        paiement = paiements[row]
        donnees = self.service_paiement.donnees_recu(paiement)

        from recus import generer_recu_pdf
        import os
        chemin_pdf = f"recu_{donnees['numero_recu']}.pdf"

        if generer_recu_pdf(donnees, chemin_pdf):
            QtWidgets.QMessageBox.information(self, "Succès", f"Reçu généré : {chemin_pdf}")
            try:
                os.startfile(chemin_pdf)
            except Exception:
                pass
        else:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Impossible de générer le PDF.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    base = BaseDonnees()
    repo_eleve = RepositoryEleve(base)
    repo_paiement = RepositoryPaiement(base)
    service_eleve = ServiceEleve(repo_eleve)
    service_paiement = ServicePaiement(repo_paiement, repo_eleve)

    fenetre = FenetrePrincipale(service_eleve, service_paiement)
    fenetre.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
