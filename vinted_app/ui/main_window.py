"""
Fenêtre principale de l'application
"""
import customtkinter as ctk
from vinted_app.ui.dashboard import DashboardFrame
from vinted_app.ui.product_list import ProductListFrame
from vinted_app.ui.add_product import AddProductFrame
from vinted_app.services.product_service import ProductService
from vinted_app.services.finance_service import FinanceService
from vinted_app.services.stats_service import StatsService
from vinted_app.database.db import DatabaseManager
from vinted_app import config


class MainWindow(ctk.CTk):
    """Fenêtre principale de l'application"""

    def __init__(self):
        """Initialise la fenêtre principale"""
        super().__init__()

        # Configuration de la fenêtre
        self.title(config.APP_TITLE)
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.minsize(1000, 700)

        # Apparence
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialisation des services
        self.db = DatabaseManager()
        self.product_service = ProductService(self.db)
        self.finance_service = FinanceService(self.db)
        self.stats_service = StatsService(self.db)

        # Ajouter les données de test si base vide
        self.db.add_sample_data()

        # Interface
        self._create_ui()

    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Configuration de la grille
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === SIDEBAR ===
        self._create_sidebar()

        # === FRAME PRINCIPAL ===
        self.main_frame = ctk.CTkFrame(self, fg_color=config.COLORS["bg_primary"])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Frames du contenu
        self.frames = {}

        # Dashboard
        self.frames['dashboard'] = DashboardFrame(
            self.main_frame,
            self.finance_service,
            self.stats_service,
            self.product_service
        )
        self.frames['dashboard'].grid(row=0, column=0, sticky="nsew")

        # Products
        self.frames['products'] = ProductListFrame(
            self.main_frame,
            self.product_service,
            self.finance_service,
            self.refresh_all
        )
        self.frames['products'].grid(row=0, column=0, sticky="nsew")

        # Add Product
        self.frames['add_product'] = AddProductFrame(
            self.main_frame,
            self.product_service,
            self.refresh_all
        )
        self.frames['add_product'].grid(row=0, column=0, sticky="nsew")

        # Afficher le dashboard par défaut
        self.show_frame('dashboard')

    def _create_sidebar(self):
        """Crée la barre latérale de navigation"""
        sidebar = ctk.CTkFrame(
            self,
            fg_color=config.COLORS["bg_secondary"],
            width=config.SIDEBAR_WIDTH
        )
        sidebar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)
        sidebar.grid_rowconfigure(1, weight=1)

        # Logo/Titre
        title = ctk.CTkLabel(
            sidebar,
            text="📊 VINTED\nSTOCK",
            font=("Arial", 18, "bold"),
            text_color=config.COLORS["accent"]
        )
        title.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Boutons de navigation
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=20)
        nav_frame.grid_columnconfigure(0, weight=1)

        buttons = [
            ("📈 Dashboard", "dashboard"),
            ("📦 Produits", "products"),
            ("➕ Ajouter Produit", "add_product"),
        ]

        for idx, (label, frame_name) in enumerate(buttons):
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                command=lambda fn=frame_name: self.show_frame(fn),
                fg_color=config.COLORS["bg_tertiary"],
                hover_color=config.COLORS["accent"],
                text_color=config.COLORS["fg_text"],
                font=("Arial", 12, "bold"),
                height=50,
                corner_radius=8
            )
            btn.grid(row=idx, column=0, sticky="ew", pady=10, padx=5)

        # Footer
        footer = ctk.CTkLabel(
            sidebar,
            text="v1.0.0",
            font=("Arial", 10),
            text_color=config.COLORS["fg_text_secondary"]
        )
        footer.grid(row=2, column=0, sticky="s", pady=20, padx=20)

    def show_frame(self, frame_name: str):
        """Affiche un frame spécifique"""
        for frame in self.frames.values():
            frame.grid_remove()

        self.frames[frame_name].grid()

        # Rafraîchir le contenu si nécessaire
        if hasattr(self.frames[frame_name], 'refresh'):
            self.frames[frame_name].refresh()

    def refresh_all(self):
        """Rafraîchit tous les frames"""
        for frame in self.frames.values():
            if hasattr(frame, 'refresh'):
                frame.refresh()

    def run(self):
        """Lance l'application"""
        self.mainloop()


def main():
    """Point d'entrée de l'application"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
