#!/usr/bin/env python3
"""
Test du script principal avec extraction focalisée
"""
import sys
sys.path.insert(0, 'src')

from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

# Charger les variables d'environnement depuis config/
load_dotenv('config/.env')

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

def extract_employment_type(job_details):
    """Extrait le type de contrat de travail"""
    employment_type = job_details.get('employmentType', 'N/A')
    
    employment_mapping = {
        'FULL_TIME': 'Temps plein',
        'PART_TIME': 'Temps partiel', 
        'CONTRACT': 'Contrat',
        'TEMPORARY': 'Temporaire',
        'VOLUNTEER': 'Bénévolat',
        'INTERNSHIP': 'Stage',
        'FREELANCE': 'Freelance'
    }
    
    return employment_mapping.get(employment_type, employment_type)

def extract_structured_data(job, job_details):
    """Extrait les données structurées demandées: entreprise, description, type contrat, localisation"""
    data = {
        'titre': job.get('title', 'N/A'),
        'id': job.get('entityUrn', 'N/A'),
        'entreprise': 'N/A',
        'description': '',
        'type_contrat': 'N/A',
        'localisation': 'N/A',
        'type_lieu_travail': 'N/A',
        'date_publication': 'N/A'
    }
    
    if job_details and isinstance(job_details, dict):
        # Nom de l'entreprise
        data['entreprise'] = extract_company_name(job_details.get('companyDetails', {}))
        
        # Description complète
        data['description'] = extract_description_text(job_details.get('description', ''))
        
        # Type de contrat
        data['type_contrat'] = extract_employment_type(job_details)
        
        # Localisation
        data['localisation'] = job_details.get('formattedLocation', 'N/A')
        
        # Type de lieu de travail
        workplace_types = job_details.get('workplaceTypes', [])
        data['type_lieu_travail'] = decode_workplace_types(workplace_types)
        
        # Date de publication
        listed_at = job_details.get('listedAt')
        if listed_at:
            data['date_publication'] = format_timestamp(listed_at)
    
    return data

def test_focused_search():
    """Test de la recherche focalisée avec authentification LinkedIn"""
    print("🔍 Test de recherche SEO à Paris avec extraction focalisée...")
    print("📊 Focus: Entreprise | Description | Type contrat | Localisation")
    print("=" * 80)
    
    try:
        # Tentative d'authentification LinkedIn
        print("🔐 Authentification LinkedIn en cours...")
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=False
        )
        print("✅ Authentification réussie!")
        
        # Petite pause pour éviter les limites de taux
        time.sleep(2)
        
        # Effectuer la recherche avec limite réduite pour le test
        print("🔍 Recherche d'emplois SEO...")
        search_results = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, France", 
            limit=5  # Limite réduite pour test rapide
        )
        
        if not search_results:
            print("❌ Aucun emploi trouvé")
            return
        
        print(f"✅ {len(search_results)} emplois trouvés pour le test!\n")
        
        # Stocker les données structurées
        structured_jobs = []
        
        # Traiter chaque emploi avec les nouvelles fonctions
        for i, job in enumerate(search_results, 1):
            print(f"📋 **Test Emploi {i}: {job.get('title', 'N/A')}**")
            
            # Récupérer les détails complets
            job_details = None
            if 'entityUrn' in job:
                try:
                    job_id = job['entityUrn'].split(':')[-1]
                    job_details = linkedin.get_job(job_id)
                    time.sleep(1)  # Pause entre les requêtes
                except Exception as e:
                    print(f"   ⚠️  Erreur détails: {str(e)}")
            
            # Extraire les données avec la nouvelle fonction
            data = extract_structured_data(job, job_details)
            structured_jobs.append(data)
            
            # Affichage focalisé sur les données demandées
            print(f"   🏢 Entreprise: {data['entreprise']}")
            print(f"   📍 Localisation: {data['localisation']}")
            print(f"   📋 Type contrat: {data['type_contrat']}")
            print(f"   🏠 Lieu travail: {data['type_lieu_travail']}")
            print(f"   📅 Publication: {data['date_publication']}")
            
            # Description (focus principal)
            if data['description']:
                print(f"   📝 Description: {data['description'][:200]}...")
            else:
                print(f"   📝 Description: Non disponible")
            
            print("-" * 80)
        
        # Sauvegarder le test
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/exports/test_focused_extraction_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(structured_jobs, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Test sauvegardé: {filename}")
        print(f"📊 Résultat: {len(structured_jobs)} emplois avec données structurées")
        
        # Analyse des résultats
        companies = [job['entreprise'] for job in structured_jobs if job['entreprise'] != 'N/A']
        contract_types = [job['type_contrat'] for job in structured_jobs if job['type_contrat'] != 'N/A']
        locations = [job['localisation'] for job in structured_jobs if job['localisation'] != 'N/A']
        
        print(f"\n📈 Analyse du test:")
        print(f"   ✅ Entreprises extraites: {len(companies)}/{len(structured_jobs)}")
        print(f"   ✅ Types contrats: {len(set(contract_types))} types différents")
        print(f"   ✅ Localisations: {len(set(locations))} lieux différents")
        print(f"   ✅ Descriptions: {len([j for j in structured_jobs if j['description']])}/{len(structured_jobs)}")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_focused_search()