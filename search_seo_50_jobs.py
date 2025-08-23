#!/usr/bin/env python3
"""
Recherche SEO avec géolocalisation Île-de-France - 50 emplois
"""
import sys
sys.path.insert(0, 'src')

from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

load_dotenv('config/.env')

def search_seo_50_jobs():
    """Recherche SEO à Paris, Île-de-France, France - 50 emplois"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 RECHERCHE SEO - PARIS, ÎLE-DE-FRANCE - 50 EMPLOIS")
    print("📋 Mot-clé: SEO")
    print("🌍 Localisation: Paris, Île-de-France, France")
    print("📊 Objectif: 50 emplois")
    print("=" * 80)
    
    try:
        # Recherche avec 50 emplois
        jobs = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, Île-de-France, France", 
            limit=50
        )
        
        if jobs:
            print(f"✅ {len(jobs)} emplois trouvés")
            
            # Analyse rapide
            seo_in_title = 0
            interesting_titles = []
            
            for job in jobs:
                title = job.get('title', '').lower()
                if any(term in title for term in ['seo', 'référenceur', 'search engine']):
                    seo_in_title += 1
                    interesting_titles.append(job.get('title', ''))
            
            print(f"🎯 SEO direct dans titres: {seo_in_title}/{len(jobs)} ({seo_in_title/len(jobs)*100:.1f}%)")
            
            # Afficher premiers titres pertinents
            if interesting_titles:
                print(f"\n📋 Titres avec SEO:")
                for title in interesting_titles[:10]:  # Plus de titres pertinents
                    print(f"   • {title}")
            
            # Afficher tous les titres pour analyse
            print(f"\n📋 TOUS LES TITRES TROUVÉS ({len(jobs)} emplois):")
            for i, job in enumerate(jobs, 1):
                title = job.get('title', 'N/A')
                company = job.get('companyName', 'N/A')
                print(f"{i:2d}. {title} - {company}")
            
            # Sauvegarde
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/exports/seo_50_jobs_{timestamp}.json"
            
            save_data = {
                'timestamp': datetime.now().isoformat(),
                'search_params': {
                    'keywords': 'SEO',
                    'location': 'Paris, Île-de-France, France',
                    'limit': 50
                },
                'results': {
                    'total_jobs': len(jobs),
                    'seo_in_title': seo_in_title,
                    'effectiveness': seo_in_title / len(jobs) * 100,
                    'jobs': jobs
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n💾 Résultats sauvegardés: {filename}")
            print(f"📊 Statistiques finales:")
            print(f"   • Total emplois: {len(jobs)}")
            print(f"   • SEO dans titres: {seo_in_title}")
            print(f"   • Efficacité: {seo_in_title/len(jobs)*100:.1f}%")
            
            return jobs
            
        else:
            print("❌ Aucun résultat trouvé")
            return []
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    results = search_seo_50_jobs()
