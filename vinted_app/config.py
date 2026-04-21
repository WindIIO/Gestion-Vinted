"""
Configuration générale de l'application Vinted Stock Manager
"""

# ====== CONFIGURATION D'APPARENCE ======
COLORS = {
    # Backgrounds - Gradient modern dark
    "bg_primary": "#0F1419",       # Noir très foncé (quasi noir)
    "bg_secondary": "#1A1F2E",     # Gris bleu foncé
    "bg_tertiary": "#252D3D",      # Gris bleu moyen
    "bg_hover": "#323D52",         # Hover effect
    
    # Text colors
    "fg_text": "#F8FAFC",          # Blanc pur (ultra clair)
    "fg_text_secondary": "#94A3B8", # Gris clair
    "fg_text_muted": "#64748B",    # Gris moyen
    
    # Status colors - Modern vibrant
    "success": "#10B981",          # Vert émeraude (vendu)
    "warning": "#F59E0B",          # Orange doré (en vente)
    "danger": "#EF4444",           # Rouge vif
    "info": "#06B6D4",             # Cyan
    "accent": "#0EA5E9",           # Bleu ciel moderne
    "neutral": "#6B7280",          # Gris
    
    # Premium colors
    "premium_purple": "#8B5CF6",   # Violet
    "premium_pink": "#EC4899",     # Rose
    "premium_indigo": "#6366F1",   # Indigo
    
    # Statuts spécifiques
    "stock": "#6B7280",            # Gris (stock)
    "en_vente": "#F59E0B",         # Orange
    "vendu": "#10B981",            # Vert
    "en_livraison": "#06B6D4",     # Cyan
    "reserve": "#8B5CF6"           # Violet
}

# ====== STYLES ======
STYLES = {
    "card_border_radius": 12,
    "button_border_radius": 8,
    "sidebar_width": 250,
    "shadow_blur": 20,
    "transition_time": 200  # ms
}

# ====== CONFIGURATION DATABASE ======
DATABASE_PATH = "vinted_app/data/vinted.db"

# ====== CONFIGURATION UI ======
APP_TITLE = "Vinted Stock Manager"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 250

# ====== STATUTS DES PRODUITS ======
PRODUCT_STATUS = {
    "STOCK": "En Stock",
    "EN_VENTE": "En Vente",
    "VENDU": "Vendu",
    "EN_LIVRAISON": "En Livraison",
    "RESERVE": "Réservé"
}

# ====== CATEGORIES ======
CATEGORIES = [
    "Vêtements",
    "Chaussures",
    "Accessoires",
    "Électronique",
    "Livres",
    "Jeux vidéo",
    "Nintendo Switch",
    "Boîte Switch",
    "LEGO",
    "Jouets",
    "Décoration",
    "Autre"
]

# ====== CONDITIONS ======
CONDITIONS = [
    "Neuf",
    "Très bon état",
    "Bon état",
    "Usagé",
    "À restaurer"
]

# ====== PLATEFORME ======
PLATFORMS = [
    "Vinted",
    "Leboncoin",
    "Facebook Marketplace",
    "Autre"
]

# ====== DONNÉES DE TEST ======
SAMPLE_PRODUCTS = [
    {
        "name": "Jean Levi's 501",
        "category": "Vêtements",
        "platform": "Vinted",
        "condition": "Très bon état",
        "purchase_price": 15.0,
        "selling_price": 28.0,
        "fees": 3.5,
        "quantity": 1,
        "status": "EN_VENTE",
        "notes": "Bleu classique, taille M",
        "description": "Jean Levi's 501 authentique, taille M, état très bon avec quelques signes d'usure normale.",
        "pegi": None
    },
    {
        "name": "Nike Air Force 1",
        "category": "Chaussures",
        "platform": "Vinted",
        "condition": "Bon état",
        "purchase_price": 35.0,
        "selling_price": 65.0,
        "fees": 8.0,
        "quantity": 1,
        "status": "VENDU",
        "notes": "Blanc cassé",
        "description": "Sneakers Nike Air Force 1 blanches avec quelques marques d'usure sur les semelles.",
        "pegi": None
    },
    {
        "name": "Louis Vuitton Speedy",
        "category": "Accessoires",
        "platform": "Leboncoin",
        "condition": "Très bon état",
        "purchase_price": 120.0,
        "selling_price": 250.0,
        "fees": 30.0,
        "quantity": 1,
        "status": "STOCK",
        "notes": "Authentique, avec certificat",
        "description": "Sac à main Louis Vuitton Speedy 30 en toile monogramme, authentique avec certificat d'authenticité.",
        "pegi": None
    },
    {
        "name": "T-shirt Vintage Nirvana",
        "category": "Vêtements",
        "platform": "Vinted",
        "condition": "Bon état",
        "purchase_price": 8.0,
        "selling_price": 22.0,
        "fees": 2.5,
        "quantity": 1,
        "status": "STOCK",
        "notes": "Rare",
        "description": "T-shirt vintage Nirvana avec le logo emblématique, état bon avec quelques décolorations.",
        "pegi": None
    },
    {
        "name": "PlayStation 5 Manette",
        "category": "Électronique",
        "platform": "Facebook Marketplace",
        "condition": "Neuf",
        "purchase_price": 45.0,
        "selling_price": 85.0,
        "fees": 10.0,
        "quantity": 2,
        "status": "STOCK",
        "notes": "Noir et blanc",
        "description": "Manette DualSense pour PlayStation 5, neuve sous blister, disponible en noir et blanc.",
        "pegi": None
    },
    {
        "name": "The Legend of Zelda: Breath of the Wild",
        "category": "Jeux vidéo",
        "platform": "Vinted",
        "condition": "Très bon état",
        "purchase_price": 25.0,
        "selling_price": 45.0,
        "fees": 5.5,
        "quantity": 1,
        "status": "EN_VENTE",
        "notes": "Complet avec boîtier",
        "description": "Jeu The Legend of Zelda: Breath of the Wild pour Nintendo Switch, complet avec manuel et boîtier.",
        "pegi": 12
    }
]
