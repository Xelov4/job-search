#!/usr/bin/env python3
"""
Script de test pour explorer tous les champs disponibles via l'API LinkedIn
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv('config/.env')

def test_single_job_extraction():
    """Test d'extraction complète d'un seul emploi pour analyser tous les champs"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=True
    )
    
    print("🔍 TEST D'EXTRACTION COMPLÈTE - UN SEUL EMPLOI")
    print("=" * 60)
    
    try:
        # Recherche d'un seul emploi pour test
        print("🔍 Phase 1: Recherche d'1 emploi...")
        jobs = linkedin.search_jobs(
            keywords="Product Manager",
            location="Paris, France", 
            limit=1
        )
        
        if not jobs:
            print("❌ Aucun emploi trouvé")
            return
        
        job = jobs[0]
        print(f"✅ Emploi trouvé: {job.get('title', 'N/A')}")
        
        print(f"\n📋 BASIC_INFO FIELDS:")
        for key, value in job.items():
            print(f"   {key}: {type(value).__name__} = {str(value)[:100]}...")
        
        # Extraction des détails complets
        print(f"\n🔍 Phase 2: Extraction détails complets...")
        if 'entityUrn' in job:
            job_id = job['entityUrn'].split(':')[-1]
            job_details = linkedin.get_job(job_id)
            
            if job_details:
                print(f"✅ Détails extraits!")
                print(f"\n📋 DETAILED_INFO FIELDS:")
                
                def explore_nested_structure(obj, prefix="", max_depth=4, current_depth=0):
                    """Explore la structure imbriquée récursivement"""
                    if current_depth > max_depth:
                        return
                    
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            full_key = f"{prefix}.{key}" if prefix else key
                            
                            if isinstance(value, dict):
                                print(f"   {full_key}: dict ({len(value)} keys)")
                                if current_depth < max_depth:
                                    explore_nested_structure(value, full_key, max_depth, current_depth + 1)
                            elif isinstance(value, list):
                                print(f"   {full_key}: list ({len(value)} items)")
                                if value and current_depth < max_depth:
                                    print(f"   {full_key}[0]: {type(value[0]).__name__}")
                                    if isinstance(value[0], dict):
                                        explore_nested_structure(value[0], f"{full_key}[0]", max_depth, current_depth + 1)
                            else:
                                value_str = str(value)[:100]
                                print(f"   {full_key}: {type(value).__name__} = {value_str}...")
                    
                explore_nested_structure(job_details)
                
                # Sauvegarde pour analyse
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data/exports/api_fields_test_{timestamp}.json"
                
                test_data = {
                    'timestamp': datetime.now().isoformat(),
                    'basic_info': job,
                    'detailed_info': job_details,
                    'field_analysis': {
                        'basic_fields_count': len(job),
                        'detailed_fields_count': len(job_details) if job_details else 0
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(test_data, f, indent=2, ensure_ascii=False, default=str)
                
                print(f"\n💾 Test sauvegardé: {filename}")
                
                return job_details
                
        else:
            print("❌ Pas d'entityUrn trouvé")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_single_job_extraction()