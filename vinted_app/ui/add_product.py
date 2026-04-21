"""
Page Ajouter un Produit
"""
import customtkinter as ctk
from vinted_app.services.product_service import ProductService
from vinted_app import config


class AddProductFrame(ctk.CTkFrame):
    """Frame pour ajouter un produit"""

    def __init__(self, parent, product_service: ProductService, refresh_callback):
        """Initialise le formulaire"""
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])

        self.product_service = product_service
        self.refresh_callback = refresh_callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_ui()

    def _create_ui(self):
        """Crée l'interface du formulaire"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=config.COLORS["bg_primary"],
            label_text="➕ Ajouter un Produit"
        )
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # === FORMULAIRE ===
        self._create_form_field(scroll_frame, 0, "Nom du produit", "name")
        self._create_form_field(scroll_frame, 1, "Catégorie", "category", field_type="combobox", options=config.CATEGORIES)
        self._create_form_field(scroll_frame, 2, "Plateforme", "platform", field_type="combobox", options=config.PLATFORMS)
        self._create_form_field(scroll_frame, 3, "État", "condition", field_type="combobox", options=config.CONDITIONS)
        self._create_form_field(scroll_frame, 4, "Statut initial", "status", field_type="combobox", options=list(config.PRODUCT_STATUS.keys()))
        self._create_form_field(scroll_frame, 5, "Prix d'achat (€)", "purchase_price", field_type="float")
        self._create_form_field(scroll_frame, 6, "Prix de vente (€)", "selling_price", field_type="float")
        self._create_form_field(scroll_frame, 7, "Frais (€)", "fees", field_type="float")
        self._create_form_field(scroll_frame, 8, "Quantité", "quantity", field_type="int")

        # Notes
        notes_label = ctk.CTkLabel(
            scroll_frame,
            text="Notes (optionnel)",
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        notes_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(15, 5), padx=10)

        self.notes_var = ctk.StringVar()
        notes_textbox = ctk.CTkTextbox(
            scroll_frame,
            height=100,
            fg_color=config.COLORS["bg_secondary"],
            scrollbar_button_color=config.COLORS["bg_tertiary"]
        )
        notes_textbox.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)
        notes_textbox.bind("<KeyRelease>", lambda e: self.notes_var.set(notes_textbox.get("1.0", "end")))

        # === BOUTONS ===
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.grid(row=11, column=0, columnspan=2, sticky="ew", pady=30, padx=10)
        button_frame.grid_columnconfigure(0, weight=1)

        # Calculer le bénéfice estimé
        calc_btn = ctk.CTkButton(
            button_frame,
            text="📊 Calculer Bénéfice Estimé",
            command=self._calculate_profit,
            fg_color=config.COLORS["info"],
            hover_color="#0891B2",
            font=("Arial", 11, "bold"),
            height=42,
            corner_radius=8
        )
        calc_btn.grid(row=0, column=0, sticky="ew", pady=8)

        # Label pour le bénéfice
        self.profit_label = ctk.CTkLabel(
            button_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["accent"]
        )
        self.profit_label.grid(row=1, column=0, sticky="w", pady=8)

        # Label pour les messages de feedback
        self.feedback_label = ctk.CTkLabel(
            button_frame,
            text="",
            font=("Arial", 11),
            text_color=config.COLORS["success"]
        )
        self.feedback_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Boutons d'action
        action_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", pady=(25, 0))
        action_frame.grid_columnconfigure((0, 1), weight=1)

        reset_btn = ctk.CTkButton(
            action_frame,
            text="🔄 Réinitialiser",
            command=self._reset_form,
            fg_color=config.COLORS["bg_tertiary"],
            hover_color=config.COLORS["bg_secondary"],
            text_color=config.COLORS["fg_text"],
            font=("Arial", 11, "bold"),
            height=42,
            corner_radius=8
        )
        reset_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        add_btn = ctk.CTkButton(
            action_frame,
            text="✓ Ajouter Produit",
            command=self._add_product,
            fg_color=config.COLORS["success"],
            hover_color="#059669",
            font=("Arial", 11, "bold"),
            height=42,
            corner_radius=8
        )
        add_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    def _create_form_field(self, parent, row, label, var_name, field_type="text", options=None):
        """Crée un champ de formulaire stylisé"""
        # Label
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        ).grid(row=row, column=0, sticky="w", pady=(18, 8), padx=12)

        # Variable StringVar
        if not hasattr(self, f"{var_name}_var"):
            setattr(self, f"{var_name}_var", ctk.StringVar())

        # Champ d'entrée
        if field_type == "combobox":
            entry = ctk.CTkComboBox(
                parent,
                values=options,
                variable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_secondary"],
                button_color=config.COLORS["accent"],
                dropdown_fg_color=config.COLORS["bg_secondary"],
                border_color=config.COLORS["bg_tertiary"],
                border_width=1
            )
            # Permettre l'ouverture du menu en cliquant sur toute la zone
            entry.bind("<Button-1>", lambda e, cb=entry: cb.event_generate("<<ComboboxSelected>>") or cb.focus())
        else:
            entry = ctk.CTkEntry(
                parent,
                textvariable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_secondary"],
                border_color=config.COLORS["bg_tertiary"],
                border_width=1,
                placeholder_text=label
            )

        entry.grid(row=row, column=1, sticky="ew", pady=(18, 8), padx=12)

    def _calculate_profit(self):
        """Calcule le bénéfice estimé"""
        try:
            selling = float(self.selling_price_var.get() or 0)
            purchase = float(self.purchase_price_var.get() or 0)
            fees = float(self.fees_var.get() or 0)

            profit = selling - purchase - fees
            margin = (profit / selling * 100) if selling > 0 else 0

            self.profit_label.configure(
                text=f"💰 Bénéfice estimé: {profit:.2f}€ | Marge: {margin:.2f}%"
            )
        except ValueError:
            self.profit_label.configure(text="⚠ Entrez des chiffres valides")

    def _show_feedback(self, message: str, type_: str = "info"):
        """Affiche un message de feedback temporaire"""
        color_map = {
            "success": config.COLORS["success"],
            "danger": config.COLORS["danger"],
            "warning": config.COLORS["warning"],
            "info": config.COLORS["info"]
        }
        self.feedback_label.configure(text=message, text_color=color_map.get(type_, config.COLORS["fg_text"]))
        # Effacer après 3 secondes
        self.after(3000, lambda: self.feedback_label.configure(text=""))

    def _add_product(self):
        """Ajoute un produit"""
        try:
            # Validation
            name = self.name_var.get().strip()
            if not name:
                self._show_feedback("Veuillez entrer un nom de produit", "danger")
                return

            category = self.category_var.get()
            if not category:
                self._show_feedback("Veuillez sélectionner une catégorie", "danger")
                return

            platform = self.platform_var.get()
            if not platform:
                self._show_feedback("Veuillez sélectionner une plateforme", "danger")
                return

            condition = self.condition_var.get()
            if not condition:
                self._show_feedback("Veuillez sélectionner un état", "danger")
                return

            status = self.status_var.get()
            if not status:
                self._show_feedback("Veuillez sélectionner un statut", "danger")
                return

            # Convertir les prix
            purchase_price = float(self.purchase_price_var.get() or 0)
            selling_price = float(self.selling_price_var.get() or 0)
            fees = float(self.fees_var.get() or 0)
            quantity = int(self.quantity_var.get() or 1)

            if purchase_price < 0 or selling_price < 0 or fees < 0:
                self._show_feedback("Les prix ne peuvent pas être négatifs", "danger")
                return

            # Créer le produit
            product_id = self.product_service.create_product(
                name=name,
                category=category,
                platform=platform,
                condition=condition,
                purchase_price=purchase_price,
                selling_price=selling_price,
                fees=fees,
                quantity=quantity,
                status=status,
                notes=self.notes_var.get()
            )

            if product_id:
                self._show_feedback(f"Produit ajouté avec succès (ID: {product_id})", "success")
                self._reset_form()
                self.refresh_callback()
            else:
                self._show_feedback("Impossible d'ajouter le produit", "danger")

        except ValueError as e:
            self._show_feedback(f"Format invalide: {str(e)}", "danger")
        except Exception as e:
            self._show_feedback(f"Une erreur s'est produite: {str(e)}", "danger")

    def _reset_form(self):
        """Réinitialise le formulaire"""
        self.name_var.set("")
        self.category_var.set("")
        self.platform_var.set("")
        self.condition_var.set("")
        self.status_var.set("STOCK")
        self.purchase_price_var.set("")
        self.selling_price_var.set("")
        self.fees_var.set("")
        self.quantity_var.set("1")
        self.notes_var.set("")
        self.profit_label.configure(text="")
        self.feedback_label.configure(text="")

    def refresh(self):
        """Rafraîchit le formulaire"""
        pass
