import subprocess
import sys

# Commandes à exécuter dans l'ordre
COMMANDS = [
    ["black", "."],
    ["isort", "."],
    ["ruff", "check", "."],
    ["ruff", "format", "."],
    ["bandit", "-ll", "-r", "."],
    ["safety", "scan", "-r", "requirements.txt"],
    ["semgrep", "ci"],
    ["flake8", "--max-line-length=250", "."],
]


def run_command(cmd):
    """Exécute une commande et stoppe si elle échoue"""
    print(f"e: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        print(f"Succes: {' '.join(cmd)}")
    except subprocess.CalledProcessError as e:
        print(f"Echec: {' '.join(cmd)} (code {e.returncode})")
        if e.stdout.strip():
            print("\n--- Sortie standard ---")
            print(e.stdout.strip())
        if e.stderr.strip():
            print("\n--- Sortie erreur ---")
            print(e.stderr.strip())
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Commande introuvable: {cmd[0]} (installe-la avant de relancer)")
        sys.exit(1)


def main():
    for cmd in COMMANDS:
        run_command(cmd)  # stoppe automatiquement si erreur
    print("Tous les checks sont passés avec succès !")


if __name__ == "__main__":
    main()
