import subprocess
import sys

import pkg_resources


def check_and_fix_dependencies(requirements_file="requirements.txt"):
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
        conflict_packages = []

        for req in requirements:
            try:
                pkg_resources.require(req)
                print(f"[OK] {req}")
            except pkg_resources.DistributionNotFound:
                print(f"[MANQUANT] {req}")
                missing_packages.append(req)
            except pkg_resources.VersionConflict as e:
                print(f"[CONFLIT] {req} → {e.report()}")
                conflict_packages.append(req)

        # Installer les packages manquants
        if missing_packages:
            print("\n🚀 Installation des packages manquants...")
            for pkg in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print("✅ Packages manquants installés.")

        # Mettre à jour les packages en conflit
        if conflict_packages:
            print("\n⚡ Mise à jour des packages en conflit...")
            for pkg in conflict_packages:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", pkg]
                )
            print("✅ Packages en conflit mis à jour.")

        # Si tout est déjà à jour, mettre à jour requirements.txt
        if not missing_packages and not conflict_packages:
            print("\nToutes les dépendances sont déjà installées et à jour.")
            print("💾 Mise à jour du fichier requirements.txt avec pip freeze...")
            with open(requirements_file, "w") as f:
                subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f)
            print("✅ requirements.txt mis à jour.")

    except FileNotFoundError:
        print(f"❌ Le fichier {requirements_file} n’existe pas.")


if __name__ == "__main__":
    check_and_fix_dependencies()
