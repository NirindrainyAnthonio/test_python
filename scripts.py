#!/usr/bin/env python3

import subprocess
import sys
import os


def get_staged_python_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def run_command(command, description):
    """
    Execute une commande shell.
    Si la commande echoue, affiche l'erreur et quitte le script.
    """
    print(f"{description}")
    print(f"   $ {' '.join(command)}")

    result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

    print(result)
    sys.exit(1)

    # try:
    #     result = subprocess.run(
    #         command,
    #         capture_output=True,
    #         text=True,
    #         check=False,
    #     )

    #     print()
    #     sys.exit(1)

    #     if result.returncode == 0:
    #         if result.stdout.strip():
    #             print("Succès - Sortie :")
    #             print(result.stdout.strip())
    #         else:
    #             print("Aucune erreur detectee.")
    #         return True
    #     else:
    #         print(" ECHEC :")
    #         if result.stderr.strip():
    #             print(result.stderr.strip())
    #         elif result.stdout.strip():
    #             print(result.stdout.strip())
    #         print(f"Commande echouee : {' '.join(command)} (code: {result.returncode})")
    #         sys.exit(1)

    # except FileNotFoundError:
    #     print(f"Erreur : la commande '{command[0]}' est introuvable.")
    #     print(f"   Installez-la avec : pip install {command[0]}")
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"Erreur inattendue : {e}")
    #     sys.exit(1)


def run_code_quality_checks():
    """
    Execute les verifications de qualite uniquement sur les fichiers Python stages.
    S'arrête dès qu'une commande echoue.
    """
    print("Demarrage des verifications sur les fichiers modifies...")

    # Recuperer uniquement les fichiers .py stages
    staged_files = get_staged_python_files()

    if not staged_files:
        print("Aucun fichier Python modifie trouve. (rien à verifier)")
        return

    print(f"Fichiers à verifier : {', '.join(staged_files)}\n")

    # 1. Formatage avec black
    if staged_files:
        run_command(
            ["black"] + staged_files,
            "Verification du formatage avec Black (verification seule)",
        )

    # 2. Tri des imports avec isort
    if staged_files:
        run_command(
            ["isort", "--check-only"] + staged_files,
            "Verification des imports avec isort",
        )

    # 3. Formatage avec ruff
    if staged_files:
        run_command(
            ["ruff", "format", "--check"] + staged_files,
            "Verification du formatage avec ruff",
        )

    # 4. Verification de securite des dependances
    if os.path.isfile("requirements.txt"):
        run_command(
            ["safety", "check", "-r", "requirements.txt"],
            "Verification de securite avec safety (requirements.txt)",
        )
    else:
        print("Skipping safety check: requirements.txt non trouve.")

    # 5. Verification de style avec flake8
    if staged_files:
        run_command(["flake8"] + staged_files, "Verification du style avec flake8")

    # 6. Analyse statique avec ruff
    if staged_files:
        run_command(["ruff", "check"] + staged_files, "Analyse du code avec ruff")

    print("Toutes les verifications ont reussi !")
    print("Tu peux maintenant valider ton commit.")


if __name__ == "__main__":
    run_code_quality_checks()
