"""
Page Ajouter un Produit - Interface modernisée
"""
import customtkinter as ctk
from vinted_app.services.product_service import ProductService
from vinted_app import config


class AddProductFrame(ctk.CTkFrame):
    """Frame pour ajouter ou modifier un produit avec interface modernisée"""

    def __init__(self, parent, product_service: ProductService, refresh_callback, edit_product=None):
        """Initialise le formulaire"""
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])

        self.product_service = product_service
        self.refresh_callback = refresh_callback
        self.edit_product = edit_product
        self.is_edit_mode = edit_product is not None

        # Catégories qui nécessitent un PEGI
        self.pegi_categories = ["Jeux vidéo", "Nintendo Switch", "Boîte Switch"]

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_ui()

    def _create_ui(self):
        """Crée l'interface modernisée avec sections claires"""
        # Container principal avec scroll
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=config.COLORS["bg_primary"]
        )
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)

        # Titre principal
        title = ctk.CTkLabel(
            main_container,
            text="➕ Ajouter un Produit",
            font=("Arial", 24, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        title.grid(row=0, column=0, pady=(0, 30), sticky="w")

        # === SECTION 1: INFORMATIONS PRINCIPALES ===
        self._create_section(main_container, "📋 Informations Principales", 1, [
            ("name", "Nom du produit*", "text"),
            ("category", "Catégorie*", "combobox", config.CATEGORIES),
            ("platform", "Plateforme*", "combobox", config.PLATFORMS),
            ("condition", "État*", "combobox", config.CONDITIONS),
            ("status", "Statut initial*", "combobox", list(config.PRODUCT_STATUS.keys())),
        ])

        # === SECTION 2: PRIX ===
        self._create_section(main_container, "💰 Prix & Quantité", 2, [
            ("purchase_price", "Prix d'achat (€)*", "float"),
            ("selling_price", "Prix de vente (€)*", "float"),
            ("fees", "Frais (€)", "float"),
            ("quantity", "Quantité*", "int"),
        ])

        # === SECTION 3: DÉTAILS ===
        self._create_section(main_container, "📝 Détails", 3, [
            ("description", "Description", "textarea"),
        ])

        # Champ PEGI (caché par défaut)
        self.pegi_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.pegi_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        self.pegi_frame.grid_columnconfigure(1, weight=1)
        self.pegi_frame.grid_remove()  # Caché par défaut

        # Label PEGI
        pegi_label = ctk.CTkLabel(
            self.pegi_frame,
            text="🎮 PEGI",
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        pegi_label.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=15)

        # ComboBox PEGI
        self.pegi_var = ctk.StringVar()
        pegi_combo = ctk.CTkComboBox(
            self.pegi_frame,
            values=["3", "7", "12", "16", "18"],
            variable=self.pegi_var,
            fg_color=config.COLORS["bg_secondary"],
            button_color=config.COLORS["accent"],
            dropdown_fg_color=config.COLORS["bg_secondary"],
            border_color=config.COLORS["bg_tertiary"],
            border_width=1,
            width=200
        )
        pegi_combo.set("")
        pegi_combo.grid(row=0, column=1, sticky="w", pady=(10, 5), padx=15)

        # === SECTION 4: CALCULS ET ACTIONS ===
        self._create_actions_section(main_container, 5)

        # Focus automatique sur le premier champ
        if hasattr(self, 'name_entry'):
            self.name_entry.focus()

    def _create_section(self, parent, title, section_row, fields):
        """Crée une section avec titre et champs"""
        # Frame de section
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=15,
            border_width=1,
            border_color=config.COLORS["bg_tertiary"]
        )
        section_frame.grid(row=section_row, column=0, sticky="ew", pady=(0, 20))
        section_frame.grid_columnconfigure((0, 1), weight=1)

        # Titre de section
        section_title = ctk.CTkLabel(
            section_frame,
            text=title,
            font=("Arial", 16, "bold"),
            text_color=config.COLORS["accent"]
        )
        section_title.grid(row=0, column=0, columnspan=2, pady=(20, 15), padx=20, sticky="w")

        # Champs de la section
        for idx, field_info in enumerate(fields, 1):
            if len(field_info) == 3:
                var_name, label, field_type = field_info
                options = None
            else:
                var_name, label, field_type, options = field_info

            self._create_field(section_frame, idx, label, var_name, field_type, options)

    def _create_field(self, parent, row, label, var_name, field_type, options=None):
        """Crée un champ de formulaire stylisé"""
        # Label
        field_label = ctk.CTkLabel(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=config.COLORS["fg_text"]
        )
        field_label.grid(row=row, column=0, sticky="w", pady=(10, 5), padx=20)

        # Variable StringVar
        if not hasattr(self, f"{var_name}_var"):
            setattr(self, f"{var_name}_var", ctk.StringVar())

        # Champ d'entrée
        if field_type == "textarea":
            entry = ctk.CTkTextbox(
                parent,
                height=80,
                fg_color=config.COLORS["bg_primary"],
                border_color=config.COLORS["bg_tertiary"],
                border_width=1,
                scrollbar_button_color=config.COLORS["bg_tertiary"]
            )
            entry.grid(row=row, column=1, sticky="ew", pady=(10, 5), padx=20)
            # Stocker la référence pour récupérer le texte
            setattr(self, f"{var_name}_entry", entry)

        elif field_type == "combobox":
            entry = ctk.CTkComboBox(
                parent,
                values=options,
                variable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_primary"],
                button_color=config.COLORS["accent"],
                dropdown_fg_color=config.COLORS["bg_secondary"],
                border_color=config.COLORS["bg_tertiary"],
                border_width=1
            )
            # Ouvrir au clic sur toute la zone
            entry.bind("<Button-1>", lambda e: entry.event_generate("<<ComboboxSelected>>") or entry.focus())
            entry.grid(row=row, column=1, sticky="ew", pady=(10, 5), padx=20)

            # Binding spécial pour la catégorie (gestion PEGI)
            if var_name == "category":
                # Utiliser trace pour détecter les changements
                getattr(self, f"{var_name}_var").trace("w", lambda *args: self._on_category_change(getattr(self, f"{var_name}_var").get()))

        else:
            entry = ctk.CTkEntry(
                parent,
                textvariable=getattr(self, f"{var_name}_var"),
                fg_color=config.COLORS["bg_primary"],
                border_color=config.COLORS["bg_tertiary"],
                border_width=1,
                placeholder_text=label.replace("*", "")
            )
            entry.grid(row=row, column=1, sticky="ew", pady=(10, 5), padx=20)

        # Stocker la référence
        setattr(self, f"{var_name}_entry", entry)

    def _create_actions_section(self, parent, section_row):
        """Crée la section des calculs et actions"""
        actions_frame = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_secondary"],
            corner_radius=15,
            border_width=1,
            border_color=config.COLORS["bg_tertiary"]
        )
        actions_frame.grid(row=section_row, column=0, sticky="ew", pady=(0, 20))
        actions_frame.grid_columnconfigure(0, weight=1)

        # Titre
        actions_title = ctk.CTkLabel(
            actions_frame,
            text="📊 Calculs & Actions",
            font=("Arial", 16, "bold"),
            text_color=config.COLORS["accent"]
        )
        actions_title.grid(row=0, column=0, pady=(20, 15), padx=20, sticky="w")

        # Calcul du bénéfice
        calc_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        calc_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        calc_frame.grid_columnconfigure(1, weight=1)

        calc_btn = ctk.CTkButton(
            calc_frame,
            text="📊 Calculer Bénéfice Estimé",
            command=self._calculate_profit,
            fg_color=config.COLORS["info"],
            hover_color="#0891B2",
            font=("Arial", 11, "bold"),
            height=40,
            corner_radius=8
        )
        calc_btn.grid(row=0, column=0, sticky="w", pady=5)

        # Label pour le bénéfice
        self.profit_label = ctk.CTkLabel(
            calc_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color=config.COLORS["accent"]
        )
        self.profit_label.grid(row=0, column=1, sticky="w", pady=5, padx=(20, 0))

        # Label de feedback
        self.feedback_label = ctk.CTkLabel(
            actions_frame,
            text="",
            font=("Arial", 11),
            text_color=config.COLORS["success"]
        )
        self.feedback_label.grid(row=2, column=0, sticky="w", pady=(5, 15), padx=20)

        # Boutons d'action
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        buttons_frame.grid_columnconfigure((0, 1), weight=1, uniform="button")

        # Bouton Réinitialiser
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Réinitialiser",
            command=self._reset_form,
            fg_color=config.COLORS["bg_tertiary"],
            hover_color=config.COLORS["bg_hover"],
            text_color=config.COLORS["fg_text"],
            font=("Arial", 11, "bold"),
            height=45,
            corner_radius=10
        )
        reset_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Bouton Ajouter
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="✓ Ajouter Produit",
            command=self._add_product,
            fg_color=config.COLORS["success"],
            hover_color="#059669",
            font=("Arial", 12, "bold"),
            height=45,
            corner_radius=10
        )
        add_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    def _on_category_change(self, choice):
        """Gère le changement de catégorie pour afficher/cacher PEGI"""
        print(f"[DEBUG] Changement de catégorie: '{choice}', PEGI categories: {self.pegi_categories}")
        if not choice or choice == "":
            return
        if choice in self.pegi_categories:
            print("[DEBUG] Affichage du champ PEGI")
            self.pegi_frame.grid()
        else:
            print("[DEBUG] Masquage du champ PEGI")
            self.pegi_frame.grid_remove()
            self.pegi_var.set("")

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
            print("[DEBUG] Début ajout de produit")
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

            # Récupérer description et PEGI
            description = self.description_entry.get("1.0", "end").strip()
            pegi_str = self.pegi_var.get()
            pegi = int(pegi_str) if pegi_str and pegi_str.isdigit() else None

            print(f"[DEBUG] Création produit: {name}, catégorie: {category}, PEGI: {pegi}")

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
                notes="",  # Plus utilisé, remplacé par description
                description=description
            )

            print(f"[DEBUG] Produit créé avec ID: {product_id}")

            # Mettre à jour le PEGI si nécessaire
            if pegi is not None:
                print(f"[DEBUG] Mise à jour PEGI: {pegi}")
                self.product_service.update_product(product_id, pegi=pegi)

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
        # Réinitialiser tous les champs
        for attr_name in dir(self):
            if attr_name.endswith('_var') and hasattr(self, attr_name):
                var = getattr(self, attr_name)
                if hasattr(var, 'set'):
                    var.set("")

        # Réinitialiser les textareas
        if hasattr(self, 'description_entry'):
            self.description_entry.delete("1.0", "end")

        # Cacher PEGI
        self.pegi_frame.grid_remove()
        self.pegi_var.set("")

        # Effacer les labels
        self.profit_label.configure(text="")
        self.feedback_label.configure(text="")

        # Focus sur le premier champ
        if hasattr(self, 'name_entry'):
            self.name_entry.focus()

    def refresh(self):
        """Rafraîchit le formulaire"""
        pass
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
