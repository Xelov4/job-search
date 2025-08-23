#!/usr/bin/env python3
"""
Script final pour la recherche d'emplois SEO à Paris avec tous les détails
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

def extract_description_text(description):
    """Extrait le texte brut d'une description LinkedIn formatée"""
    if not description:
        return "Aucune description"
    
    if isinstance(description, str):
        return description
    
    if isinstance(description, dict):
        # Si c'est un objet avec un texte direct
        if 'text' in description:
            return description['text']
            
        # Si c'est un objet avec des attributs formatés
        if 'attributes' in description:
            try:
                # Reconstituer le texte depuis les attributs
                full_text = description.get('text', '')
                if full_text:
                    return full_text
                else:
                    # Fallback: essayer d'extraire depuis les attributs
                    return "Texte formaté (extraction partielle non implémentée)"
            except:
                return "Erreur lors de l'extraction du texte"
    
    return f"Format non supporté: {type(description)}"

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
        
        print(f"🔍 Debug - Type de search_results: {type(search_results)}")
        print(f"🔍 Debug - Nombre d'emplois: {len(search_results) if search_results else 0}")
        if search_results and len(search_results) > 0:
            print(f"🔍 Debug - Structure du premier emploi:")
            first_job = search_results[0]
            for key, value in first_job.items():
                print(f"     {key}: {type(value)} = {str(value)[:100]}..." if len(str(value)) > 100 else f"     {key}: {type(value)} = {value}")
        
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
            print(f"   Poster ID: {job.get('posterId', 'N/A')}")
            
            # Debug - afficher toutes les clés disponibles (commentaire pour moins de verbosité)
            # print(f"   🔍 Toutes les clés disponibles: {list(job.keys())}")
            
            # Essayer de récupérer plus d'informations via l'API
            if 'entityUrn' in job:
                try:
                    # Extraire l'ID de l'emploi
                    job_id = job['entityUrn'].split(':')[-1]
                    
                    # Récupérer les détails complets
                    print(f"   🔍 Tentative de récupération pour l'ID: {job_id}")
                    job_details = linkedin.get_job(job_id)
                    print(f"   🔍 Type de réponse: {type(job_details)}")
                    
                    if job_details:
                        print(f"   🔍 Debug - job_details reçu, type: {type(job_details)}")
                        if isinstance(job_details, dict):
                            print(f"   🔍 Debug - Clés dans job_details: {list(job_details.keys())}")
                        
                        # Debug spécifique pour companyDetails et description
                        company_details = job_details.get('companyDetails')
                        print(f"   🔍 companyDetails type: {type(company_details)} = {company_details}")
                        
                        desc = job_details.get('description')
                        print(f"   🔍 description type: {type(desc)}")
                        if isinstance(desc, dict):
                            print(f"   🔍 description keys: {list(desc.keys())}")
                            if 'text' in desc:
                                print(f"   🔍 description.text: {desc['text'][:100] if desc['text'] else 'Empty'}...")
                            
                            # Informations de base - extraction correcte des données LinkedIn
                            # Entreprise depuis companyDetails
                            company_details = job_details.get('companyDetails', {})
                            if isinstance(company_details, dict):
                                company = company_details.get('companyName') or company_details.get('name', 'N/A')
                            else:
                                company = 'N/A'
                                
                            location = job_details.get('formattedLocation', 'N/A')
                            
                            # Types de lieu de travail - décodage des URNs LinkedIn
                            workplace_types = job_details.get('workplaceTypes', [])
                            work_remote = job_details.get('workRemoteAllowed', False)
                            
                            # Mapper les URNs vers du texte lisible
                            workplace_mapping = {
                                'urn:li:fs_workplaceType:1': 'Sur site',
                                'urn:li:fs_workplaceType:2': 'Hybride', 
                                'urn:li:fs_workplaceType:3': 'Distanciel'
                            }
                            
                            workplace_info = 'N/A'
                            if workplace_types:
                                decoded_types = [workplace_mapping.get(wt, wt) for wt in workplace_types]
                                workplace_info = ', '.join(decoded_types)
                            
                            if work_remote:
                                workplace_info += ' (Télétravail autorisé)'
                                
                            job_type = workplace_info
                            experience = 'N/A'  # Cette info n'est pas directement disponible dans cette structure
                            
                            print(f"   Entreprise: {company}")
                            print(f"   Localisation: {location}")
                            print(f"   Type: {job_type}")
                            print(f"   Expérience: {experience}")
                        else:
                            print(f"   ⚠️  job_details n'est pas un dictionnaire: {type(job_details)}")
                            print(f"   🔍 Contenu: {str(job_details)[:200]}...")
                        
                            # Description - extraction du texte depuis les attributs LinkedIn
                            description = job_details.get('description', '')
                            if description:
                                extracted_text = extract_description_text(description)
                                if len(extracted_text) > 200:
                                    print(f"   Description: {extracted_text[:200]}...")
                                else:
                                    print(f"   Description: {extracted_text}")
                        
                            # Informations supplémentaires
                            apply_method = job_details.get('applyMethod', {})
                            if isinstance(apply_method, dict):
                                apply_info = apply_method.get('companyApplyUrl') or apply_method.get('easyApplyUrl')
                                if apply_info:
                                    print(f"   Postuler: Lien disponible")
                            
                            # Date de publication
                            listed_at = job_details.get('listedAt')
                            if listed_at:
                                print(f"   Publié le: {format_timestamp(listed_at)}")
                                
                            # État du job
                            job_state = job_details.get('jobState', 'N/A')
                            if job_state != 'N/A':
                                print(f"   État: {job_state}")
                        
                    else:
                        print(f"   ⚠️  Aucun détail reçu de l'API")
                        
                except Exception as e:
                    print(f"   ⚠️  Erreur lors de la récupération des détails: {str(e)}")
                    print(f"   🔍 Debug - ID utilisé: {job_id}")
                    print(f"   🔍 Debug - Type de job_details: {type(job_details) if 'job_details' in locals() else 'Non défini'}")
                    if 'job_details' in locals() and job_details:
                        print(f"   🔍 Debug - Clés disponibles: {list(job_details.keys()) if isinstance(job_details, dict) else 'Pas un dict'}")
            
            print("-" * 70)
        
        # Sauvegarder les résultats dans data/temp/
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../../data/temp/seo_jobs_paris_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats sauvegardés dans '{filename}'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_seo_jobs_paris()
