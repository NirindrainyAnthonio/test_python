import datetime
import json
import os


# ===============================
# Classe représentant une tâche
# ===============================
class Task:
    def __init__(
        self, title, description="", priority="Moyenne", deadline=None, completed=False
    ):
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.completed = completed

    def to_dict(self):
        """Convertir la tâche en dictionnaire pour sauvegarde JSON"""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline.strftime("%Y-%m-%d") if self.deadline else None,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data):
        """Recréer une tâche depuis un dictionnaire"""
        deadline = None
        if data.get("deadline"):
            try:
                deadline = datetime.datetime.strptime(
                    data["deadline"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "Moyenne"),
            deadline=deadline,
            completed=data.get("completed", False),
        )

    def __str__(self):
        status = "✅" if self.completed else "❌"
        deadline_str = self.deadline.strftime("%Y-%m-%d") if self.deadline else "Aucune"
        return f"[{status}] {self.title} (Priorité: {self.priority}, Échéance: {deadline_str})"


# ===============================
# Classe gestionnaire de tâches
# ===============================
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, title):
        """Supprimer une tâche par son titre"""
        self.tasks = [t for t in self.tasks if t.title.lower() != title.lower()]
        self.save_tasks()

    def mark_completed(self, title):
        """Marquer une tâche comme terminée"""
        for t in self.tasks:
            if t.title.lower() == title.lower():
                t.completed = True
        self.save_tasks()

    def update_task(
        self,
        old_title,
        new_title=None,
        new_desc=None,
        new_priority=None,
        new_deadline=None,
    ):
        """Modifier une tâche existante"""
        for t in self.tasks:
            if t.title.lower() == old_title.lower():
                if new_title:
                    t.title = new_title
                if new_desc:
                    t.description = new_desc
                if new_priority:
                    t.priority = new_priority
                if new_deadline:
                    t.deadline = new_deadline
        self.save_tasks()

    def search_tasks(self, keyword):
        """Rechercher une tâche par mot clé"""
        return [
            t
            for t in self.tasks
            if keyword.lower() in t.title.lower()
            or keyword.lower() in t.description.lower()
        ]

    def list_tasks(self, show_completed=True):
        """Lister les tâches (avec ou sans terminées)"""
        return [t for t in self.tasks if show_completed or not t.completed]

    def save_tasks(self):
        """Sauvegarde en JSON"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tasks], f, indent=4, ensure_ascii=False
            )

    def load_tasks(self):
        """Charger les tâches depuis JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]


# ===============================
# Interface utilisateur (menu)
# ===============================
def print_menu():
    print("\n=== Gestionnaire de tâches ===")
    print("1. Ajouter une tâche")
    print("2. Supprimer une tâche")
    print("3. Marquer une tâche comme terminée")
    print("4. Modifier une tâche")
    print("5. Rechercher des tâches")
    print("6. Afficher toutes les tâches")
    print("7. Quitter")


def get_priority():
    """Choisir la priorité"""
    print("Choisissez une priorité :")
    print("1. Basse")
    print("2. Moyenne")
    print("3. Haute")
    choice = input("Votre choix: ")
    if choice == "1":
        return "Basse"
    elif choice == "3":
        return "Haute"
    return "Moyenne"


def get_deadline():
    """Entrer une échéance optionnelle"""
    deadline_str = input("Date d'échéance (YYYY-MM-DD) ou vide: ").strip()
    if deadline_str:
        try:
            return datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            print("Format invalide, aucune échéance définie.")
    return None


def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Choisissez une option: ")

        if choice == "1":
            title = input("Titre: ")
            desc = input("Description: ")
            priority = get_priority()
            deadline = get_deadline()
            task = Task(title, desc, priority, deadline)
            manager.add_task(task)
            print("✅ Tâche ajoutée avec succès.")

        elif choice == "2":
            title = input("Titre de la tâche à supprimer: ")
            manager.remove_task(title)
            print("🗑️ Tâche supprimée.")

        elif choice == "3":
            title = input("Titre de la tâche à marquer terminée: ")
            manager.mark_completed(title)
            print("✅ Tâche marquée comme terminée.")

        elif choice == "4":
            old_title = input("Titre de la tâche à modifier: ")
            new_title = (
                input("Nouveau titre (laisser vide pour garder): ").strip() or None
            )
            new_desc = (
                input("Nouvelle description (laisser vide pour garder): ").strip()
                or None
            )
            print("Voulez-vous changer la priorité ? (o/n)")
            new_priority = get_priority() if input().lower() == "o" else None
            print("Voulez-vous changer l'échéance ? (o/n)")
            new_deadline = get_deadline() if input().lower() == "o" else None
            manager.update_task(
                old_title, new_title, new_desc, new_priority, new_deadline
            )
            print("✏️ Tâche mise à jour.")

        elif choice == "5":
            keyword = input("Mot clé: ")
            results = manager.search_tasks(keyword)
            if results:
                print("🔎 Résultats de la recherche:")
                for t in results:
                    print("-", t)
            else:
                print("Aucune tâche trouvée.")

        elif choice == "6":
            print("📋 Liste des tâches:")
            for t in manager.list_tasks():
                print("-", t)

        elif choice == "7":
            print("👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, essayez encore.")


if __name__ == "__main__":
    main()
