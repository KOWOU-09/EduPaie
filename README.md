# EduPaie — Gestion des paiements scolaires

**Application de gestion des paiements d'élèves pour établissements scolaires.**

Enregistrez les élèves, suivez leurs paiements, calculez les soldes automatiquement et générez des reçus numérotés.

---

## Installation rapide

### Prérequis
- Python 3.10+ (ou téléchargez l'exécutable Windows `.exe`)

### Par source (Python)

```bash
pip install -r requirements.txt
python principal.py
```

### Par exécutable Windows (.exe)

1. Téléchargez `EduPaie.exe` depuis `dist/`
2. Double-cliquez `EduPaie.exe`
3. La base de données se crée automatiquement

---

## Utilisation

### Démarrer

```bash
python principal.py
```

L'interface a **3 onglets** :
1. **📊 Tableau de bord** : stats globales (nb élèves, encaissé, restant, non soldés)
2. **👥 Élèves** : ajouter/modifier/supprimer, enregistrer paiements
3. **📋 Fiche élève** : infos + historique complet des paiements

### Créer des données test

```bash
python donnees_test.py
```

Génère 16 élèves avec des paiements variés (soldés, partiels, non payés).

---

## Documentation

| Document | Contenu |
|---|---|
| **[DOCUMENTATION.md](DOCUMENTATION.md)** | Architecture technique (3-4 pages) |
| **[MANUEL_UTILISATEUR.md](MANUEL_UTILISATEUR.md)** | Guide pour les secrétaires (1 page) |

---

## Structure du projet

```
EduPaie/
├── métier/                    Règles métier (ServiceEleve, ServicePaiement)
├── donnees/                   Base de données SQLite + repositories
├── principal.py               Interface PySide6 (3 pages)
├── recus.py                   Génération PDF des reçus
├── donnees_test.py            Script créant 16 élèves de test
├── build_exe.py               Packager en .exe
├── requirements.txt           Dépendances (PySide6, fpdf2)
├── README.md                  Ce fichier
├── DOCUMENTATION.md           Documentation technique
├── MANUEL_UTILISATEUR.md      Manuel pour l'utilisateur
└── ressources/                Fichier base.db
```

---

## Packaging en exécutable

Pour créer un `.exe` autonome (sans Python) :

```bash
pip install PyInstaller
python build_exe.py
```

L'exécutable se trouve dans `dist/EduPaie.exe`. Testez-le sur une machine sans Python !

---

## Fonctionnalités

 **Gestion des élèves** : ajouter, modifier, supprimer  
 **Enregistrement paiements** : montant, date, mode (Espèces/Chèque/Virement/Mobile Money)  
 **Calcul automatique du solde** : affiché en temps réel  
 **Statut de paiement** : Soldé / Partiellement payé / Non payé  
 **Historique complet** : tous les paiements par élève  
 **Reçus numérotés** : PDF uniques et réimprimables  
 **Tableau de bord** : vue d'ensemble des stats  

---

## Technologie

- **Langage** : Python 3.13
- **Interface** : PySide6
- **Base de données** : SQLite (fichier unique `edupaie.db`)
- **Reçus PDF** : fpdf2
- **Packaging** : PyInstaller

---

## Limitations connues

- Pas de multi-utilisateur concurrent (SQLite est single-threaded)
- Pas d'authentification
- Base livrée manuelle (à recréer avec `donnees_test.py`)

---

## Support

- Consulter **DOCUMENTATION.md** pour l'architecture
- Consulter **MANUEL_UTILISATEUR.md** pour les tâches courantes
- Lancer `python donnees_test.py` pour régénérer la base

---

**Version** : 1.0  
**Licence** : MIT




