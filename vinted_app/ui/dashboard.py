"""
Page Dashboard (Tableau de bord)
"""
import customtkinter as ctk
from vinted_app.services.finance_service import FinanceService
from vinted_app.services.stats_service import StatsService
from vinted_app.services.product_service import ProductService
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
                "format": lambda x: format_currency(x)
            },
            {
                "title": "Total Gagné",
                "color": config.COLORS["success"],
                "icon": "💵",
                "value_fn": self.finance_service.get_total_earned,
                "format": lambda x: format_currency(x)
            },
            {
                "title": "Bénéfice Total",
                "color": config.COLORS["accent"],
                "icon": "📈",
                "value_fn": self.finance_service.get_total_profit,
                "format": lambda x: format_currency(x)
            },
            {
                "title": "Marge %",
                "color": config.COLORS["warning"],
                "icon": "📊",
                "value_fn": self.finance_service.get_profit_margin_percent,
                "format": lambda x: format_percentage(x)
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
                "value_fn": lambda: self.stats_service.get_general_stats()['total_products']
            },
            {
                "title": "En Stock",
                "icon": "🏪",
                "color": config.COLORS["neutral"],
                "value_fn": lambda: self.stats_service.get_general_stats()['in_stock']
            },
            {
                "title": "En Vente",
                "icon": "🔄",
                "color": config.COLORS["warning"],
                "value_fn": lambda: self.stats_service.get_general_stats()['in_sale']
            },
            {
                "title": "Vendus",
                "icon": "✓",
                "color": config.COLORS["success"],
                "value_fn": lambda: self.stats_service.get_general_stats()['sold']
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
                "description": "Retour sur investissement"
            },
            {
                "title": "Bénéfice Moyen",
                "icon": "💎",
                "value": format_currency(self.finance_service.get_average_product_profit()),
                "description": "Par produit vendu"
            },
            {
                "title": "Frais Totaux",
                "icon": "💸",
                "value": format_currency(self.finance_service.get_total_fees()),
                "description": "Tous les frais"
            },
            {
                "title": "Quantité Totale",
                "icon": "📊",
                "value": str(self.stats_service.get_general_stats()['total_quantity']),
                "description": "Articles en possession"
            },
        ]

        for idx, item in enumerate(advanced_data):
            self._create_advanced_card(scroll_frame, idx % 4, 6 + idx // 4, item)

    def _create_kpi_card(self, parent, col, row, data):
        """Crée une carte KPI"""
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10,
            border_width=2,
            border_color=data["color"]
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

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
        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold"),
            text_color=data["color"]
        ).pack(padx=15, pady=10)

    def _create_stat_card(self, parent, col, row, data):
        """Crée une carte de statistique"""
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            card,
            text=data["icon"],
            font=("Arial", 32)
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card,
            text=data["title"],
            font=("Arial", 11),
            text_color=config.COLORS["fg_text_secondary"]
        ).pack()

        value = str(data["value_fn"]())
        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            text_color=data["color"]
        ).pack(pady=10)

    def _create_advanced_card(self, parent, col, row, data):
        """Crée une carte avancée"""
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Icône et titre
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=data["icon"],
            font=("Arial", 20)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text=data["title"],
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["fg_text"]
        ).pack(side="left")

        # Valeur
        ctk.CTkLabel(
            card,
            text=data["value"],
            font=("Arial", 20, "bold"),
            text_color=config.COLORS["accent"]
        ).pack(padx=15, pady=(0, 5))

        # Description
        ctk.CTkLabel(
            card,
            text=data["description"],
            font=("Arial", 10),
            text_color=config.COLORS["fg_text_secondary"]
        ).pack(padx=15, pady=(0, 15))

    def refresh(self):
        """Rafraîchit le dashboard"""
        # Recréer toute l'interface
        for widget in self.winfo_children():
            widget.destroy()
        self._create_ui()
