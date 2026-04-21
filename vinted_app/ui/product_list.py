"""
Page Liste des Produits
"""
import customtkinter as ctk
from tkinter import messagebox
from vinted_app.services.product_service import ProductService
from vinted_app.services.finance_service import FinanceService
from vinted_app.database.models import Product
from vinted_app import config
from vinted_app.utils.helpers import format_currency, get_status_color, get_status_label


class ProductListFrame(ctk.CTkFrame):
    """Frame pour la liste des produits"""

    def __init__(self, parent, product_service: ProductService,
                 finance_service: FinanceService, refresh_callback):
        """Initialise la liste des produits"""
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])

        self.product_service = product_service
        self.finance_service = finance_service
        self.refresh_callback = refresh_callback

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Filtres actuels
        self.current_filter = None
        self.current_category_filter = "Toutes les catégories"
        self.search_query = ""

        self._create_ui()

    def _create_ui(self):
        """Crée l'interface"""
        # === BARRE SUPÉRIEURE ===
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="📦 Liste des Produits",
            font=("Arial", 20, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        title.grid(row=0, column=0, sticky="w")

        # Barre de recherche
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="e", padx=(20, 0))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un produit...",
            textvariable=self.search_var,
            width=300,
            fg_color=config.COLORS["bg_secondary"]
        )
        search_entry.pack(side="left", padx=(0, 10))
        self.search_var.trace("w", lambda *args: self.refresh())

        # === FILTRES PAR STATUT ===
        status_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        status_label = ctk.CTkLabel(
            status_filter_frame,
            text="Statut:",
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        status_label.pack(side="left", padx=(0, 10))

        for status, label in [("STOCK", "📦 Stock"), ("EN_VENTE", "🔄 Vente"), ("EN_LIVRAISON", "🚚 Livraison"), ("RESERVE", "⭐ Réservé"), ("VENDU", "✓ Vendu"), (None, "Tous")]:
            btn = ctk.CTkButton(
                status_filter_frame,
                text=label,
                command=lambda s=status: self._set_filter(s),
                fg_color=config.COLORS["bg_secondary"],
                hover_color=config.COLORS["accent"],
                font=("Arial", 9),
                height=30
            )
            btn.pack(side="left", padx=3)

        # === FILTRES PAR CATÉGORIE ===
        category_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        category_filter_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

        category_label = ctk.CTkLabel(
            category_filter_frame,
            text="Catégorie:",
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        category_label.pack(side="left", padx=(0, 10))

        self.category_filter = ctk.CTkComboBox(
            category_filter_frame,
            values=["Toutes les catégories"] + config.CATEGORIES,
            command=self._on_category_filter_change,
            fg_color=config.COLORS["bg_secondary"],
            button_color=config.COLORS["accent"],
            dropdown_fg_color=config.COLORS["bg_secondary"],
            width=220
        )
        self.category_filter.set("Toutes les catégories")
        self.category_filter.pack(side="left", padx=5)

        # === TABLEAU ===
        self.table_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=config.COLORS["bg_primary"]
        )
        self.table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.table_frame.grid_columnconfigure(0, weight=1)

        self._refresh_table()

    def _set_filter(self, status):
        """Change le filtre"""
        self.current_filter = status
        self.refresh()

    def _on_category_filter_change(self, choice):
        """Callback du filtre de catégorie"""
        self.current_category_filter = choice
        self.refresh()

    def _refresh_table(self):
        """Rafraîchit le tableau"""
        # Effacer le tableau
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Récupérer les produits
        if self.current_filter:
            products = self.product_service.get_products_by_status(self.current_filter)
        else:
            products = self.product_service.get_all_products()

        # Appliquer le filtre de catégorie
        if self.current_category_filter != "Toutes les catégories":
            products = [p for p in products if p.category == self.current_category_filter]

        # Appliquer la recherche
        if self.search_query:
            products = [p for p in products if self.search_query.lower() in p.name.lower()]

        # Créer le header du tableau
        header = ctk.CTkFrame(
            self.table_frame,
            fg_color=config.COLORS["bg_tertiary"],
            corner_radius=12
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15), padx=5)
        header.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        headers = ["Nom", "Catégorie", "Prix Achat", "Prix Vente", "Bénéfice", "Statut", "Actions"]
        for idx, h in enumerate(headers):
            ctk.CTkLabel(
                header,
                text=h,
                font=("Arial", 11, "bold"),
                text_color=config.COLORS["fg_text"]
            ).grid(row=0, column=idx, padx=12, pady=12, sticky="w")

        # Créer les lignes
        if not products:
            ctk.CTkLabel(
                self.table_frame,
                text="Aucun produit trouvé",
                font=("Arial", 12),
                text_color=config.COLORS["fg_text_secondary"]
            ).grid(row=1, column=0, pady=30)
        else:
            for idx, product in enumerate(products, 1):
                self._create_product_row(self.table_frame, idx, product)

    def _create_product_row(self, parent, row, product: Product):
        """Crée une ligne de produit stylisée"""
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=10,
            border_width=1,
            border_color=config.COLORS["bg_tertiary"]
        )
        row_frame.grid(row=row, column=0, sticky="ew", pady=6, padx=5)
        row_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Nom du produit
        ctk.CTkLabel(
            row_frame,
            text=product.name,
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        ).grid(row=0, column=0, padx=12, pady=12, sticky="w")

        # Catégorie avec badge
        category_frame = ctk.CTkFrame(
            row_frame,
            fg_color=config.COLORS["bg_tertiary"],
            corner_radius=6
        )
        category_frame.grid(row=0, column=1, padx=6, pady=12, sticky="ew")
        
        ctk.CTkLabel(
            category_frame,
            text=product.category,
            font=("Arial", 10),
            text_color=config.COLORS["fg_text"]
        ).pack(padx=8, pady=4)

        # Prix achat
        ctk.CTkLabel(
            row_frame,
            text=format_currency(product.purchase_price),
            font=("Arial", 10),
            text_color=config.COLORS["fg_text_secondary"]
        ).grid(row=0, column=2, padx=12, pady=12, sticky="w")

        # Prix vente
        ctk.CTkLabel(
            row_frame,
            text=format_currency(product.selling_price),
            font=("Arial", 10),
            text_color=config.COLORS["fg_text_secondary"]
        ).grid(row=0, column=3, padx=12, pady=12, sticky="w")

        # Bénéfice
        profit = product.get_profit()
        profit_color = config.COLORS["success"] if profit >= 0 else config.COLORS["danger"]
        profit_symbol = "+" if profit >= 0 else ""
        ctk.CTkLabel(
            row_frame,
            text=f"{profit_symbol}{format_currency(profit)}",
            font=("Arial", 11, "bold"),
            text_color=profit_color
        ).grid(row=0, column=4, padx=12, pady=12, sticky="w")

        # Statut avec couleur appropriée
        status_label = get_status_label(product.status)
        status_color = get_status_color(product.status)
        status_frame = ctk.CTkFrame(
            row_frame,
            fg_color=status_color,
            corner_radius=6
        )
        status_frame.grid(row=0, column=5, padx=6, pady=12, sticky="ew")

        ctk.CTkLabel(
            status_frame,
            text=status_label,
            font=("Arial", 10, "bold"),
            text_color="white"
        ).pack(padx=10, pady=5)

        # Actions
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=6, padx=12, pady=12, sticky="e")

        # Menu pour changer le statut
        status_options = [s for s in config.PRODUCT_STATUS.keys() if s != product.status]
        if status_options:
            status_menu = ctk.CTkOptionMenu(
                action_frame,
                values=status_options,
                command=lambda status, p=product: self._change_product_status(p, status),
                fg_color=config.COLORS["bg_tertiary"],
                button_color=config.COLORS["accent"],
                dropdown_fg_color=config.COLORS["bg_secondary"],
                font=("Arial", 9),
                height=28,
                width=95
            )
            status_menu.set("Statut")
            status_menu.pack(side="left", padx=3)

        # Bouton supprimer
        btn_delete = ctk.CTkButton(
            action_frame,
            text="✕",
            font=("Arial", 10, "bold"),
            height=28,
            width=28,
            fg_color=config.COLORS["danger"],
            hover_color="#DC2626",
            command=lambda p=product: self._delete_product(p)
        )
        btn_delete.pack(side="left", padx=3)
        
        # Effet hover sur la ligne
        def on_enter(e):
            row_frame.configure(fg_color=config.COLORS["bg_tertiary"])
        def on_leave(e):
            row_frame.configure(fg_color=config.COLORS["bg_secondary"])
        
        row_frame.bind("<Enter>", on_enter)
        row_frame.bind("<Leave>", on_leave)

    def _change_product_status(self, product: Product, new_status: str):
        """Change le statut d'un produit"""
        if self.product_service.change_product_status(product.id, new_status):
            status_label = config.PRODUCT_STATUS.get(new_status, new_status)
            messagebox.showinfo("Succès", f"{product.name} est maintenant {status_label.lower()}!")
            self.refresh()
            self.refresh_callback()
        else:
            messagebox.showerror("Erreur", "Impossible de changer le statut du produit")

    def _mark_as_sold(self, product: Product):
        """Marque un produit comme vendu (compatible avec ancien code)"""
        self._change_product_status(product, "VENDU")

    def _delete_product(self, product: Product):
        """Supprime un produit"""
        if messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {product.name}?"):
            if self.product_service.delete_product(product.id):
                messagebox.showinfo("Succès", f"{product.name} a été supprimé!")
                self.refresh()
                self.refresh_callback()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer le produit")

    def refresh(self):
        """Rafraîchit le tableau"""
        self.search_query = self.search_var.get() if hasattr(self, 'search_var') else ""
        self._refresh_table()
