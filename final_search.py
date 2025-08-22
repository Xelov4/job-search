#!/usr/bin/env python3
"""
Script final pour la recherche d'emplois SEO à Paris avec tous les détails
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

def format_timestamp(timestamp):
    """Convertit un timestamp en date lisible"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp / 1000).strftime('%d/%m/%Y %H:%M')
        except:
            return "Date inconnue"
    return "Date inconnue"

def search_seo_jobs_paris():
    """Recherche d'emplois SEO à Paris avec tous les détails"""
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
            
            # Essayer de récupérer plus d'informations via l'API
            if 'entityUrn' in job:
                try:
                    # Extraire l'ID de l'emploi
                    job_id = job['entityUrn'].split(':')[-1]
                    
                    # Récupérer les détails complets
                    job_details = linkedin.get_job(job_id)
                    
                    if job_details and isinstance(job_details, dict):
                        # Informations de base
                        company = job_details.get('companyName') or job_details.get('company', {}).get('name', 'N/A')
                        location = job_details.get('formattedLocation') or job_details.get('location', 'N/A')
                        job_type = job_details.get('employmentStatus') or job_details.get('jobType', 'N/A')
                        experience = job_details.get('experienceLevel') or job_details.get('seniorityLevel', 'N/A')
                        
                        print(f"   Entreprise: {company}")
                        print(f"   Localisation: {location}")
                        print(f"   Type: {job_type}")
                        print(f"   Expérience: {experience}")
                        
                        # Description
                        description = job_details.get('description', '')
                        if description:
                            print(f"   Description: {description[:150]}...")
                        
                        # Compétences
                        skills = job_details.get('skills', [])
                        if skills:
                            print(f"   Compétences: {', '.join(skills[:5])}")
                        
                        # Date de publication
                        listed_at = job_details.get('listedAt')
                        if listed_at:
                            print(f"   Publié le: {format_timestamp(listed_at)}")
                        
                    else:
                        print(f"   ⚠️  Détails non disponibles")
                        
                except Exception as e:
                    print(f"   ⚠️  Erreur lors de la récupération des détails: {str(e)[:50]}...")
            
            print("-" * 70)
        
        # Sauvegarder les résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"seo_jobs_paris_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats sauvegardés dans '{filename}'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_seo_jobs_paris()
