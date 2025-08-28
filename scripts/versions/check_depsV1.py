import subprocess
import sys

import pkg_resources


def check_and_install_dependencies(requirements_file="requirements.txt"):
    try:
        with open(requirements_file, "r") as f:
            requirements = f.readlines()

        requirements = [
            req.strip()
            for req in requirements
            if req.strip() and not req.startswith("#")
        ]

        missing_or_conflict = []

        for req in requirements:
            try:
                pkg_resources.require(req)
                print(f"[OK] {req}")
            except pkg_resources.DistributionNotFound:
                print(f"[MANQUANT] {req}")
                missing_or_conflict.append(req)
            except pkg_resources.VersionConflict as e:
                print(f"[CONFLIT] {req} → {e.report()}")
                missing_or_conflict.append(req)

        if missing_or_conflict:
            print("\n🚀 Installation des dépendances manquantes...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", requirements_file]
            )
            print("✅ Installation terminée.")
        else:
            print("\nToutes les dépendances sont déjà installées et compatibles.")

    except FileNotFoundError:
        print(f"❌ Le fichier {requirements_file} n’existe pas.")


if __name__ == "__main__":
    check_and_install_dependencies()
