import subprocess
import sys

# Commandes de lint/format à exécuter (sera filtré par type de fichier)
COMMANDS = {
    "python": [
        ["black"],
        ["isort"],
        ["ruff", "check"],
        ["ruff", "format"],
        ["bandit", "-ll", "-r"],
        ["flake8", "--max-line-length=250"],
    ],
    "requirements": [["safety", "scan", "-r"]],
    "generic": [
        ["semgrep", "ci"],
    ],
}


def get_changed_files():
    # Récupère les fichiers modifiés dans le commit
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    return files


def run_command(cmd, files=None):
    # Exécute une commande sur les fichiers donnés et stoppe si erreur
    full_cmd = cmd.copy()
    if files:
        full_cmd.extend(files)

    print(f"Execution: {' '.join(full_cmd)}")
    try:
        result = subprocess.run(full_cmd, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        print(f"Succes: {' '.join(full_cmd)}")
    except subprocess.CalledProcessError as e:
        print(f"Échec: {' '.join(full_cmd)} (code {e.returncode})")
        if e.stdout.strip():
            print("\n--- Sortie standard ---")
            print(e.stdout.strip())
        if e.stderr.strip():
            print("\n--- Sortie erreur ---")
            print(e.stderr.strip())
        sys.exit(e.returncode)


def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("Aucun fichier modifié détecté ")
        return

    py_files = [f for f in changed_files if f.endswith(".py")]
    req_files = [f for f in changed_files if f == "requirements.txt"]

    # Étape 1 : Python
    if py_files:
        for cmd in COMMANDS["python"]:
            run_command(cmd, py_files)

    # Étape 2 : Safety (requirements.txt)
    if req_files:
        for cmd in COMMANDS["requirements"]:
            run_command(cmd, req_files)

    # Étape 3 : Semgrep (analyse globale)
    for cmd in COMMANDS["generic"]:
        run_command(cmd)

    print("Tous les checks sont passés avec succès !")


if __name__ == "__main__":
    main()
