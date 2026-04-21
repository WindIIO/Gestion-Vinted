"""
Fenêtre de visualisation des graphiques
"""
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from vinted_app import config


class ChartWindow(ctk.CTkToplevel):
    """Fenêtre pour afficher un graphique"""

    def __init__(self, parent, title: str, figure: Figure):
        """
        Initialise la fenêtre de graphique
        
        Args:
            parent: Parent window
            title: Titre de la fenêtre
            figure: Figure matplotlib à afficher
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Configure la couleur de fond
        self.configure(fg_color=config.COLORS["bg_primary"])
        
        # Configure la grille
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Crée le canvas pour matplotlib
        canvas_frame = ctk.CTkFrame(self, fg_color=config.COLORS["bg_primary"])
        canvas_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Intègre matplotlib dans tkinter
        canvas = FigureCanvasTkAgg(figure, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Bouton fermer
        close_btn = ctk.CTkButton(
            self,
            text="Fermer",
            command=self.destroy,
            fg_color=config.COLORS["accent"],
            hover_color="#0052CC",
            height=35,
            font=("Arial", 11, "bold")
        )
        close_btn.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
