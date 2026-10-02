"""
Script pour packager EduPaie en .exe avec PyInstaller.
Lancer depuis la racine du projet : python build_exe.py
"""

import os
import shutil
import subprocess


def main():
    print("=== EduPaie Package Builder ===\n")

    # Vérifier que PyInstaller est installé
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller n'est pas installé.")
        print("Installez-le : pip install pyinstaller")
        return

    # Nettoyer les builds précédentes
    print("Nettoyage des builds precedentes...")
    for dossier in ["build", "dist"]:
        if os.path.exists(dossier):
            shutil.rmtree(dossier)
    if os.path.exists("EduPaie.spec"):
        os.remove("EduPaie.spec")

    print("Generation de l'executable (peut prendre 1-2 minutes)...\n")
    cmd = [
        "pyinstaller",
        "--onefile",              # Un seul fichier .exe
        "--windowed",             # Pas de console noire
        "--name", "EduPaie",      # Nom de l'exe
        # Inclure le schema SQL dans l'exe (Windows : separateur ';')
        "--add-data", "sql;sql",
        "principal.py",
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERREUR lors de la generation : {e}")
        return

    print("\n=== Build termine ===")
    print("Executable : dist/EduPaie.exe")
    print("\nPour distribuer :")
    print("  1. Copiez dist/EduPaie.exe dans un dossier")
    print("  2. Copiez ressources/edupaie.db a cote de l'exe (donnees de test)")
    print("  3. Double-cliquez EduPaie.exe")


if __name__ == "__main__":
    main()
