#!/usr/bin/env python3
"""
Script d'exploration pour analyser toute la structure des données LinkedIn
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
import pprint

# Charger les variables d'environnement
load_dotenv()

def print_nested_structure(data, prefix="", max_depth=10, current_depth=0):
    """Affiche la structure imbriquée de manière récursive"""
    if current_depth > max_depth:
        print(f"{prefix}... (profondeur maximale atteinte)")
        return
        
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{prefix}{key}: {type(value)}")
            if isinstance(value, (dict, list)) and len(str(value)) < 1000:
                print_nested_structure(value, prefix + "  ", max_depth, current_depth + 1)
            elif isinstance(value, str) and len(value) > 100:
                print(f"{prefix}  = '{value[:100]}...'")
            else:
                print(f"{prefix}  = {value}")
    elif isinstance(data, list):
        print(f"{prefix}[Liste de {len(data)} éléments]")
        if data and current_depth < max_depth:
            print(f"{prefix}Exemple du premier élément:")
            print_nested_structure(data[0], prefix + "  ", max_depth, current_depth + 1)

def explore_linkedin_data():
    """Exploration complète des données LinkedIn"""
    try:
        # Initialiser l'API LinkedIn
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=True
        )
        
        print("🔍 EXPLORATION COMPLÈTE DES DONNÉES LINKEDIN")
        print("=" * 80)
        
        # Recherche d'un seul emploi pour exploration détaillée
        search_results = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, France",
            limit=3  # Juste quelques emplois pour l'exploration
        )
        
        if not search_results:
            print("❌ Aucun emploi trouvé")
            return
            
        print(f"✅ {len(search_results)} emplois trouvés pour exploration\n")
        
        # Explorer chaque emploi en détail
        for i, job in enumerate(search_results, 1):
            print(f"\n{'='*60}")
            print(f"📋 EXPLORATION DÉTAILLÉE - EMPLOI {i}")
            print(f"{'='*60}")
            
            # Données de base de search_jobs
            print("\n🔸 DONNÉES DE BASE (search_jobs):")
            print("-" * 40)
            print_nested_structure(job, "  ")
            
            # Récupérer les détails complets
            if 'entityUrn' in job:
                job_id = job['entityUrn'].split(':')[-1]
                print(f"\n🔸 RÉCUPÉRATION DES DÉTAILS COMPLETS (get_job({job_id})):")
                print("-" * 40)
                
                try:
                    job_details = linkedin.get_job(job_id)
                    
                    if job_details:
                        print("\n📊 STRUCTURE COMPLÈTE DES DONNÉES:")
                        print_nested_structure(job_details, "  ")
                        
                        # Sauvegarder un exemple complet
                        if i == 1:  # Premier emploi seulement
                            filename = f"complete_job_data_example_{job_id}.json"
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump({
                                    'basic_data': job,
                                    'detailed_data': job_details
                                }, f, indent=2, ensure_ascii=False)
                            print(f"\n💾 Exemple complet sauvegardé dans '{filename}'")
                    else:
                        print("❌ Aucun détail récupéré")
                        
                except Exception as e:
                    print(f"❌ Erreur lors de la récupération: {e}")
                    
            print("\n" + "="*60 + "\n")
                        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_linkedin_data()