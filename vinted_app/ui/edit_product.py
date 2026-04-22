"""
Fenêtre de modification de produit - Architecture propre
"""
import customtkinter as ctk
from vinted_app.services.product_service import ProductService
from vinted_app.database.models import Product
from vinted_app import config


class EditProductWindow(ctk.CTkToplevel):
    """Fenêtre modale pour modifier un produit"""

    def __init__(self, parent, product_service: ProductService, product: Product, refresh_callback):
        """Initialise la fenêtre d'édition"""
        super().__init__(parent)

        self.product_service = product_service
        self.product = product
        self.refresh_callback = refresh_callback

        # Configuration de la fenêtre
        self.title("✏ Modifier un Produit")
        self.geometry("600x700")
        self.resizable(False, False)

        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()

        # Catégories nécessitant un PEGI
        self.pegi_categories = ["Jeux vidéo", "Nintendo Switch", "Boîte Switch"]

        # Variables des champs
        self._init_variables()

        # Interface
        self._create_ui()

        # Pré-remplir les champs
        self._load_product_data()

    def _init_variables(self):
        """Initialise les variables des champs"""
        self.name_var = ctk.StringVar()
        self.category_var = ctk.StringVar()
        self.platform_var = ctk.StringVar()
        self.condition_var = ctk.StringVar()
        self.status_var = ctk.StringVar()
        self.purchase_price_var = ctk.StringVar()
        self.selling_price_var = ctk.StringVar()
        self.fees_var = ctk.StringVar()
        self.quantity_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.pegi_var = ctk.StringVar()

    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color=config.COLORS["bg_primary"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        title = ctk.CTkLabel(
            main_frame,
            text="✏ Modifier un Produit",
            font=("Arial", 20, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        title.pack(pady=(20, 30))

        # Scrollable frame pour le formulaire
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=15
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Champs du formulaire
        self._create_form_fields(scroll_frame)

        # Boutons d'action
        self._create_action_buttons(main_frame)

    def _create_form_fields(self, parent):
        """Crée les champs du formulaire"""
        fields = [
            ("name", "Nom du produit*", "entry"),
            ("category", "Catégorie*", "combobox", config.CATEGORIES),
            ("platform", "Plateforme*", "combobox", config.PLATFORMS),
            ("condition", "État*", "combobox", config.CONDITIONS),
            ("status", "Statut*", "combobox", list(config.PRODUCT_STATUS.keys())),
            ("purchase_price", "Prix d'achat (€)*", "entry"),
            ("selling_price", "Prix de vente (€)*", "entry"),
            ("fees", "Frais (€)", "entry"),
            ("quantity", "Quantité*", "entry"),
            ("description", "Description", "textbox"),
        ]

        for i, field_info in enumerate(fields):
            if len(field_info) == 3:
                var_name, label, field_type = field_info
                options = None
            else:
                var_name, label, field_type, options = field_info

            self._create_field(parent, i, label, var_name, field_type, options)

        # Champ PEGI (caché par défaut)
        self.pegi_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.pegi_frame.pack(fill="x", padx=20, pady=(10, 20))

        pegi_label = ctk.CTkLabel(
            self.pegi_frame,
            text="🎮 PEGI",
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        pegi_label.pack(anchor="w", pady=(10, 5))

        self.pegi_combo = ctk.CTkComboBox(
            self.pegi_frame,
            values=["3", "7", "12", "16", "18"],
            variable=self.pegi_var,
            fg_color=config.COLORS["bg_primary"],
            button_color=config.COLORS["accent"],
            dropdown_fg_color=config.COLORS["bg_secondary"]
        )
        self.pegi_combo.pack(fill="x", pady=(0, 10))

        # Cacher par défaut
        self.pegi_frame.pack_forget()

    def _create_field(self, parent, row, label, var_name, field_type, options=None):
        """Crée un champ de formulaire"""
        # Label
        field_label = ctk.CTkLabel(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        field_label.pack(anchor="w", padx=20, pady=(20 if row == 0 else 10, 5))

        # Champ
        if field_type == "entry":
            entry = ctk.CTkEntry(
                parent,
                textvariable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_primary"],
                border_color=config.COLORS["bg_tertiary"]
            )
            entry.pack(fill="x", padx=20, pady=(0, 10))

        elif field_type == "combobox":
            combo = ctk.CTkComboBox(
                parent,
                values=options,
                variable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_primary"],
                button_color=config.COLORS["accent"],
                dropdown_fg_color=config.COLORS["bg_secondary"]
            )
            combo.pack(fill="x", padx=20, pady=(0, 10))

            # Binding pour la catégorie (gestion PEGI)
            if var_name == "category":
                combo.configure(command=self._on_category_change)

        elif field_type == "textbox":
            textbox = ctk.CTkTextbox(
                parent,
                height=80,
                fg_color=config.COLORS["bg_primary"]
            )
            textbox.pack(fill="x", padx=20, pady=(0, 10))

            # Lier au StringVar
            def update_var(event):
                getattr(self, f"{var_name}_var").set(textbox.get("1.0", "end").strip())
            textbox.bind("<KeyRelease>", update_var)
            setattr(self, f"{var_name}_textbox", textbox)

    def _create_action_buttons(self, parent):
        """Crée les boutons d'action"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Annuler",
            command=self.destroy,
            fg_color=config.COLORS["bg_tertiary"],
            hover_color=config.COLORS["bg_hover"]
        )
        cancel_btn.pack(side="left", padx=(0, 10))

        # Bouton Enregistrer
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Enregistrer",
            command=self._save_product,
            fg_color=config.COLORS["success"],
            hover_color="#059669"
        )
        save_btn.pack(side="right")

    def _load_product_data(self):
        """Charge les données du produit dans les champs"""
        self.name_var.set(self.product.name)
        self.category_var.set(self.product.category)
        self.platform_var.set(self.product.platform)
        self.condition_var.set(self.product.condition)
        self.status_var.set(self.product.status)
        self.purchase_price_var.set(str(self.product.purchase_price))
        self.selling_price_var.set(str(self.product.selling_price))
        self.fees_var.set(str(self.product.fees))
        self.quantity_var.set(str(self.product.quantity))
        self.description_var.set(self.product.description or "")

        # PEGI
        if self.product.pegi:
            self.pegi_var.set(str(self.product.pegi))
            self.pegi_frame.pack(fill="x", padx=20, pady=(10, 20))
        else:
            self.pegi_var.set("")

        # Mettre à jour l'affichage PEGI selon la catégorie
        self._on_category_change(self.product.category)

    def _on_category_change(self, category):
        """Gère le changement de catégorie pour afficher/cacher PEGI"""
        if category in self.pegi_categories:
            self.pegi_frame.pack(fill="x", padx=20, pady=(10, 20))
        else:
            self.pegi_frame.pack_forget()
            self.pegi_var.set("")

    def _save_product(self):
        """Sauvegarde les modifications du produit"""
        try:
            # Validation
            name = self.name_var.get().strip()
            if not name:
                self._show_error("Le nom du produit est obligatoire")
                return

            category = self.category_var.get()
            if not category:
                self._show_error("La catégorie est obligatoire")
                return

            platform = self.platform_var.get()
            if not platform:
                self._show_error("La plateforme est obligatoire")
                return

            condition = self.condition_var.get()
            if not condition:
                self._show_error("L'état est obligatoire")
                return

            status = self.status_var.get()
            if not status:
                self._show_error("Le statut est obligatoire")
                return

            # Conversion des valeurs numériques
            try:
                purchase_price = float(self.purchase_price_var.get() or 0)
                selling_price = float(self.selling_price_var.get() or 0)
                fees = float(self.fees_var.get() or 0)
                quantity = int(self.quantity_var.get() or 1)
            except ValueError:
                self._show_error("Les prix et quantité doivent être des nombres valides")
                return

            if purchase_price < 0 or selling_price < 0 or fees < 0 or quantity < 0:
                self._show_error("Les valeurs numériques ne peuvent pas être négatives")
                return

            # Description et PEGI
            description = self.description_var.get()
            pegi_str = self.pegi_var.get()
            pegi = int(pegi_str) if pegi_str and pegi_str.isdigit() else None

            # Mise à jour du produit
            update_data = {
                "name": name,
                "category": category,
                "platform": platform,
                "condition": condition,
                "purchase_price": purchase_price,
                "selling_price": selling_price,
                "fees": fees,
                "quantity": quantity,
                "status": status,
                "description": description,
                "pegi": pegi
            }

            if self.product_service.update_product(self.product.id, **update_data):
                # Fermer la fenêtre et rafraîchir
                self.destroy()
                self.refresh_callback()
            else:
                self._show_error("Impossible de modifier le produit")

        except Exception as e:
            self._show_error(f"Erreur lors de la sauvegarde: {str(e)}")

    def _show_error(self, message):
        """Affiche un message d'erreur"""
        # Créer une boîte de dialogue simple
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Erreur")
        error_dialog.geometry("300x150")
        error_dialog.transient(self)
        error_dialog.grab_set()

        ctk.CTkLabel(
            error_dialog,
            text="⚠ Erreur",
            font=("Arial", 14, "bold"),
            text_color=config.COLORS["danger"]
        ).pack(pady=10)

        ctk.CTkLabel(
            error_dialog,
            text=message,
            wraplength=250
        ).pack(pady=10)

        ctk.CTkButton(
            error_dialog,
            text="OK",
            command=error_dialog.destroy
        ).pack(pady=10)
