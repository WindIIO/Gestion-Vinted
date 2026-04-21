"""
Service de génération de graphiques pour le dashboard
Utilise matplotlib pour créer des visualisations interactives
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from vinted_app.database.db import DatabaseManager
from vinted_app.database.models import Product


class ChartsService:
    """Service pour la génération de graphiques"""

    def __init__(self, db: DatabaseManager):
        """Initialise le service de graphiques"""
        self.db = db
        # Configure matplotlib pour dark mode
        plt.style.use('dark_background')

    def get_profit_evolution_chart(self) -> Figure:
        """
        Génère un graphique d'évolution du bénéfice au fil du temps
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Récupère tous les produits vendus
        sold_products = self.db.get_products_by_status("VENDU")
        
        if not sold_products:
            ax.text(0.5, 0.5, 'Aucune vente enregistrée', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Évolution du Bénéfice")
            return fig
        
        # Organise les ventes par date
        profits_by_date = {}
        for product in sold_products:
            if product.date_sold:
                date = product.date_sold.split(' ')[0]
                profit = (product.selling_price - product.purchase_price - product.fees) * product.quantity
                if date not in profits_by_date:
                    profits_by_date[date] = 0
                profits_by_date[date] += profit
        
        # Trie par date
        sorted_dates = sorted(profits_by_date.keys())
        cumulative_profit = []
        cumul = 0
        for date in sorted_dates:
            cumul += profits_by_date[date]
            cumulative_profit.append(cumul)
        
        # Affiche le graphique
        ax.plot(sorted_dates, cumulative_profit, marker='o', linewidth=2, markersize=8, color='#22C55E')
        ax.fill_between(range(len(sorted_dates)), cumulative_profit, alpha=0.3, color='#22C55E')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Bénéfice Cumulé (€)", fontsize=12)
        ax.set_title("Évolution du Bénéfice dans le Temps", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        
        return fig

    def get_sales_by_category_chart(self) -> Figure:
        """
        Génère un graphique des ventes par catégorie
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Récupère les ventes par catégorie
        sold_products = self.db.get_products_by_status("VENDU")
        sales_by_category = {}
        
        for product in sold_products:
            if product.category not in sales_by_category:
                sales_by_category[product.category] = 0
            sales_by_category[product.category] += product.selling_price * product.quantity
        
        if not sales_by_category:
            ax.text(0.5, 0.5, 'Aucune vente enregistrée', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Ventes par Catégorie")
            return fig
        
        # Trie par montant
        categories = list(sales_by_category.keys())
        amounts = list(sales_by_category.values())
        
        colors = ['#3B82F6', '#F59E0B', '#22C55E', '#A855F7', '#EC4899', '#14B8A6', '#F97316', '#06B6D4']
        colors = colors[:len(categories)]
        
        bars = ax.bar(categories, amounts, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_ylabel("Montant (€)", fontsize=12)
        ax.set_title("Montant des Ventes par Catégorie", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Ajoute les valeurs sur les barres
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{amount:.0f}€',
                   ha='center', va='bottom', fontsize=10)
        
        fig.autofmt_xdate()
        return fig

    def get_products_distribution_chart(self) -> Figure:
        """
        Génère un graphique de répartition des produits par statut
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Récupère les statistiques
        stats = {
            'STOCK': len(self.db.get_products_by_status('STOCK')),
            'EN_VENTE': len(self.db.get_products_by_status('EN_VENTE')),
            'VENDU': len(self.db.get_products_by_status('VENDU')),
            'EN_LIVRAISON': len(self.db.get_products_by_status('EN_LIVRAISON')),
            'RESERVE': len(self.db.get_products_by_status('RESERVE')),
        }
        
        # Filtre les statuts avec 0 produit
        stats = {k: v for k, v in stats.items() if v > 0}
        
        if not stats:
            ax.text(0.5, 0.5, 'Aucun produit', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Distribution des Produits")
            return fig
        
        labels_map = {
            'STOCK': 'En Stock',
            'EN_VENTE': 'En Vente',
            'VENDU': 'Vendu',
            'EN_LIVRAISON': 'En Livraison',
            'RESERVE': 'Réservé'
        }
        
        labels = [labels_map[k] for k in stats.keys()]
        sizes = list(stats.values())
        colors = ['#6B7280', '#F59E0B', '#22C55E', '#3B82F6', '#A855F7']
        colors = colors[:len(labels)]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                           startangle=90, textprops={'fontsize': 10})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title("Distribution des Produits par Statut", fontsize=14, fontweight='bold', pad=20)
        
        return fig

    def get_profit_by_category_chart(self) -> Figure:
        """
        Génère un graphique du profit par catégorie
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Récupère le profit par catégorie
        sold_products = self.db.get_products_by_status("VENDU")
        profit_by_category = {}
        
        for product in sold_products:
            if product.category not in profit_by_category:
                profit_by_category[product.category] = 0
            profit = (product.selling_price - product.purchase_price - product.fees) * product.quantity
            profit_by_category[product.category] += profit
        
        if not profit_by_category:
            ax.text(0.5, 0.5, 'Aucune vente enregistrée', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Profit par Catégorie")
            return fig
        
        # Trie par profit
        categories = list(profit_by_category.keys())
        profits = list(profit_by_category.values())
        
        colors = ['#22C55E' if p >= 0 else '#EF4444' for p in profits]
        
        bars = ax.barh(categories, profits, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_xlabel("Profit (€)", fontsize=12)
        ax.set_title("Profit par Catégorie", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        ax.axvline(x=0, color='white', linestyle='-', linewidth=0.8)
        
        # Ajoute les valeurs sur les barres
        for bar, profit in zip(bars, profits):
            width = bar.get_width()
            label_x_pos = width + (max(profits) * 0.02 if width > 0 else -max(profits) * 0.02)
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2.,
                   f'{profit:.0f}€',
                   va='center', ha='left' if width > 0 else 'right', fontsize=10)
        
        return fig

    def get_roi_evolution_chart(self) -> Figure:
        """
        Génère un graphique de l'évolution du ROI
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Récupère tous les produits vendus
        sold_products = self.db.get_products_by_status("VENDU")
        
        if not sold_products:
            ax.text(0.5, 0.5, 'Aucune vente enregistrée', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Évolution du ROI")
            return fig
        
        # Organise les ventes par date
        sales_by_date = {}
        for product in sold_products:
            if product.date_sold:
                date = product.date_sold.split(' ')[0]
                if date not in sales_by_date:
                    sales_by_date[date] = {'profit': 0, 'invested': 0}
                profit = (product.selling_price - product.purchase_price - product.fees) * product.quantity
                invested = product.purchase_price * product.quantity
                sales_by_date[date]['profit'] += profit
                sales_by_date[date]['invested'] += invested
        
        # Calcule le ROI cumulatif par date
        sorted_dates = sorted(sales_by_date.keys())
        roi_values = []
        cumul_profit = 0
        cumul_invested = 0
        
        for date in sorted_dates:
            cumul_profit += sales_by_date[date]['profit']
            cumul_invested += sales_by_date[date]['invested']
            roi = (cumul_profit / cumul_invested * 100) if cumul_invested > 0 else 0
            roi_values.append(roi)
        
        # Affiche le graphique
        ax.plot(sorted_dates, roi_values, marker='o', linewidth=2.5, markersize=8, color='#0066FF')
        ax.fill_between(range(len(sorted_dates)), roi_values, alpha=0.3, color='#0066FF')
        ax.axhline(y=0, color='white', linestyle='--', linewidth=0.8)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("ROI (%)", fontsize=12)
        ax.set_title("Évolution du ROI (Return on Investment)", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        
        return fig

    def get_monthly_sales_chart(self) -> Figure:
        """
        Génère un graphique des ventes par mois
        Retourne: Figure matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Récupère tous les produits vendus
        sold_products = self.db.get_products_by_status("VENDU")
        
        if not sold_products:
            ax.text(0.5, 0.5, 'Aucune vente enregistrée', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title("Ventes Mensuelles")
            return fig
        
        # Organise les ventes par mois
        sales_by_month = {}
        for product in sold_products:
            if product.date_sold:
                month = product.date_sold[:7]  # Format YYYY-MM
                if month not in sales_by_month:
                    sales_by_month[month] = 0
                sales_by_month[month] += product.selling_price * product.quantity
        
        # Trie par mois
        sorted_months = sorted(sales_by_month.keys())
        amounts = [sales_by_month[m] for m in sorted_months]
        
        bars = ax.bar(sorted_months, amounts, color='#3B82F6', edgecolor='white', linewidth=1.5)
        ax.set_ylabel("Montant (€)", fontsize=12)
        ax.set_title("Ventes Mensuelles", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Ajoute les valeurs sur les barres
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{amount:.0f}€',
                   ha='center', va='bottom', fontsize=10)
        
        fig.autofmt_xdate()
        return fig
