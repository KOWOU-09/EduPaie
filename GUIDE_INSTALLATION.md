# EduPaie — Guide d'installation (Windows)

Ce guide explique comment installer et lancer **EduPaie** sur un ordinateur
Windows, **sans avoir besoin d'installer Python**.

---

## 1. Ce dont vous avez besoin

Deux fichiers, fournis avec le projet :

| Fichier | Rôle |
|---|---|
| `EduPaie.exe` | L'application (≈ 58 Mo) |
| `edupaie.db` | La base de données (élèves et paiements) |

> ⚠️ Ces deux fichiers doivent **toujours rester ensemble** dans le même dossier.

---

## 2. Installation (une seule fois)

1. Créez un dossier sur le disque, par exemple :
   ```
   C:\EduPaie
   ```
2. Copiez-y les **deux fichiers** : `EduPaie.exe` et `edupaie.db`.
3. (Optionnel mais pratique) Créez un raccourci sur le Bureau :
   - Clic **DROIT** sur `EduPaie.exe`
   - **« Envoyer vers » → « Bureau (créer un raccourci) »**

C'est terminé. Aucune autre installation n'est nécessaire.

---

## 3. Lancer l'application

- **Double-cliquez** sur `EduPaie.exe` (ou sur le raccourci du Bureau).
- L'application s'ouvre avec les données déjà enregistrées.

### Message « Windows a protégé votre ordinateur » ?
C'est normal : l'application n'est pas signée numériquement.
- Cliquez sur **« Informations complémentaires »**
- Puis sur **« Exécuter quand même »**

L'application est sans danger (c'est votre logiciel).

---

## 4. Où sont enregistrées les données ?

Tout est stocké **automatiquement** dans le fichier `edupaie.db`.
Chaque élève ajouté, chaque paiement enregistré y est sauvegardé.

- Vous n'avez **jamais besoin de « sauvegarder »** manuellement.
- À la réouverture, toutes les données sont toujours là.

---

## 5. Règles importantes

| À faire | À ne pas faire |
|---|---|
| Garder `EduPaie.exe` et `edupaie.db` ensemble | ❌ Supprimer `edupaie.db` (perte de toutes les données) |
| Copier `edupaie.db` sur une clé USB de temps en temps (sauvegarde) | ❌ Séparer les deux fichiers |

---

## 6. En cas de problème

| Problème | Solution |
|---|---|
| L'application ne s'ouvre pas | Vérifiez que `edupaie.db` est bien à côté de `EduPaie.exe` |
| L'antivirus bloque l'application | Ajoutez une exception pour le dossier `C:\EduPaie` |
| Les données ont disparu | Restaurez une copie de sauvegarde de `edupaie.db` |

---

**Version 1.0 — EduPaie, gestion des paiements scolaires**
