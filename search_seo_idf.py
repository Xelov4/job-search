#!/usr/bin/env python3
"""
Recherche SEO avec géolocalisation Île-de-France
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

def search_seo_idf():
    """Recherche SEO à Paris, Île-de-France, France"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 RECHERCHE SEO - PARIS, ÎLE-DE-FRANCE")
    print("📋 Mot-clé: SEO")
    print("🌍 Localisation: Paris, Île-de-France, France")
    print("=" * 80)
    
    try:
        # Recherche avec la nouvelle localisation
        jobs = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, Île-de-France, France", 
            limit=20
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
                for title in interesting_titles[:5]:
                    print(f"   • {title}")
            
            # Afficher tous les titres pour analyse
            print(f"\n📋 TOUS LES TITRES TROUVÉS:")
            for i, job in enumerate(jobs, 1):
                title = job.get('title', 'N/A')
                print(f"{i:2d}. {title}")
            
            # Sauvegarde
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/exports/seo_idf_{timestamp}.json"
            
            save_data = {
                'timestamp': datetime.now().isoformat(),
                'search_params': {
                    'keywords': 'SEO',
                    'location': 'Paris, Île-de-France, France',
                    'limit': 20
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
            
            return jobs
            
        else:
            print("❌ Aucun résultat trouvé")
            return []
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    results = search_seo_idf()