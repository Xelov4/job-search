#!/usr/bin/env python3
"""
Test simplifié import WTJ vers Supabase
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .fast_scraper import scrape_wtj_fast
from supabase_client import SimpleJobManager, JobOfferData as SupabaseJobOfferData

async def test_wtj_db_import():
    """Test d'import simplifié WTJ"""
    print("🧪 Test import WTJ vers Supabase")
    print("=" * 40)
    
    # 1. Scraping limité à 5 jobs
    jobs = await scrape_wtj_fast("SEO", "Île-de-France", 1)  # 1 page seulement
    jobs = jobs[:5]  # Limiter à 5 jobs pour le test
    
    print(f"📋 Jobs à tester: {len(jobs)}")
    
    if not jobs:
        print("❌ Aucun job trouvé")
        return False
    
    # 2. Test connexion Supabase
    try:
        client = SimpleJobManager()
        print("✅ Connexion Supabase OK")
    except Exception as e:
        print(f"❌ Connexion Supabase échoué: {e}")
        return False
    
    # 3. Test import 1 job
    job = jobs[0]
    print(f"\n🔄 Test import job: '{job.title}' chez '{job.company_name}'")
    
    try:
        # Convertir vers format Supabase
        supabase_job = SupabaseJobOfferData(
            source_platform="welcometothejungle",
            source_id=f"test_wtj_{job.source_id}",
            source_url=job.source_url,
            title=job.title or "Test SEO Job",
            company_name=job.company_name or "Test Company",
            company_url=None,
            location=job.location or "France",
            description=job.description or "Test job from WTJ scraper",
            work_mode=job.work_mode,
            job_type="full-time",
            application_url=job.application_url,
            salary_info=job.salary_info,
            posted_at=None,
            priority=0,
            notes="Test import WTJ"
        )
        
        success, message = client.save_job(supabase_job)
        
        if success:
            print("✅ Import réussi!")
            print(f"📝 Message: {message}")
        else:
            print("⚠️ Import échoué ou doublon")
            print(f"📝 Message: {message}")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur import: {str(e)}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_wtj_db_import())
    print(f"\n🎯 Résultat: {'✅ SUCCÈS' if result else '❌ ÉCHEC'}")