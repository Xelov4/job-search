#!/usr/bin/env python3
"""
Script de test amélioré pour la recherche d'emplois SEO à Paris
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json

# Charger les variables d'environnement
# Charger les variables d'environnement depuis config/
load_dotenv('../../config/.env')

def test_enhanced_seo_job_search():
    """Test de recherche d'emplois SEO à Paris avec plus de détails"""
    try:
        # Initialiser l'API LinkedIn
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=False  # Désactiver le debug pour plus de clarté
        )
        
        print("🔍 Recherche d'emplois SEO à Paris, France...")
        print("=" * 60)
        
        # Effectuer la recherche
        search_results = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, France",
            limit=5  # Réduire pour tester
        )
        
        if not search_results:
            print("❌ Aucun emploi trouvé avec ces critères.")
            return
        
        print(f"✅ {len(search_results)} emplois trouvés !\n")
        
        # Afficher les résultats avec plus de détails
        for i, job in enumerate(search_results, 1):
            print(f"📋 **Emploi {i}**")
            print(f"   Titre: {job.get('title', 'N/A')}")
            
            # Essayer de récupérer plus d'informations
            if 'entityUrn' in job:
                try:
                    # Récupérer les détails complets de l'emploi
                    job_id = job['entityUrn'].split(':')[-1]
                    job_details = linkedin.get_job(job_id)
                    
                    if job_details:
                        print(f"   Entreprise: {job_details.get('companyName', 'N/A')}")
                        print(f"   Localisation: {job_details.get('formattedLocation', 'N/A')}")
                        print(f"   Type: {job_details.get('employmentStatus', 'N/A')}")
                        print(f"   Expérience: {job_details.get('experienceLevel', 'N/A')}")
                        print(f"   Date: {job_details.get('listedAt', 'N/A')}")
                        print(f"   Description: {job_details.get('description', 'N/A')[:100]}...")
                        
                except Exception as e:
                    print(f"   ⚠️  Impossible de récupérer les détails: {e}")
            
            # Afficher les informations disponibles dans le résultat de base
            print(f"   ID: {job.get('entityUrn', 'N/A')}")
            print(f"   Type de contenu: {job.get('contentType', 'N/A')}")
            
            print("-" * 60)
        
        # Sauvegarder les résultats bruts pour analyse
        with open('../../data/temp/search_results_raw.json', 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        print("💾 Résultats bruts sauvegardés dans 'search_results_raw.json'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_seo_job_search()
