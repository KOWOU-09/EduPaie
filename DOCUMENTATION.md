# EduPaie — Documentation Technique

## 1. Vue d'ensemble

EduPaie est une application desktop de gestion des paiements scolaires. Elle permet aux établissements d'enregistrer les élèves, de suivre les paiements, de calculer automatiquement les soldes et de générer des reçus numérotés.

**Objectif métier** : Remplacer les cahiers papier par une application fiable, traçable et légale.

## 2. Architecture

### Architecture en couches

L'application suit une **architecture strictement en trois couches** :

```
Interface (PySide6)
    ↓
Métier (Services)
    ↓
Données (Repositories + SQLite)
```

**Avantage** : Isolation des responsabilités. Les tests et la maintenance sont simplifiés.

### Dossiers

- **`métier/`** : Services (règles métier), modèles, configuration
- **`donnees/`** : Base de données SQLite, repositories (DAO)
- **`principal.py`** : Interface PySide6 (3 pages : tableau de bord, élèves, fiche)
- **`recus.py`** : Génération PDF des reçus
- **`donnees_test.py`** : Script de données test

## 3. Modélisation des données

### Schéma

Deux tables relationnelles :

```sql
ELEVE
  id (PK)
  nom, prenom, classe, annee_scolaire
  frais_total
  date_creation

PAIEMENT
  id (PK)
  eleve_id (FK → ELEVE)
  numero_recu (UNIQUE)
  montant, date_paiement, mode_paiement
  date_creation
```

### Calculs

- **Solde** = `frais_total − SUM(paiements.montant)`
- **Statut** : dérivé du solde (Soldé / Partiellement payé / Non payé)
- **Vue SQL** `v_eleves_solde` : centralise ces calculs

### Intégrité

- `montant > 0` (check)
- `frais_total >= 0` (check)
- Clé étrangère avec `ON DELETE CASCADE` (supprimer un élève → supprimer ses paiements)
- `PRAGMA foreign_keys = ON` activé à chaque connexion

## 4. Couche métier (services)

### ServiceEleve
- Validation des champs (nom, frais > 0, etc.)
- CRUD simple

### ServicePaiement (le cœur)
- **Numérotation unique des reçus** : `REC-2025-0001`, `0002`, etc.
- **Règle clé** : Un paiement ne peut jamais faire devenir le solde négatif
  - Levée d'une exception `ErreurSoldeInsuffisant` si `montant > solde_restant`
- Calcul du solde après paiement (réimpression identique du reçu)

## 5. Interface (PySide6)

### Page 1 : Tableau de bord
- 4 cartes (Élèves, Encaissé, Restant, Non soldés)
- Liste filtrée par statut de paiement

### Page 2 : Élèves
- Recherche par nom/prénom
- Filtre par classe
- Tableau avec colonnes (Nom, Prénom, Classe, Année, Frais, Payé, Solde, Statut)
- Boutons : Ajouter, Modifier, Supprimer, Enregistrer paiement, Fiche détail

### Page 3 : Fiche élève
- Infos de l'élève (nom, classe, frais, payé, solde, statut)
- **Historique chronologique** de tous les paiements
- Numéro de reçu, date, montant, mode, solde après (réimprimable)

### Dialogues
- **Ajouter/Modifier élève** : formulaire avec validation
- **Enregistrer paiement** : montant, date, mode, avec validation solde

## 6. Génération des reçus

**Format** : PDF lisible et professionnel
- En-tête : nom et adresse de l'école
- Numéro unique, date, mode
- Infos élève (nom, prénom, classe, année)
- Montant payé, solde restant après paiement
- Pied de page avec date/heure

**Réimpression** : Rechercher le paiement dans l'historique et régénérer le PDF (identique à l'original grâce au numéro unique et au cumul jusqu'à ce paiement)

## 7. Données de test

**16 élèves** avec cas variés :
- 5 **Soldés** (100% payé)
- 6 **Partiellement payés** (50-90%)
- 5 **Non payés** (0%)

Statistiques finales : 1 825 000 FCFA encaissés, 1 805 000 restants

Générer : `python donnees_test.py`

## 8. Choix techniques justifiés

| Choix | Justification |
|---|---|
| **SQLite** | Moteur embarqué, pas de serveur, une seule base `.db` à livrer |
| **PySide6** | GUI riche, native Windows, open-source |
| **Repositories** | Isolation du SQL, testabilité, maintenabilité |
| **Numéro reçu en base** | Garantit l'unicité (contrainte UNIQUE) |
| **Vue SQL solde** | Pas de redondance, toujours à jour |
| **fpdf2** | Léger, pas de dépendance lourde (pas Reportlab) |

## 9. Limitations et améliorations possibles

**Limitations connues** :
- Pas de user management (pas de login)
- Pas de multi-utilisateur concurrent (SQLite ne scalpe pas)
- Pas de sauvegarde/export des anciennes bases (à faire à la main)
- Pas d'impression directe d'étiquettes

**Amélioration futures** :
- Authentification et logs d'audit
- Export Excel des données
- Rappels SMS/email (intégration Twilio)
- Multi-établissement

## 10. Dépannage

| Problème | Solution |
|---|---|
| Reçu n'apparaît pas | Vérifier que fpdf2 est installé : `pip install fpdf2` |
| Erreur "solde négatif" | Normal, c'est une sécurité. Montant > solde_restant → refusé |
| Base vide | Lancer `python donnees_test.py` |
| Interface gelée | Peut être un paiement qui prend du temps. Patient, ou relancer |

## 11. Fichiers clés

```
métier/service_paiement.py  → Règle du solde, numéro reçu
donnees/repo_eleve.py       → SQL des élèves
donnees/repo_paiement.py    → SQL des paiements
principal.py                → Interface (300+ lignes, bien structurée)
recus.py                    → Génération PDF
```

---

**Version** : 1.0  
**Date** : Septembre 2025  
**Auteur** : Étudiant TP EduPaie
