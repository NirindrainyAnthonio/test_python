import os
import subprocess
import sys

# Liste des dossiers à ignorer
IGNORE_DIRS = {"venv", "__pycache__", "node_modules", ".git"}


def format_python_code(directory="."):
    for root, dirs, files in os.walk(directory):
        # Supprimer les dossiers à ignorer de la recherche
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Formatage de : {file_path}")
                # Utiliser Python pour appeler black (plus sûr sur Windows)
                subprocess.run([sys.executable, "-m", "black", file_path])


if __name__ == "__main__":
    format_python_code()
