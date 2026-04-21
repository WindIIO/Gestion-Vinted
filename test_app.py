#!/usr/bin/env python
"""Test script pour vérifier que l'application fonctionne"""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test des imports
    from vinted_app.database.db import DatabaseManager
    from vinted_app.database.models import Product
    from vinted_app.services.product_service import ProductService
    from vinted_app.services.finance_service import FinanceService
    from vinted_app.services.stats_service import StatsService
    from vinted_app.utils.helpers import format_currency
    
    print("✓ Tous les imports réussis!")
    
    # Test création de la DB
    db = DatabaseManager()
    print("✓ Base de données initialisée!")
    
    # Test des services
    product_service = ProductService(db)
    finance_service = FinanceService(db)
    stats_service = StatsService(db)
    print("✓ Tous les services créés!")
    
    # Ajouter les données de test
    db.add_sample_data()
    print("✓ Données de test ajoutées!")
    
    # Tester quelques fonctions
    all_products = product_service.get_all_products()
    print(f"✓ {len(all_products)} produits trouvés")
    
    total_profit = finance_service.get_total_profit()
    print(f"✓ Bénéfice total calculé: {format_currency(total_profit)}")
    
    stats = stats_service.get_general_stats()
    print(f"✓ Stats: {stats['total_products']} produits au total")
    
    print("\n" + "="*50)
    print("✅ TEST COMPLÈTEMENT RÉUSSI!")
    print("="*50)
    print("\nLancez: python vinted_app\\main.py")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
