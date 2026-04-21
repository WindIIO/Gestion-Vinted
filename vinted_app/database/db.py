"""
Gestion de la base de données SQLite
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from .models import Product
from vinted_app import config


class DatabaseManager:
    """Gestionnaire de base de données"""

    def __init__(self, db_path: str = config.DATABASE_PATH):
        """Initialise le gestionnaire de base de données"""
        self.db_path = db_path
        self._create_data_directory()
        self._init_database()

    def _create_data_directory(self):
        """Crée le répertoire de données s'il n'existe pas"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)

    def _init_database(self):
        """Initialise la base de données et crée les tables si nécessaire"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Création de la table products
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                platform TEXT,
                condition TEXT,
                purchase_price REAL,
                selling_price REAL,
                fees REAL,
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'STOCK',
                date_added TEXT,
                date_sold TEXT,
                notes TEXT,
                description TEXT DEFAULT '',
                pegi INTEGER,
                image_path TEXT
            )
        ''')

        # Migration : ajouter les colonnes si elles n'existent pas
        self._migrate_database(cursor)

        conn.commit()
        conn.close()

    def _migrate_database(self, cursor):
        """Migre la base de données pour ajouter les nouvelles colonnes"""
        # Vérifier et ajouter la colonne description
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'description' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN description TEXT DEFAULT ''")
        
        if 'pegi' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN pegi INTEGER")

    def _get_connection(self) -> sqlite3.Connection:
        """Obtient une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ====== PRODUITS ======

    def add_product(self, product: Product) -> int:
        """Ajoute un produit à la base de données"""
        conn = self._get_connection()
        cursor = conn.cursor()

        product.date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO products (name, category, platform, condition,
                                purchase_price, selling_price, fees, quantity,
                                status, date_added, notes, description, pegi, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.name,
            product.category,
            product.platform,
            product.condition,
            product.purchase_price,
            product.selling_price,
            product.fees,
            product.quantity,
            product.status,
            product.date_added,
            product.notes,
            product.description,
            product.pegi,
            product.image_path
        ))

        product_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return product_id

    def get_all_products(self) -> List[Product]:
        """Récupère tous les produits"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        conn.close()

        products = [Product.from_dict(dict(row)) for row in rows]
        return products

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par son ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Product.from_dict(dict(row))
        return None

    def get_products_by_status(self, status: str) -> List[Product]:
        """Récupère tous les produits avec un statut spécifique"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products WHERE status = ?', (status,))
        rows = cursor.fetchall()
        conn.close()

        products = [Product.from_dict(dict(row)) for row in rows]
        return products

    def update_product(self, product: Product) -> bool:
        """Met à jour un produit"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE products
            SET name = ?, category = ?, platform = ?, condition = ?,
                purchase_price = ?, selling_price = ?, fees = ?, quantity = ?,
                status = ?, date_sold = ?, notes = ?, description = ?, pegi = ?, image_path = ?
            WHERE id = ?
        ''', (
            product.name,
            product.category,
            product.platform,
            product.condition,
            product.purchase_price,
            product.selling_price,
            product.fees,
            product.quantity,
            product.status,
            product.date_sold,
            product.notes,
            product.description,
            product.pegi,
            product.image_path,
            product.id
        ))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def update_product_status(self, product_id: int, new_status: str) -> bool:
        """Met à jour le statut d'un produit"""
        product = self.get_product_by_id(product_id)
        if product:
            product.status = new_status
            if new_status == "VENDU":
                product.date_sold = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return self.update_product(product)
        return False

    def search_products(self, query: str) -> List[Product]:
        """Recherche des produits par nom ou catégorie"""
        conn = self._get_connection()
        cursor = conn.cursor()

        search_term = f"%{query}%"
        cursor.execute('''
            SELECT * FROM products
            WHERE name LIKE ? OR category LIKE ? OR platform LIKE ?
        ''', (search_term, search_term, search_term))

        rows = cursor.fetchall()
        conn.close()

        products = [Product.from_dict(dict(row)) for row in rows]
        return products

    def add_sample_data(self):
        """Ajoute des données de test à la base de données"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Vérifier si des données existent déjà
        cursor.execute('SELECT COUNT(*) as count FROM products')
        if cursor.fetchone()['count'] > 0:
            conn.close()
            return

        for product_data in config.SAMPLE_PRODUCTS:
            product = Product.from_dict(product_data)
            product.date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if product.status == "VENDU":
                product.date_sold = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO products (name, category, platform, condition,
                                    purchase_price, selling_price, fees, quantity,
                                    status, date_added, date_sold, notes, description, pegi, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product.name,
                product.category,
                product.platform,
                product.condition,
                product.purchase_price,
                product.selling_price,
                product.fees,
                product.quantity,
                product.status,
                product.date_added,
                product.date_sold,
                product.notes,
                product.description,
                product.pegi,
                product.image_path
            ))

        conn.commit()
        conn.close()
