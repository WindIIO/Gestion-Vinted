"""
Configuration générale de l'application Vinted Stock Manager
"""

# ====== CONFIGURATION D'APPARENCE ======
COLORS = {
    "bg_primary": "#1a1a1a",      # Noir foncé
    "bg_secondary": "#2d2d2d",    # Gris foncé
    "bg_tertiary": "#3d3d3d",     # Gris moyen
    "fg_text": "#ffffff",          # Blanc
    "fg_text_secondary": "#b0b0b0", # Gris clair
    "accent": "#0066FF",           # Bleu
    "success": "#22C55E",          # Vert (vendu)
    "warning": "#F59E0B",          # Orange (en vente)
    "info": "#3B82F6",             # Bleu info
    "danger": "#EF4444",           # Rouge
    "neutral": "#6B7280"           # Gris neutre (stock)
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
    "VENDU": "Vendu"
}

# ====== CATEGORIES ======
CATEGORIES = [
    "Vêtements",
    "Chaussures",
    "Accessoires",
    "Électronique",
    "Livres",
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
        "notes": "Bleu classique, taille M"
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
        "notes": "Blanc cassé"
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
        "notes": "Authentique, avec certificat"
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
        "notes": "Rare"
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
        "notes": "Noir et blanc"
    }
]
