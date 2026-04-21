"""
Point d'entrée de l'application Vinted Stock Manager
"""
from vinted_app.ui.main_window import MainWindow


def main():
    """Lance l'application"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
