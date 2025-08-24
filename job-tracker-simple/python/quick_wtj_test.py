#!/usr/bin/env python3
"""
Test rapide Welcome to the Jungle avec timeout optimisé
"""

import asyncio
import json
from datetime import datetime
from wtj import scrape_wtj_fast

async def quick_wtj_test():
    """Test optimisé WTJ pour SEO"""
    print("🚀 Test rapide WTJ - Keyword: SEO")
    
    try:
        # Test avec 1 page seulement pour éviter timeout
        jobs = await scrape_wtj_fast(
            keywords="SEO",
            location="Île-de-France",
            max_pages=1  # Une seule page pour éviter timeout
        )
        
        print(f"✅ Scraping terminé: {len(jobs)} jobs trouvés")
        
        # Afficher les résultats
        if jobs:
            print("\n🏆 JOBS WELCOME TO THE JUNGLE:")
            print("=" * 50)
            
            for i, job in enumerate(jobs[:10]):
                print(f"\n📋 Job {i+1}:")
                print(f"  📝 Titre: {job.title}")
                print(f"  🏢 Entreprise: {job.company_name}")
                print(f"  📍 Localisation: {job.location}")
                print(f"  💼 Mode travail: {job.work_mode}")
                print(f"  🔗 URL: {job.source_url[:80]}...")
                print(f"  🆔 Source ID: {job.source_id}")
        
        # Sauvegarder résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/Job/linkedin-mcp/data/exports/wtj_seo_test_{timestamp}.json"
        
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'test_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'keywords': 'SEO',
                    'location': 'Île-de-France',
                    'total_jobs': len(jobs)
                },
                'jobs': [job.__dict__ for job in jobs]
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats sauvegardés: {filename}")
        return jobs
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []

if __name__ == "__main__":
    asyncio.run(quick_wtj_test())