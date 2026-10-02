# EduPaie — Manuel d'utilisation

## Démarrage

```bash
python principal.py
```

L'application ouvre avec un tableau de bord et trois onglets à gauche.

---

## Tâche 1 : Ajouter un élève

1. Cliquez sur l'onglet **👥 Élèves** (à gauche)
2. Cliquez sur **Ajouter**
3. Remplissez :
   - **Nom** : nom de famille
   - **Prénom** : prénom
   - **Classe** : ex. tle,1er,2nd
   - **Année scolaire** : ex. "2024-2025" (pré-rempli)
   - **Frais (FCFA)** : montant total à payer pour l'année
4. Cliquez **OK**

L'élève apparaît dans la liste et dans le tableau de bord.

---

## Tâche 2 : Modifier un élève

1. Allez à l'onglet **👥 Élèves**
2. Cliquez sur l'élève dans la table pour le sélectionner (elle devient bleue)
3. Cliquez **Modifier**
4. Changez les champs
5. Cliquez **OK**

---

## Tâche 3 : Enregistrer un paiement

1. Allez à l'onglet **👥 Élèves**
2. **Sélectionnez l'élève** (clic sur sa ligne)
3. Cliquez **Enregistrer paiement**
4. Remplissez :
   - **Montant (FCFA)** : ce qu'il paye
   - **Date** : jour du paiement (calendrier popup)
   - **Mode de paiement** : Espèces / Chèque / Virement / Mobile Money
5. Cliquez **Enregistrer**

Un reçu s'affiche avec :
- Numéro unique (ex. REC-2025-0001)
- Nom et classe de l'élève
- Montant payé
- **Solde après paiement** (important : reste à payer)

⚠️ Si le montant dépasse le solde restant, vous verrez une erreur : c'est normal, il faut un montant plus petit.

---

## Tâche 4 : Voir la fiche d'un élève

1. Allez à l'onglet **👥 Élèves**
2. Sélectionnez l'élève
3. Cliquez **Fiche détail**

Vous voyez :
- **Infos** : nom, classe, frais totaux, montant payé, solde restant, statut
- **Historique** : tous les paiements enregistrés (dates, montants, soldes après)

---

## Tâche 5 : Réimprimer un reçu

1. Allez à l'onglet **📋 Fiche élève**
2. Sélectionnez l'élève dans l'historique en haut
3. Cliquez **Réimprimer le reçu**

Le PDF se génère et s'ouvre (identique à l'original).

---

## Tableau de bord

L'onglet **📊 Tableau de bord** montre :
- **Élèves** : combien il y a
- **Encaissé** : total payé (tous les élèves)
- **Restant** : total à encaisser
- **Non soldés** : combien d'élèves ne sont pas payés

Vous pouvez **filtrer par statut** (Tous / Soldé / Partiellement payé / Non payé).

---

## Suppression d'un élève

⚠️ **Attention** : supprime aussi tous ses paiements !

1. Sélectionnez l'élève
2. Cliquez **Supprimer**
3. Confirmez

---

## Recherche et filtre

Dans l'onglet **👥 Élèves** :
- **Rechercher** : tapez un nom ou prénom (en temps réel)
- **Classe** : filtre exact

Tapez "kodjo" pour voir tous les élèves avec "kodjo" dans le nom.

---

## Points importants

✅ L'application garde automatiquement l'historique de tous les paiements  
✅ Chaque reçu a un numéro unique et réimprimable  
✅ Le solde se calcule automatiquement (frais − somme des paiements)  
✅ Un paiement ne peut jamais rendre le solde négatif  

---

## Besoin d'aide ?

- Relancer l'app : `python principal.py`
- Recréer les données de test : `python donnees_test.py`
- Consulter la documentation technique : `DOCUMENTATION.md`
