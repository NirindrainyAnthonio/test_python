import subprocess
import sys

import pkg_resources


def check_and_install_missing(requirements_file="requirements.txt"):
    try:
        with open(requirements_file, "r") as f:
            requirements = f.readlines()

        # Nettoyage de la liste
        requirements = [
            req.strip()
            for req in requirements
            if req.strip() and not req.startswith("#")
        ]

        missing_packages = []

        for req in requirements:
            try:
                pkg_resources.require(req)
                print(f"[OK] {req}")
            except pkg_resources.DistributionNotFound:
                print(f"[MANQUANT] {req}")
                missing_packages.append(req)
            except pkg_resources.VersionConflict as e:
                print(f"[CONFLIT] {req} → {e.report()}")

        if missing_packages:
            print("\n🚀 Installation des packages manquants...")
            for pkg in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print("✅ Installation des packages manquants terminée.")
        else:
            print("\nToutes les dépendances sont déjà installées.")

    except FileNotFoundError:
        print(f"❌ Le fichier {requirements_file} n’existe pas.")


if __name__ == "__main__":
    check_and_install_missing()
