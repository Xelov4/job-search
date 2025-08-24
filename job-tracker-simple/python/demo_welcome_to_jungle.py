#!/usr/bin/env python3
"""
Démonstration du scraper Welcome to the Jungle
Script simple pour tester et démontrer les fonctionnalités
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Ajout du chemin pour imports
sys.path.append(os.path.dirname(__file__))

from welcometothejungle_scraper import scrape_welcome_to_jungle, WTJSearchConfig


async def demo_scraping():
    """Démonstration du scraping Welcome to the Jungle"""
    print("🌟 DÉMONSTRATION WELCOME TO THE JUNGLE SCRAPER")
    print("=" * 60)
    
    # Configuration
    keywords = "SEO"
    location = "Île-de-France"
    
    print(f"🎯 Recherche: '{keywords}' - Localisation: {location}")
    print("📱 Mode: Headless (sans interface graphique)")
    print("📄 Pages: 1 (démonstration)")
    
    try:
        print("\n🚀 Lancement du scraping...")
        
        # Scraping avec paramètres de démo
        jobs = await scrape_welcome_to_jungle(
            keywords=keywords,
            location=location,
            max_pages=1  # Une page pour la démo
        )
        
        print(f"\n✅ Scraping terminé!")
        print(f"📊 Jobs trouvés: {len(jobs)}")
        
        if jobs:
            print(f"\n🏆 JOBS TROUVÉS:")
            print("-" * 40)
            
            for i, job in enumerate(jobs[:10]):  # Maximum 10 pour la démo
                print(f"\n📋 Job #{i+1}:")
                print(f"  📝 Titre: {job.title}")
                print(f"  🏢 Entreprise: {job.company_name}")
                print(f"  📍 Lieu: {job.location}")
                print(f"  💼 Mode: {job.work_mode}")
                print(f"  🔗 URL: {job.source_url[:80]}...")
                if job.description:
                    desc_preview = job.description[:100].replace('\n', ' ')
                    print(f"  📄 Description: {desc_preview}...")
        else:
            print("\n⚠️ Aucun job trouvé pour cette recherche")
            print("💡 Essayez avec des mots-clés plus génériques comme 'developer' ou 'marketing'")
        
        return jobs
        
    except Exception as e:
        print(f"\n❌ Erreur lors du scraping: {str(e)}")
        print("🔧 Vérifiez que Playwright est correctement installé:")
        print("   pip install playwright")
        print("   playwright install chromium")
        return []


async def demo_with_different_keywords():
    """Test avec différents mots-clés"""
    print("\n" + "=" * 60)
    print("🧪 TEST AVEC DIFFÉRENTS MOTS-CLÉS")
    print("=" * 60)
    
    keywords_to_test = [
        "developer",
        "marketing",
        "data analyst",
        "product manager"
    ]
    
    results = {}
    
    for keyword in keywords_to_test:
        print(f"\n🔍 Test: '{keyword}'")
        
        try:
            jobs = await scrape_welcome_to_jungle(
                keywords=keyword,
                location="Île-de-France", 
                max_pages=1
            )
            
            results[keyword] = len(jobs)
            print(f"  ✅ {len(jobs)} jobs trouvés")
            
        except Exception as e:
            results[keyword] = 0
            print(f"  ❌ Erreur: {str(e)}")
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS:")
    print("-" * 30)
    for keyword, count in results.items():
        print(f"  {keyword:15} : {count:3d} jobs")
    
    return results


def save_demo_results(jobs, filename=None):
    """Sauvegarder les résultats de démonstration"""
    if not jobs:
        return
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/Job/linkedin-mcp/data/exports/wtj_demo_{timestamp}.json"
    
    # Créer le répertoire si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Préparer les données
    demo_data = {
        'demo_metadata': {
            'timestamp': datetime.now().isoformat(),
            'source': 'welcometothejungle',
            'demo_mode': True,
            'total_jobs': len(jobs)
        },
        'jobs': [job.__dict__ for job in jobs]  # Convertir en dict
    }
    
    # Sauvegarder
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés: {filename}")


async def interactive_demo():
    """Démonstration interactive"""
    print("\n" + "=" * 60)
    print("🎮 DÉMONSTRATION INTERACTIVE")
    print("=" * 60)
    
    while True:
        print("\nOptions disponibles:")
        print("1. 🔍 Recherche personnalisée")
        print("2. 🧪 Test multi-mots-clés")
        print("3. 🌟 Démo SEO (défaut)")
        print("4. ❌ Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == "1":
            keywords = input("🎯 Mots-clés: ").strip()
            if keywords:
                jobs = await demo_scraping_custom(keywords)
                if jobs:
                    save_demo_results(jobs)
        
        elif choice == "2":
            await demo_with_different_keywords()
        
        elif choice == "3":
            jobs = await demo_scraping()
            if jobs:
                save_demo_results(jobs)
        
        elif choice == "4":
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")


async def demo_scraping_custom(keywords):
    """Scraping avec mots-clés personnalisés"""
    print(f"\n🔍 Recherche personnalisée: '{keywords}'")
    
    try:
        jobs = await scrape_welcome_to_jungle(
            keywords=keywords,
            location="Île-de-France",
            max_pages=2  # 2 pages pour personnalisé
        )
        
        print(f"✅ {len(jobs)} jobs trouvés pour '{keywords}'")
        
        if jobs:
            # Afficher top 5
            for i, job in enumerate(jobs[:5]):
                print(f"\n{i+1}. {job.title} chez {job.company_name}")
                print(f"   📍 {job.location} | 💼 {job.work_mode}")
        
        return jobs
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []


async def main():
    """Menu principal de démonstration"""
    print("🌟 WELCOME TO THE JUNGLE SCRAPER - DÉMONSTRATION")
    print("=" * 60)
    print("Ce script démontre les capacités du scraper Welcome to the Jungle")
    print("intégré au système Job Tracker multi-sources.")
    print("\n⚡ Fonctionnalités:")
    print("- Scraping automatisé avec Playwright")
    print("- Normalisation des données pour Supabase")
    print("- Détection automatique du mode de travail")
    print("- Sauvegarde des résultats en JSON")
    
    mode = input("\n🎮 Mode interactif? (y/N): ").strip().lower()
    
    if mode in ['y', 'yes', 'oui']:
        await interactive_demo()
    else:
        # Mode automatique
        jobs = await demo_scraping()
        if jobs:
            save_demo_results(jobs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        sys.exit(1)