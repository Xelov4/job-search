#!/usr/bin/env python3
"""
Script final corrigé pour la recherche d'emplois SEO à Paris avec extraction propre des données
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Charger les variables d'environnement depuis config/
load_dotenv('../../config/.env')

def format_timestamp(timestamp):
    """Convertit un timestamp en date lisible"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp / 1000).strftime('%d/%m/%Y %H:%M')
        except:
            return "Date inconnue"
    return "Date inconnue"

def extract_company_name(company_details):
    """Extrait le nom de l'entreprise de la structure complexe LinkedIn"""
    if not company_details or not isinstance(company_details, dict):
        return 'N/A'
    
    # Navigation dans la structure imbriquée
    for key in company_details:
        if isinstance(company_details[key], dict):
            comp_result = company_details[key].get('companyResolutionResult', {})
            if isinstance(comp_result, dict) and 'name' in comp_result:
                return comp_result['name']
    return 'N/A'

def extract_description_text(description):
    """Extrait le texte brut d'une description LinkedIn formatée"""
    if not description:
        return ""
    
    if isinstance(description, str):
        return description
    
    if isinstance(description, dict) and 'text' in description:
        return description['text']
    
    return ""

def decode_workplace_types(workplace_types):
    """Décode les URNs LinkedIn en types de lieu de travail lisibles"""
    workplace_mapping = {
        'urn:li:fs_workplaceType:1': 'Sur site',
        'urn:li:fs_workplaceType:2': 'Hybride', 
        'urn:li:fs_workplaceType:3': 'Distanciel'
    }
    
    if not workplace_types:
        return 'N/A'
    
    decoded_types = [workplace_mapping.get(wt, wt) for wt in workplace_types]
    return ', '.join(decoded_types)

def search_seo_jobs_paris():
    """Recherche d'emplois SEO à Paris avec extraction propre des données"""
    try:
        # Initialiser l'API LinkedIn
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=False
        )
        
        print("🔍 Recherche d'emplois SEO à Paris, France...")
        print("=" * 70)
        
        # Effectuer la recherche
        search_results = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, France",
            limit=10
        )
        
        if not search_results:
            print("❌ Aucun emploi trouvé avec ces critères.")
            return
        
        print(f"✅ {len(search_results)} emplois trouvés !\n")
        
        # Traiter chaque emploi
        for i, job in enumerate(search_results, 1):
            print(f"📋 **Emploi {i}**")
            print(f"   Titre: {job.get('title', 'N/A')}")
            print(f"   ID: {job.get('entityUrn', 'N/A')}")
            print(f"   Source: {job.get('contentSource', 'N/A')}")
            
            # Récupérer les détails complets
            if 'entityUrn' in job:
                try:
                    job_id = job['entityUrn'].split(':')[-1]
                    job_details = linkedin.get_job(job_id)
                    
                    if job_details and isinstance(job_details, dict):
                        # Entreprise
                        company = extract_company_name(job_details.get('companyDetails', {}))
                        print(f"   Entreprise: {company}")
                        
                        # Localisation
                        location = job_details.get('formattedLocation', 'N/A')
                        print(f"   Localisation: {location}")
                        
                        # Type de lieu de travail
                        workplace_types = job_details.get('workplaceTypes', [])
                        work_type = decode_workplace_types(workplace_types)
                        work_remote = job_details.get('workRemoteAllowed', False)
                        if work_remote and work_type != 'N/A':
                            work_type += ' (Télétravail autorisé)'
                        print(f"   Type: {work_type}")
                        
                        # Description
                        description = extract_description_text(job_details.get('description', ''))
                        if description:
                            if len(description) > 200:
                                print(f"   Description: {description[:200]}...")
                            else:
                                print(f"   Description: {description}")
                        
                        # Date de publication
                        listed_at = job_details.get('listedAt')
                        if listed_at:
                            print(f"   Publié le: {format_timestamp(listed_at)}")
                        
                        # État du job
                        job_state = job_details.get('jobState', 'N/A')
                        if job_state != 'N/A':
                            print(f"   État: {job_state}")
                            
                    else:
                        print(f"   ⚠️  Aucun détail récupéré")
                        
                except Exception as e:
                    print(f"   ⚠️  Erreur lors de la récupération: {str(e)}")
            
            print("-" * 70)
        
        # Sauvegarder les résultats dans data/exports/
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../../data/exports/seo_jobs_paris_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats sauvegardés dans '{filename}'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_seo_jobs_paris()