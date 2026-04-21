"""
Page Dashboard (Tableau de bord)
"""
import customtkinter as ctk
from vinted_app.services.finance_service import FinanceService
from vinted_app.services.stats_service import StatsService
from vinted_app.services.product_service import ProductService
from vinted_app.services.charts_service import ChartsService
from vinted_app.ui.chart_window import ChartWindow
from vinted_app import config
from vinted_app.utils.helpers import format_currency, format_percentage


class DashboardFrame(ctk.CTkFrame):
    """Frame du dashboard"""

    def __init__(self, parent, finance_service: FinanceService, 
                 stats_service: StatsService, product_service: ProductService):
        """Initialise le dashboard"""
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])

        self.finance_service = finance_service
        self.stats_service = stats_service
        self.product_service = product_service
        self.charts_service = ChartsService(product_service.db)  # Initialise le service de graphiques

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_ui()

    def _create_ui(self):
        """Crée l'interface du dashboard"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=config.COLORS["bg_primary"],
            label_text="Dashboard"
        )
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # === CARDS KPI ===
        kpi_data = [
            {
                "title": "Total Investi",
                "color": config.COLORS["info"],
                "icon": "💰",
                "value_fn": self.finance_service.get_total_invested,
                "format": lambda x: format_currency(x),
                "chart_fn": None  # Pas de graphique spécifique
            },
            {
                "title": "Total Gagné",
                "color": config.COLORS["success"],
                "icon": "💵",
                "value_fn": self.finance_service.get_total_earned,
                "format": lambda x: format_currency(x),
                "chart_fn": self.charts_service.get_monthly_sales_chart  # Graphique des ventes mensuelles
            },
            {
                "title": "Bénéfice Total",
                "color": config.COLORS["accent"],
                "icon": "📈",
                "value_fn": self.finance_service.get_total_profit,
                "format": lambda x: format_currency(x),
                "chart_fn": self.charts_service.get_profit_evolution_chart  # Graphique d'évolution des bénéfices
            },
            {
                "title": "Marge %",
                "color": config.COLORS["warning"],
                "icon": "📊",
                "value_fn": self.finance_service.get_profit_margin_percent,
                "format": lambda x: format_percentage(x),
                "chart_fn": self.charts_service.get_profit_by_category_chart  # Graphique profit par catégorie
            },
        ]

        for idx, kpi in enumerate(kpi_data):
            self._create_kpi_card(scroll_frame, idx % 4, idx // 4, kpi)

        # === STATS PRODUITS ===
        stats_title = ctk.CTkLabel(
            scroll_frame,
            text="Statistiques Produits",
            font=("Arial", 18, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        stats_title.grid(row=2, column=0, columnspan=4, sticky="w", pady=(30, 10))

        stats_cards = [
            {
                "title": "Total Produits",
                "icon": "📦",
                "color": config.COLORS["info"],
                "value_fn": lambda: self.stats_service.get_general_stats()['total_products'],
                "chart_fn": self.charts_service.get_products_distribution_chart
            },
            {
                "title": "En Stock",
                "icon": "🏪",
                "color": config.COLORS["neutral"],
                "value_fn": lambda: self.stats_service.get_general_stats()['in_stock'],
                "chart_fn": self.charts_service.get_products_distribution_chart
            },
            {
                "title": "En Vente",
                "icon": "🔄",
                "color": config.COLORS["warning"],
                "value_fn": lambda: self.stats_service.get_general_stats()['in_sale'],
                "chart_fn": self.charts_service.get_products_distribution_chart
            },
            {
                "title": "Vendus",
                "icon": "✓",
                "color": config.COLORS["success"],
                "value_fn": lambda: self.stats_service.get_general_stats()['sold'],
                "chart_fn": self.charts_service.get_profit_by_category_chart
            },
        ]

        for idx, card in enumerate(stats_cards):
            self._create_stat_card(scroll_frame, idx % 4, 3 + idx // 4, card)

        # === CHIFFRES AVANCÉS ===
        advanced_title = ctk.CTkLabel(
            scroll_frame,
            text="Analyses Avancées",
            font=("Arial", 18, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        advanced_title.grid(row=5, column=0, columnspan=4, sticky="w", pady=(30, 10))

        advanced_data = [
            {
                "title": "ROI",
                "icon": "🎯",
                "value": f"{self.finance_service.get_roi()}%",
                "description": "Retour sur investissement",
                "chart_fn": self.charts_service.get_roi_evolution_chart
            },
            {
                "title": "Bénéfice Moyen",
                "icon": "💎",
                "value": format_currency(self.finance_service.get_average_product_profit()),
                "description": "Par produit vendu",
                "chart_fn": self.charts_service.get_profit_by_category_chart
            },
            {
                "title": "Frais Totaux",
                "icon": "💸",
                "value": format_currency(self.finance_service.get_total_fees()),
                "description": "Tous les frais",
                "chart_fn": None
            },
            {
                "title": "Quantité Totale",
                "icon": "📊",
                "value": str(self.stats_service.get_general_stats()['total_quantity']),
                "description": "Articles en possession",
                "chart_fn": self.charts_service.get_products_distribution_chart
            },
        ]

        for idx, item in enumerate(advanced_data):
            self._create_advanced_card(scroll_frame, idx % 4, 6 + idx // 4, item)

    def _create_kpi_card(self, parent, col, row, data):
        """Crée une carte KPI cliquable"""
        # Frame principal contenant la carte
        card_container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        card_container.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card_container.grid_rowconfigure(0, weight=1)
        card_container.grid_columnconfigure(0, weight=1)
        
        # Créer la carte
        card = ctk.CTkFrame(
            card_container,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10,
            border_width=2,
            border_color=data["color"]
        )
        card.grid(row=0, column=0, sticky="nsew")

        # Titre et icône
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header_frame,
            text=data["icon"],
            font=("Arial", 24)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text=data["title"],
            font=("Arial", 12),
            text_color=config.COLORS["fg_text_secondary"]
        ).pack(side="left")

        # Valeur
        value = data["format"](data["value_fn"]())
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold"),
            text_color=data["color"]
        )
        value_label.pack(padx=15, pady=10)
        
        # Ajouter une indication de clic si un graphique est disponible
        if data["chart_fn"]:
            info_label = ctk.CTkLabel(
                card,
                text="🔍 Cliquez pour voir le graphique",
                font=("Arial", 9),
                text_color=config.COLORS["fg_text_secondary"]
            )
            info_label.pack(padx=15, pady=(0, 10))
            
            # Bind des événements de clic
            def on_click(event=None, chart_fn=data["chart_fn"], title=data["title"]):
                try:
                    figure = chart_fn()
                    ChartWindow(self.winfo_toplevel(), f"📊 {title}", figure)
                except Exception as e:
                    print(f"Erreur lors de la création du graphique: {e}")
            
            card.bind("<Button-1>", on_click)
            header_frame.bind("<Button-1>", on_click)
            value_label.bind("<Button-1>", on_click)
            info_label.bind("<Button-1>", on_click)
            
            # Change le curseur pour indiquer que c'est cliquable
            card.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            card.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            header_frame.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            header_frame.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            value_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            value_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            info_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            info_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))

    def _create_stat_card(self, parent, col, row, data):
        """Crée une carte de statistique cliquable"""
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        icon_label = ctk.CTkLabel(
            card,
            text=data["icon"],
            font=("Arial", 32)
        )
        icon_label.pack(pady=(15, 5))

        title_label = ctk.CTkLabel(
            card,
            text=data["title"],
            font=("Arial", 11),
            text_color=config.COLORS["fg_text_secondary"]
        )
        title_label.pack()

        value = str(data["value_fn"]())
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            text_color=data["color"]
        )
        value_label.pack(pady=10)
        
        # Ajouter une indication de clic
        if "chart_fn" in data and data["chart_fn"]:
            info_label = ctk.CTkLabel(
                card,
                text="🔍 Cliquez",
                font=("Arial", 9),
                text_color=config.COLORS["fg_text_secondary"]
            )
            info_label.pack(padx=15, pady=(0, 10))
            
            # Bind des événements de clic
            def on_click(event=None, chart_fn=data["chart_fn"], title=data["title"]):
                try:
                    figure = chart_fn()
                    ChartWindow(self.winfo_toplevel(), f"📊 {title}", figure)
                except Exception as e:
                    print(f"Erreur lors de la création du graphique: {e}")
            
            card.bind("<Button-1>", on_click)
            icon_label.bind("<Button-1>", on_click)
            title_label.bind("<Button-1>", on_click)
            value_label.bind("<Button-1>", on_click)
            info_label.bind("<Button-1>", on_click)
            
            # Change la couleur au survol
            card.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            card.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            icon_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            icon_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            title_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            title_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            value_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            value_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            info_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            info_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))

    def _create_advanced_card(self, parent, col, row, data):
        """Crée une carte avancée cliquable"""
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Icône et titre
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))

        icon_label = ctk.CTkLabel(
            header,
            text=data["icon"],
            font=("Arial", 20)
        )
        icon_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            header,
            text=data["title"],
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        title_label.pack(side="left")

        # Valeur
        value_label = ctk.CTkLabel(
            card,
            text=data["value"],
            font=("Arial", 20, "bold"),
            text_color=config.COLORS["accent"]
        )
        value_label.pack(padx=15, pady=(0, 5))

        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=data["description"],
            font=("Arial", 10),
            text_color=config.COLORS["fg_text_secondary"]
        )
        desc_label.pack(padx=15, pady=(0, 15))
        
        # Ajouter une indication de clic si graphique disponible
        if "chart_fn" in data and data["chart_fn"]:
            info_label = ctk.CTkLabel(
                card,
                text="🔍 Cliquez pour voir le graphique",
                font=("Arial", 8),
                text_color=config.COLORS["fg_text_secondary"]
            )
            info_label.pack(padx=15, pady=(0, 10))
            
            # Bind des événements de clic
            def on_click(event=None, chart_fn=data["chart_fn"], title=data["title"]):
                try:
                    figure = chart_fn()
                    ChartWindow(self.winfo_toplevel(), f"📊 {title}", figure)
                except Exception as e:
                    print(f"Erreur lors de la création du graphique: {e}")
            
            card.bind("<Button-1>", on_click)
            header.bind("<Button-1>", on_click)
            icon_label.bind("<Button-1>", on_click)
            title_label.bind("<Button-1>", on_click)
            value_label.bind("<Button-1>", on_click)
            desc_label.bind("<Button-1>", on_click)
            info_label.bind("<Button-1>", on_click)
            
            # Change la couleur au survol
            card.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            card.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            header.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            header.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            icon_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            icon_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            title_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            title_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            value_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            value_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))
            desc_label.bind("<Enter>", lambda e: card.configure(fg_color=config.COLORS["bg_tertiary"]))
            desc_label.bind("<Leave>", lambda e: card.configure(fg_color=config.COLORS["bg_secondary"]))

    def refresh(self):
        """Rafraîchit le dashboard"""
        # Recréer toute l'interface
        for widget in self.winfo_children():
            widget.destroy()
        self._create_ui()
