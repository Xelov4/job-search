#!/usr/bin/env python3
"""
Test complet Welcome to the Jungle - avec workflow DB
Equivalent au workflow LinkedIn Enhanced
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from .fast_scraper import scrape_wtj_fast

# Import des modules système - remonter d'un niveau pour accéder aux modules parent
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from supabase_client import SimpleJobManager, JobOfferData as SupabaseJobOfferData

async def test_wtj_complete_workflow():
    """Test complet du workflow WTJ comme LinkedIn"""
    print("🌟 TEST COMPLET WELCOME TO THE JUNGLE")
    print("=" * 60)
    print("📋 Keyword: SEO")
    print("📍 Location: Île-de-France") 
    print("📄 Pages: 2")
    print("")
    
    # Étape 1: Scraping WTJ
    print("🚀 ÉTAPE 1: Scraping Welcome to the Jungle...")
    
    jobs = await scrape_wtj_fast("SEO", "Île-de-France", 2)
    
    print(f"✅ Scraping terminé: {len(jobs)} jobs extraits")
    
    if not jobs:
        print("❌ Aucun job trouvé, arrêt du test")
        return
    
    # Étape 2: Affichage des résultats
    print(f"\n🏆 TOP 10 JOBS WELCOME TO THE JUNGLE:")
    print("-" * 50)
    
    for i, job in enumerate(jobs[:10]):
        print(f"\n📋 Job {i+1}:")
        print(f"  📝 Titre: {job.title}")
        print(f"  🏢 Entreprise: {job.company_name}")
        print(f"  📍 Location: {job.location}")
        print(f"  💼 Mode: {job.work_mode}")
        print(f"  🔗 URL: {job.source_url[:60]}..." if job.source_url else "  🔗 URL: N/A")
        print(f"  🆔 ID: {job.source_id}")
    
    # Étape 3: Sauvegarde JSON (comme LinkedIn Enhanced)
    print(f"\n💾 ÉTAPE 2: Sauvegarde JSON...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = "/root/Job/linkedin-mcp/data/exports"
    json_filename = f"{export_dir}/wtj_seo_jobs_{timestamp}.json"
    
    os.makedirs(export_dir, exist_ok=True)
    
    # Format similaire aux exports LinkedIn
    export_data = {
        'export_metadata': {
            'timestamp': datetime.now().isoformat(),
            'source': 'welcometothejungle_fast_scraper',
            'keywords': 'SEO',
            'location': 'Île-de-France',
            'total_jobs': len(jobs),
            'test_mode': True
        },
        'jobs': [job.__dict__ for job in jobs]
    }
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Export JSON sauvé: {json_filename}")
    
    # Étape 4: Import en base Supabase (comme LinkedIn)
    print(f"\n🗄️ ÉTAPE 3: Import Supabase...")
    
    try:
        supabase_client = SimpleJobManager()
        
        print("📊 État de la base avant import:")
        # Compter manuellement les jobs existants
        try:
            all_jobs = supabase_client.get_jobs_by_status(limit=1000)
            total_before = len(all_jobs) if all_jobs else 0
            wtj_before = len([j for j in (all_jobs or []) if j.get('source_platform') == 'welcometothejungle'])
            print(f"  Total jobs: {total_before}")
            print(f"  WTJ jobs: {wtj_before}")
        except:
            total_before = 0
            wtj_before = 0
            print(f"  Total jobs: N/A (nouvelle base)")
            print(f"  WTJ jobs: N/A")
        
        # Import des jobs
        success_count = 0
        error_count = 0
        duplicate_count = 0
        
        print(f"\n🔄 Import de {len(jobs)} jobs WTJ...")
        
        for i, job in enumerate(jobs):
            try:
                # Convertir vers format Supabase
                supabase_job = SupabaseJobOfferData(
                    source_platform=job.source_platform,
                    source_id=job.source_id,
                    source_url=job.source_url,
                    title=job.title,
                    company_name=job.company_name,
                    company_url=getattr(job, 'company_url', None),
                    location=job.location,
                    description=job.description,
                    work_mode=job.work_mode,
                    job_type=job.job_type,
                    application_url=job.application_url,
                    salary_info=job.salary_info,
                    posted_at=None,  # WTJ ne fournit pas cette info
                    priority=0,
                    notes=None
                )
                
                # Tentative d'insertion
                success, message = supabase_client.save_job(supabase_job)
                if success:
                    success_count += 1
                    if (i + 1) % 10 == 0:
                        print(f"  📈 {i + 1}/{len(jobs)} jobs traités...")
                else:
                    duplicate_count += 1
                    
            except Exception as e:
                error_count += 1
                print(f"  ⚠️ Erreur job {i+1}: {str(e)}")
        
        print(f"\n✅ Import terminé!")
        print(f"  ✅ Succès: {success_count}")
        print(f"  🔄 Doublons ignorés: {duplicate_count}")
        print(f"  ❌ Erreurs: {error_count}")
        
        # État final
        print(f"\n📊 État de la base après import:")
        try:
            all_jobs_after = supabase_client.get_jobs_by_status(limit=1000)
            total_after = len(all_jobs_after) if all_jobs_after else 0
            wtj_after = len([j for j in (all_jobs_after or []) if j.get('source_platform') == 'welcometothejungle'])
            print(f"  Total jobs: {total_after}")
            print(f"  WTJ jobs: {wtj_after}")
            print(f"  🆕 Nouveaux WTJ: {wtj_after - wtj_before}")
        except Exception as e:
            print(f"  État final: Erreur lors du décompte - {str(e)}")
        
        # Étape 5: Vérification finale
        print(f"\n🔍 ÉTAPE 4: Vérification des données importées...")
        
        # Récupérer quelques jobs WTJ récents
        recent_wtj_jobs = supabase_client.get_jobs_by_status(limit=5)
        
        if recent_wtj_jobs:
            print(f"✅ Vérification réussie: {len(recent_wtj_jobs)} jobs WTJ récents trouvés")
            print("\n🎯 Aperçu des jobs importés:")
            for i, job in enumerate(recent_wtj_jobs[:3]):
                print(f"  {i+1}. {job.get('title', 'N/A')} chez {job.get('company_name', 'N/A')}")
        else:
            print("⚠️ Aucun job WTJ trouvé en base")
        
        print(f"\n🎉 WORKFLOW WTJ COMPLET TERMINÉ!")
        print(f"📈 Résultat: {success_count} nouveaux jobs SEO depuis Welcome to the Jungle")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur import Supabase: {str(e)}")
        print("⚠️ Vérifiez la configuration .env")
        return False

if __name__ == "__main__":
    try:
        asyncio.run(test_wtj_complete_workflow())
    except KeyboardInterrupt:
        print("\n👋 Test interrompu")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        sys.exit(1)