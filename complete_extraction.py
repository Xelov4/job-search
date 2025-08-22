#!/usr/bin/env python3
"""
Script d'extraction complète de TOUTES les informations disponibles LinkedIn
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
            return f"Timestamp: {timestamp}"
    return "Date inconnue"

def extract_company_details(company_details):
    """Extraction complète des détails de l'entreprise"""
    if not company_details or not isinstance(company_details, dict):
        return {}
    
    company_info = {}
    
    for key in company_details:
        if isinstance(company_details[key], dict):
            comp_result = company_details[key].get('companyResolutionResult', {})
            if isinstance(comp_result, dict):
                company_info.update({
                    'name': comp_result.get('name', 'N/A'),
                    'entityUrn': comp_result.get('entityUrn', 'N/A'),
                    'universalName': company_details[key].get('universalName', 'N/A'),
                    'url': company_details[key].get('url', 'N/A')
                })
                
                # Logo de l'entreprise
                logo = comp_result.get('logo', {})
                if logo:
                    image_info = logo.get('image', {})
                    if image_info:
                        vector_image = image_info.get('com.linkedin.common.VectorImage', {})
                        if vector_image:
                            artifacts = vector_image.get('artifacts', [])
                            if artifacts:
                                company_info['logo_urls'] = []
                                for artifact in artifacts:
                                    company_info['logo_urls'].append({
                                        'size': f"{artifact.get('width', 0)}x{artifact.get('height', 0)}",
                                        'url': f"{vector_image.get('rootUrl', '')}{artifact.get('fileIdentifyingUrlPathSegment', '')}"
                                    })
    
    return company_info

def extract_description_full(description):
    """Extraction complète de la description avec formatage"""
    if not description:
        return {'text': '', 'formatted_info': 'Aucune description'}
    
    if isinstance(description, str):
        return {'text': description, 'formatted_info': 'Texte simple'}
    
    if isinstance(description, dict):
        result = {
            'text': description.get('text', ''),
            'formatted_info': 'Description avec formatage LinkedIn'
        }
        
        # Analyser les attributs de formatage
        attributes = description.get('attributes', [])
        if attributes:
            formatting_info = {
                'total_attributes': len(attributes),
                'formatting_types': [],
                'structure_elements': []
            }
            
            for attr in attributes:
                attr_type = attr.get('type', {})
                if attr_type:
                    for format_type in attr_type.keys():
                        if format_type not in formatting_info['formatting_types']:
                            formatting_info['formatting_types'].append(format_type)
                
                # Éléments de structure
                attr_union = attr.get('attributeKindUnion', {})
                for union_key in attr_union.keys():
                    if union_key not in formatting_info['structure_elements']:
                        formatting_info['structure_elements'].append(union_key)
            
            result['formatting_details'] = formatting_info
        
        return result
    
    return {'text': str(description), 'formatted_info': f'Format non géré: {type(description)}'}

def extract_apply_method(apply_method):
    """Extraction des méthodes de candidature"""
    if not apply_method or not isinstance(apply_method, dict):
        return {'type': 'N/A', 'details': {}}
    
    apply_info = {'type': 'Unknown', 'details': {}}
    
    for method_type, method_data in apply_method.items():
        if isinstance(method_data, dict):
            apply_info['type'] = method_type
            apply_info['details'] = method_data
            
            # Informations spécifiques selon le type
            if 'easyApplyUrl' in method_data:
                apply_info['easy_apply'] = True
                apply_info['apply_url'] = method_data['easyApplyUrl']
            elif 'companyApplyUrl' in method_data:
                apply_info['company_apply'] = True
                apply_info['apply_url'] = method_data['companyApplyUrl']
            
            apply_info['unify_enabled'] = method_data.get('unifyApplyEnabled', False)
    
    return apply_info

def extract_workplace_info(job_details):
    """Extraction complète des informations de lieu de travail"""
    workplace_info = {
        'types': [],
        'remote_allowed': job_details.get('workRemoteAllowed', False),
        'formatted_location': job_details.get('formattedLocation', 'N/A'),
        'detailed_types': []
    }
    
    # Types de lieu de travail
    workplace_types = job_details.get('workplaceTypes', [])
    workplace_results = job_details.get('workplaceTypesResolutionResults', {})
    
    for workplace_type in workplace_types:
        workplace_info['types'].append(workplace_type)
        
        # Résolution des types
        if workplace_type in workplace_results:
            resolved = workplace_results[workplace_type]
            workplace_info['detailed_types'].append({
                'urn': workplace_type,
                'localized_name': resolved.get('localizedName', 'N/A'),
                'entity_urn': resolved.get('entityUrn', 'N/A')
            })
    
    return workplace_info

def extract_complete_job_info(job_details):
    """Extraction complète de toutes les informations d'un emploi"""
    if not job_details or not isinstance(job_details, dict):
        return {}
    
    complete_info = {
        # Informations de base
        'basic_info': {
            'title': job_details.get('title', 'N/A'),
            'job_id': job_details.get('jobPostingId', 'N/A'),
            'entity_urn': job_details.get('entityUrn', 'N/A'),
            'dash_entity_urn': job_details.get('dashEntityUrn', 'N/A'),
            'job_state': job_details.get('jobState', 'N/A'),
            'talent_hub_job': job_details.get('talentHubJob', False),
            'recipe_type': job_details.get('$recipeType', 'N/A')
        },
        
        # Informations de l'entreprise
        'company': extract_company_details(job_details.get('companyDetails', {})),
        
        # Description complète
        'description': extract_description_full(job_details.get('description', {})),
        
        # Lieu de travail
        'workplace': extract_workplace_info(job_details),
        
        # Méthode de candidature
        'apply_method': extract_apply_method(job_details.get('applyMethod', {})),
        
        # Dates
        'dates': {
            'listed_at': job_details.get('listedAt'),
            'listed_at_formatted': format_timestamp(job_details.get('listedAt'))
        }
    }
    
    # Ajouter toutes les clés restantes qui n'ont pas été traitées
    processed_keys = {
        'title', 'jobPostingId', 'entityUrn', 'dashEntityUrn', 'jobState', 
        'talentHubJob', '$recipeType', 'companyDetails', 'description', 
        'workplaceTypes', 'workRemoteAllowed', 'formattedLocation', 
        'workplaceTypesResolutionResults', 'applyMethod', 'listedAt'
    }
    
    additional_data = {}
    for key, value in job_details.items():
        if key not in processed_keys:
            additional_data[key] = value
    
    if additional_data:
        complete_info['additional_fields'] = additional_data
    
    return complete_info

def search_complete_jobs():
    """Recherche avec extraction complète de toutes les informations"""
    try:
        # Initialiser l'API LinkedIn
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=False
        )
        
        print("🔍 EXTRACTION COMPLÈTE DE TOUTES LES INFORMATIONS LINKEDIN")
        print("=" * 80)
        
        # Effectuer la recherche
        search_results = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, France",
            limit=10  # 10 emplois pour analyse détaillée
        )
        
        if not search_results:
            print("❌ Aucun emploi trouvé")
            return
        
        print(f"✅ {len(search_results)} emplois trouvés\n")
        
        all_jobs_complete = []
        
        # Traiter chaque emploi
        for i, job in enumerate(search_results, 1):
            print(f"{'='*60}")
            print(f"📋 EMPLOI {i} - EXTRACTION COMPLÈTE")
            print(f"{'='*60}")
            
            # Données de base
            basic_job_data = {
                'search_result_data': job,
                'detailed_data': None,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            # Récupérer les détails complets
            if 'entityUrn' in job:
                job_id = job['entityUrn'].split(':')[-1]
                
                try:
                    job_details = linkedin.get_job(job_id)
                    
                    if job_details:
                        # Extraction complète
                        complete_info = extract_complete_job_info(job_details)
                        basic_job_data['detailed_data'] = complete_info
                        
                        # Affichage formaté
                        print(f"📍 TITRE: {complete_info['basic_info']['title']}")
                        print(f"🏢 ENTREPRISE: {complete_info['company'].get('name', 'N/A')}")
                        print(f"📍 LOCALISATION: {complete_info['workplace']['formatted_location']}")
                        print(f"🏠 TYPE: {', '.join([wt['localized_name'] for wt in complete_info['workplace']['detailed_types']])}")
                        print(f"🌐 TÉLÉTRAVAIL: {'Oui' if complete_info['workplace']['remote_allowed'] else 'Non'}")
                        print(f"📅 PUBLIÉ: {complete_info['dates']['listed_at_formatted']}")
                        print(f"✉️ CANDIDATURE: {complete_info['apply_method']['type']}")
                        
                        if complete_info['company'].get('logo_urls'):
                            print(f"🎨 LOGOS ENTREPRISE: {len(complete_info['company']['logo_urls'])} tailles disponibles")
                        
                        # Description (tronquée pour l'affichage)
                        desc_text = complete_info['description']['text']
                        if desc_text:
                            print(f"📝 DESCRIPTION: {desc_text[:200]}...")
                            print(f"📐 FORMATAGE: {complete_info['description']['formatted_info']}")
                        
                        # Informations supplémentaires
                        if 'additional_fields' in complete_info:
                            print(f"➕ CHAMPS ADDITIONNELS: {len(complete_info['additional_fields'])} champs")
                            for field_name in complete_info['additional_fields'].keys():
                                print(f"   • {field_name}")
                    else:
                        print("❌ Aucun détail récupéré")
                        
                except Exception as e:
                    print(f"❌ Erreur: {e}")
                    basic_job_data['error'] = str(e)
            
            all_jobs_complete.append(basic_job_data)
            print("\n")
        
        # Sauvegarde complète
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"complete_extraction_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_jobs_complete, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 EXTRACTION COMPLÈTE SAUVEGARDÉE dans '{filename}'")
        print(f"📊 TOTAL: {len(all_jobs_complete)} emplois avec extraction complète")
        
        return all_jobs_complete
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_complete_jobs()