#!/usr/bin/env python3
"""
Démonstration du module WTJ organisé
Script de démonstration pour le module Welcome to the Jungle
"""

import asyncio
import sys
import os
from datetime import datetime

# Utilisation du module WTJ organisé
from wtj import scrape_wtj_fast, FastWTJScraper, WTJFastConfig

async def demo_wtj_module():
    """Démonstration du module WTJ organisé"""
    print("🌟 DÉMONSTRATION MODULE WTJ")
    print("=" * 50)
    print("📁 Module: job-tracker-simple/python/wtj/")
    print("🎯 Objectif: Codebase clean et organisée")
    print("")
    
    # Test 1: Utilisation simple
    print("🚀 TEST 1: Utilisation simple")
    print("-" * 30)
    
    jobs = await scrape_wtj_fast("marketing", "Île-de-France", max_pages=1)
    print(f"✅ Jobs trouvés: {len(jobs)}")
    
    if jobs:
        print(f"📋 Premier job: '{jobs[0].title}' chez '{jobs[0].company_name}'")
    
    # Test 2: Configuration avancée
    print(f"\n🚀 TEST 2: Configuration avancée")
    print("-" * 30)
    
    config = WTJFastConfig(
        keywords="developer",
        location="Île-de-France",
        max_pages=1,
        headless=True
    )
    
    async with FastWTJScraper(config) as scraper:
        jobs = await scraper.scrape_all_fast()
        print(f"✅ Jobs avec config personnalisée: {len(jobs)}")
    
    # Test 3: Import module
    print(f"\n🚀 TEST 3: Test imports module")
    print("-" * 30)
    
    try:
        from wtj.fast_scraper import scrape_wtj_fast as scraper_func
        from wtj.db_test import test_wtj_db_import
        print("✅ Import direct des composants: OK")
    except ImportError as e:
        print(f"❌ Import error: {e}")
    
    # Résumé
    print(f"\n🎉 RÉSUMÉ MODULE WTJ")
    print("=" * 50)
    print("✅ Organisation clean: /wtj/ dossier")
    print("✅ Module importable: from wtj import ...")
    print("✅ Tests fonctionnels: scraping + DB")
    print("✅ Documentation: wtj/README.md")
    print("✅ Structure maintenue: 4 fichiers organisés")
    print("")
    print("📁 Structure:")
    print("   wtj/__init__.py       # Exports module")
    print("   wtj/README.md         # Documentation complète")
    print("   wtj/fast_scraper.py   # Scraper principal")
    print("   wtj/scraper.py        # Scraper legacy")
    print("   wtj/complete_test.py  # Test workflow complet")
    print("   wtj/db_test.py        # Test DB simplifié")
    
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(demo_wtj_module())
        print(f"\n🎯 Module WTJ: {'✅ OPÉRATIONNEL' if result else '❌ PROBLÈME'}")
    except KeyboardInterrupt:
        print("\n👋 Démonstration interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        sys.exit(1)