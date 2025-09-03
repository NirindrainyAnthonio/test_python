import subprocess
import sys

# Commandes de lint/format à exécuter
COMMANDS = {
    "python": [
        ["black"],
        ["isort"],
        ["ruff", "check"],
        ["ruff", "format"],
        ["flake8", "--max-line-length=250"],
    ],
    "requirements": [["safety", "scan", "-r", "requirements.txt"]],
    "generic": [["semgrep", "ci"]],
}


def get_changed_files():
    """Récupère les fichiers modifiés dans le commit"""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def run_command(cmd, files=None):
    """Exécute une commande et affiche Passed/Failed/Skipped"""
    full_cmd = cmd.copy()

    # On ajoute les fichiers seulement pour les outils qui l'acceptent
    if files and cmd[0] not in ["bandit", "safety", "semgrep"]:
        full_cmd.extend(files)

    print(f"Execution: {' '.join(full_cmd)}")
    try:
        result = subprocess.run(full_cmd, check=True, capture_output=True, text=True)

        if result.stdout.strip():
            print(result.stdout.strip())

        print(f"Passed: {' '.join(full_cmd)}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Failed: {' '.join(full_cmd)} (code {e.returncode})")

        if e.stdout.strip():
            print("\n--- Sortie standard ---")
            print(e.stdout.strip())

        if e.stderr.strip():
            print("\n--- Sortie erreur ---")
            print(e.stderr.strip())

        sys.exit(1)  # stoppe immédiatement le commit


def run_bandit(py_files):
    """Exécute Bandit correctement (sur les fichiers modifiés ou tout le projet)"""
    if py_files:
        full_cmd = ["bandit", "-ll", "-f", "json"] + py_files
    else:
        full_cmd = ["bandit", "-ll", "-r", ".", "-f", "json"]

    print(f"Execution: {' '.join(full_cmd)}")
    try:
        result = subprocess.run(full_cmd, check=True, capture_output=True, text=True)
        print(result.stdout.strip() or "Bandit check passed")
        print("Passed: Bandit")
    except subprocess.CalledProcessError as e:
        print("Failed: Bandit")
        if e.stdout.strip():
            print("\n--- Sortie standard ---")
            print(e.stdout.strip())
        if e.stderr.strip():
            print("\n--- Sortie erreur ---")
            print(e.stderr.strip())
        sys.exit(1)


def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("Aucun fichier modifié détecté")
        return

    py_files = [f for f in changed_files if f.endswith(".py")]
    req_files = [f for f in changed_files if f == "requirements.txt"]

    # Étape 1 : Python
    if py_files:
        for cmd in COMMANDS["python"]:
            run_command(cmd, py_files)
        run_bandit(py_files)
    else:
        print("Skipped: vérifications Python (aucun fichier .py modifié)")

    # Étape 2 : Safety (requirements.txt)
    if req_files:
        for cmd in COMMANDS["requirements"]:
            run_command(cmd)
    else:
        print("Skipped: vérification des dépendances (requirements.txt non modifié)")

    # Étape 3 : Semgrep (analyse globale)
    for cmd in COMMANDS["generic"]:
        run_command(cmd)

    print("Tous les checks sont passés avec succès !")


if __name__ == "__main__":
    main()
