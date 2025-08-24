#!/usr/bin/env python3
"""
Script de test pour le système multi-sources
Test Welcome to the Jungle + Intégration système existant
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Vérifier les dépendances nécessaires"""
    print("🔧 Vérification des dépendances...")
    
    required_modules = [
        'playwright',
        'supabase',
        'python_dotenv',
        'dataclasses'
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == 'python_dotenv':
                import dotenv
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Modules manquants: {missing}")
        print("Installation requise:")
        print("pip install playwright supabase python-dotenv")
        print("playwright install chromium")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def check_playwright_browsers():
    """Vérifier si les navigateurs Playwright sont installés"""
    print("\n🌐 Vérification des navigateurs Playwright...")
    
    try:
        import subprocess
        result = subprocess.run(['playwright', 'list'], capture_output=True, text=True)
        
        if 'chromium' in result.stdout.lower():
            print("  ✅ Chromium installé")
            return True
        else:
            print("  ❌ Chromium non installé")
            print("Installation requise: playwright install chromium")
            return False
    except Exception as e:
        print(f"  ⚠️ Impossible de vérifier: {str(e)}")
        return False

async def test_welcome_to_jungle_scraper():
    """Test du scraper Welcome to the Jungle"""
    print("\n🌟 Test Welcome to the Jungle Scraper...")
    
    try:
        from welcometothejungle_scraper import scrape_welcome_to_jungle
        
        # Test avec des paramètres limités
        jobs = await scrape_welcome_to_jungle(
            keywords="developer",  # Mot-clé plus général pour avoir des résultats
            location="Île-de-France",
            max_pages=1  # Une seule page pour le test
        )
        
        print(f"✅ Scraper WTJ fonctionne: {len(jobs)} jobs trouvés")
        
        # Afficher quelques exemples
        for i, job in enumerate(jobs[:3]):
            print(f"  📋 Job {i+1}: {job.title} chez {job.company_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test WTJ: {str(e)}")
        return False

def test_supabase_connection():
    """Test de connexion Supabase"""
    print("\n🗄️ Test connexion Supabase...")
    
    try:
        from supabase_client import SupabaseJobClient
        
        client = SupabaseJobClient()
        stats = client.get_database_stats()
        
        print(f"✅ Connexion Supabase OK: {stats['total']} jobs en base")
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion Supabase: {str(e)}")
        print("Vérifiez vos variables d'environnement dans .env")
        return False

def test_linkedin_integration():
    """Test intégration LinkedIn Enhanced"""
    print("\n🔗 Test intégration LinkedIn Enhanced...")
    
    try:
        from linkedin_integration import LinkedInJobNormalizer
        
        # Test avec un job factice
        test_job = {
            'enhanced_info': {
                'job_posting_id': 'test123',
                'title': 'Test SEO Specialist',
                'company': {'name': 'Test Company'},
                'location': {'displayName': 'Paris, France'},
                'description': 'Test job description for SEO role',
                'workplaceTypes': ['remote']
            }
        }
        
        normalized = LinkedInJobNormalizer.normalize_job(test_job)
        
        if normalized:
            print(f"✅ Normalisation LinkedIn OK: {normalized.title}")
            return True
        else:
            print("❌ Échec normalisation LinkedIn")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test LinkedIn: {str(e)}")
        return False

async def test_multi_source_collector():
    """Test du collecteur multi-sources"""
    print("\n🚀 Test collecteur multi-sources...")
    
    try:
        from multi_source_collector import MultiSourceJobCollector, MultiSourceConfig
        
        # Configuration de test
        config = MultiSourceConfig(
            keywords="developer",
            location="Paris, France",
            enable_linkedin=True,  # Utilise les exports existants
            enable_wtj=True,      # Scrape WTJ
            wtj_max_pages=1,      # Limité pour le test
            linkedin_limit=10,    # Limité pour le test
            auto_sync_supabase=False,  # Pas de sync pour le test
            save_raw_results=False     # Pas de sauvegarde pour le test
        )
        
        collector = MultiSourceJobCollector(config)
        
        # Test collecte (sans sync)
        jobs = await collector.collect_from_all_sources()
        
        print(f"✅ Collecteur multi-sources OK: {len(jobs)} jobs collectés")
        collector.print_summary()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test collecteur: {str(e)}")
        return False

async def run_full_test():
    """Lancer la suite complète de tests"""
    print("🧪 SUITE DE TESTS SYSTÈME MULTI-SOURCES")
    print("=" * 60)
    
    tests_results = []
    
    # Tests synchrones
    tests_results.append(("Dependencies", check_dependencies()))
    tests_results.append(("Playwright Browsers", check_playwright_browsers()))
    tests_results.append(("Supabase Connection", test_supabase_connection()))
    tests_results.append(("LinkedIn Integration", test_linkedin_integration()))
    
    # Tests asynchrones
    tests_results.append(("Welcome to the Jungle Scraper", await test_welcome_to_jungle_scraper()))
    tests_results.append(("Multi-Source Collector", await test_multi_source_collector()))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(tests_results)
    
    for test_name, result in tests_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Système prêt.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

async def demo_search():
    """Démonstration d'une recherche complète"""
    print("\n" + "=" * 60)
    print("🎯 DÉMONSTRATION RECHERCHE MULTI-SOURCES")
    print("=" * 60)
    
    try:
        from multi_source_collector import collect_jobs_multi_source
        
        # Recherche de démonstration
        keywords = input("🔍 Mots-clés de recherche (ou Enter pour 'SEO'): ").strip() or "SEO"
        
        print(f"\n🚀 Lancement recherche: '{keywords}'")
        print("Sources activées: LinkedIn Enhanced + Welcome to the Jungle")
        
        jobs = await collect_jobs_multi_source(
            keywords=keywords,
            location="Paris, Île-de-France, France",
            enable_linkedin=True,
            enable_wtj=True,
            linkedin_limit=25,  # Limité pour la démo
            wtj_max_pages=2     # 2 pages WTJ
        )
        
        print(f"\n🎉 Démonstration terminée: {len(jobs)} jobs trouvés et synchronisés!")
        
        # Afficher quelques exemples
        if jobs:
            print("\n🏆 TOP 5 JOBS TROUVÉS:")
            for i, job in enumerate(jobs[:5]):
                print(f"  {i+1}. {job.title} chez {job.company_name}")
                print(f"     📍 {job.location} | 🔗 {job.source_platform}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur démonstration: {str(e)}")
        return False

async def main():
    """Menu principal"""
    while True:
        print("\n" + "=" * 60)
        print("🧪 TEST SYSTÈME MULTI-SOURCES")
        print("=" * 60)
        print("1. 🔧 Tests complets du système")
        print("2. 🎯 Démonstration recherche")
        print("3. ❌ Quitter")
        
        choice = input("\nChoix (1-3): ").strip()
        
        if choice == "1":
            await run_full_test()
        elif choice == "2":
            await demo_search()
        elif choice == "3":
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {str(e)}")
        sys.exit(1)