import os
import subprocess

# Dossiers à ignorer
IGNORE_DIRS = {"venv", "__pycache__", "node_modules", ".git"}


def format_imports(directory="."):
    for root, dirs, files in os.walk(directory):
        # On enlève les dossiers à ignorer
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Formatage des imports : {file_path}")
                subprocess.run(["isort", file_path])


if __name__ == "__main__":
    format_imports()
