#!/usr/bin/env python3
"""
Script de test pour la recherche d'emplois SEO à Paris
"""
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

def test_seo_job_search():
    """Test de recherche d'emplois SEO à Paris"""
    try:
        # Initialiser l'API LinkedIn
        linkedin = Linkedin(
            os.getenv("LINKEDIN_EMAIL"), 
            os.getenv("LINKEDIN_PASSWORD"), 
            debug=True
        )
        
        print("🔍 Recherche d'emplois SEO à Paris, France...")
        print("=" * 50)
        
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
        
        # Afficher les résultats
        for i, job in enumerate(search_results, 1):
            print(f"📋 **Emploi {i}**")
            print(f"   Titre: {job.get('title', 'N/A')}")
            print(f"   Entreprise: {job.get('company', 'N/A')}")
            print(f"   Localisation: {job.get('location', 'N/A')}")
            print(f"   Type: {job.get('job_type', 'N/A')}")
            print(f"   Expérience: {job.get('experience_level', 'N/A')}")
            print(f"   Date: {job.get('date_posted', 'N/A')}")
            print(f"   Lien: {job.get('job_url', 'N/A')}")
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")

if __name__ == "__main__":
    test_seo_job_search()
