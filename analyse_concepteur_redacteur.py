#!/usr/bin/env python3
"""
Analyse complète de pertinence pour Concepteur Redacteur avec extraction des descriptions complètes
"""
import sys
sys.path.insert(0, 'src')

from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime
import re

load_dotenv('config/.env')

def extract_job_details(linkedin, job):
    """Extrait les détails complets d'un emploi via l'API LinkedIn"""
    try:
        if 'entityUrn' in job:
            job_id = job['entityUrn'].split(':')[-1]
            job_details = linkedin.get_job(job_id)
            return job_details
        return None
    except Exception as e:
        print(f"   ⚠️ Erreur extraction détails: {e}")
        return None

def analyze_concepteur_redacteur_relevance(title, description, company_name=None):
    """Analyse la pertinence pour Concepteur Redacteur avec scoring avancé"""
    
    # Normalisation des textes
    title_lower = title.lower() if title else ""
    desc_lower = description.lower() if description else ""
    
    # Mots-clés Concepteur Redacteur primaires (score élevé)
    concepteur_primary = [
        'concepteur rédacteur', 'concepteur-rédacteur', 'concepteur redacteur',
        'concepteur', 'rédacteur', 'redacteur', 'copywriter', 'copy writer',
        'concepteur créatif', 'rédacteur créatif', 'concepteur publicitaire',
        'rédacteur publicitaire', 'concepteur-rédacteur publicitaire'
    ]
    concepteur_primary_score = 10
    
    # Mots-clés Concepteur Redacteur secondaires (score moyen)
    concepteur_secondary = [
        'contenu', 'content', 'rédaction', 'redaction', 'création', 'creation',
        'concept', 'concepting', 'stratégie créative', 'creative strategy',
        'campagne publicitaire', 'advertising campaign', 'marque', 'brand',
        'communication', 'marketing', 'publicité', 'advertising', 'agence',
        'agency', 'studio créatif', 'creative studio'
    ]
    concepteur_secondary_score = 5
    
    # Mots-clés connexes et compétences (score faible)
    concepteur_related = [
        'design', 'graphisme', 'graphic design', 'typographie', 'typography',
        'identité visuelle', 'visual identity', 'logo', 'packaging', 'emballage',
        'print', 'digital', 'web', 'social media', 'réseaux sociaux',
        'storytelling', 'narratif', 'tone of voice', 'ton de voix',
        'positionnement', 'positioning', 'cible', 'target', 'audience'
    ]
    concepteur_related_score = 2
    
    # Mots-clés négatifs (déduction de points)
    concepteur_negative = [
        'casino', 'gaming', 'gambling', 'spontaneous', 'general manager',
        'sales', 'business development', 'développeur', 'developer',
        'programmeur', 'programmer', 'ingénieur', 'engineer', 'technique',
        'technical', 'maintenance', 'support', 'administratif', 'administrative'
    ]
    concepteur_negative_score = -5
    
    total_score = 0
    matches = []
    
    # Analyse du titre
    for keyword in concepteur_primary:
        if keyword in title_lower:
            total_score += concepteur_primary_score
            matches.append(f"Titre: {keyword} (+{concepteur_primary_score})")
    
    for keyword in concepteur_secondary:
        if keyword in title_lower:
            total_score += concepteur_secondary_score
            matches.append(f"Titre: {keyword} (+{concepteur_secondary_score})")
    
    # Analyse de la description
    if description:
        for keyword in concepteur_primary:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += concepteur_primary_score * min(count, 3)  # Max 3 occurrences
                matches.append(f"Description: {keyword} x{count} (+{concepteur_primary_score * min(count, 3)})")
        
        for keyword in concepteur_secondary:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += concepteur_secondary_score * min(count, 2)
                matches.append(f"Description: {keyword} x{count} (+{concepteur_secondary_score * min(count, 2)})")
        
        for keyword in concepteur_related:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += concepteur_related_score * min(count, 1)
                matches.append(f"Description: {keyword} x{count} (+{concepteur_related_score * min(count, 1)})")
    
    # Pénalités pour mots-clés négatifs
    for keyword in concepteur_negative:
        if keyword in title_lower or (description and keyword in desc_lower):
            total_score += concepteur_negative_score
            matches.append(f"Négatif: {keyword} ({concepteur_negative_score})")
    
    # Bonus pour la longueur de la description (plus de détails = plus de contexte)
    if description:
        desc_length = len(description)
        if desc_length > 1000:
            total_score += 3
            matches.append(f"Description longue (+3)")
        elif desc_length > 500:
            total_score += 1
            matches.append(f"Description moyenne (+1)")
    
    # Bonus pour la présence du nom de l'entreprise
    if company_name and company_name != "N/A":
        total_score += 1
        matches.append(f"Entreprise identifiée (+1)")
    
    # Déterminer la classe de pertinence
    if total_score >= 15:
        relevance_class = "A"
        relevance = "TRÈS PERTINENT - POSTULER EN PRIORITÉ"
    elif total_score >= 8:
        relevance_class = "B"
        relevance = "PERTINENT - POSTULER"
    elif total_score >= 3:
        relevance_class = "C"
        relevance = "MODÉRÉMENT PERTINENT - ÉVALUER"
    elif total_score >= 0:
        relevance_class = "D"
        relevance = "PEU PERTINENT - IGNORER"
    else:
        relevance_class = "E"
        relevance = "NON PERTINENT - IGNORER TOTALEMENT"
    
    return {
        'score': total_score,
        'relevance_class': relevance_class,
        'relevance': relevance,
        'matches': matches
    }

def search_and_analyze_concepteur_redacteur_complete():
    """Recherche et analyse complète pour Concepteur Redacteur"""
    
    # Vérifier les credentials
    if not os.getenv("LINKEDIN_EMAIL") or not os.getenv("LINKEDIN_PASSWORD"):
        print("❌ Erreur: Credentials LinkedIn manquants dans config/.env")
        print("   Créez le fichier config/.env avec LINKEDIN_EMAIL et LINKEDIN_PASSWORD")
        return
    
    # Vérifier que le dossier d'export existe
    os.makedirs('data/exports', exist_ok=True)
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 ANALYSE COMPLÈTE DE PERTINENCE CONCEPTEUR RÉDACTEUR")
    print("📋 Mot-clé: Concepteur Rédacteur")
    print("🌍 Localisation: Paris, Île-de-France, France")
    print("📊 Objectif: 50 emplois avec analyse complète")
    print("=" * 80)
    
    try:
        # Recherche initiale
        print("🔍 Phase 1: Recherche des emplois (50 emplois)...")
        jobs = linkedin.search_jobs(
            keywords="Concepteur Rédacteur",
            location="Paris, Île-de-France, France", 
            limit=50
        )
        
        if not jobs:
            print("❌ Aucun emploi trouvé")
            return
        
        print(f"✅ {len(jobs)} emplois trouvés\n")
        
        # Phase 2: Extraction des détails complets
        print("🔍 Phase 2: Extraction des descriptions complètes (50 emplois)...")
        jobs_with_details = []
        
        for i, job in enumerate(jobs, 1):
            print(f"   📋 Emploi {i}/{len(jobs)}: {job.get('title', 'N/A')}")
            
            # Extraction des détails complets
            job_details = extract_job_details(linkedin, job)
            
            if job_details:
                # Extraire la description
                description = ""
                if 'description' in job_details:
                    desc_data = job_details['description']
                    if isinstance(desc_data, dict) and 'text' in desc_data:
                        description = desc_data['text']
                    elif isinstance(desc_data, str):
                        description = desc_data
                
                # Extraire le nom de l'entreprise
                company_name = "N/A"
                if 'companyDetails' in job_details:
                    comp_details = job_details['companyDetails']
                    if isinstance(comp_details, dict):
                        for key in comp_details:
                            if 'companyResolutionResult' in comp_details[key]:
                                comp_result = comp_details[key]['companyResolutionResult']
                                if isinstance(comp_result, dict) and 'name' in comp_result:
                                    company_name = comp_result['name']
                                    break
                
                # Analyse de pertinence complète
                relevance_analysis = analyze_concepteur_redacteur_relevance(
                    job.get('title', ''),
                    description,
                    company_name
                )
                
                job_with_details = {
                    'basic_info': job,
                    'detailed_info': job_details,
                    'description': description,
                    'company_name': company_name,
                    'relevance_analysis': relevance_analysis
                }
                
                jobs_with_details.append(job_with_details)
                
                print(f"      ✅ Détails extraits - Score: {relevance_analysis['score']} - {relevance_analysis['relevance']}")
                
                # Pause pour éviter le rate limiting
                time.sleep(1)
            else:
                print(f"      ⚠️ Pas de détails disponibles")
                # Ajouter quand même l'emploi de base
                relevance_analysis = analyze_concepteur_redacteur_relevance(job.get('title', ''), "")
                job_with_details = {
                    'basic_info': job,
                    'detailed_info': None,
                    'description': "",
                    'company_name': "N/A",
                    'relevance_analysis': relevance_analysis
                }
                jobs_with_details.append(job_with_details)
        
        print(f"\n✅ Extraction terminée: {len(jobs_with_details)} emplois analysés\n")
        
        # Phase 3: Analyse et classement
        print("🔍 Phase 3: Analyse et classement par pertinence...")
        
        # Classer par score de pertinence
        jobs_with_details.sort(key=lambda x: x['relevance_analysis']['score'], reverse=True)
        
        # Statistiques globales
        total_score = sum(job['relevance_analysis']['score'] for job in jobs_with_details)
        avg_score = total_score / len(jobs_with_details)
        
        # Répartition par classe de pertinence
        class_distribution = {}
        for job in jobs_with_details:
            relevance_class = job['relevance_analysis']['relevance_class']
            class_distribution[relevance_class] = class_distribution.get(relevance_class, 0) + 1
        
        print(f"📊 STATISTIQUES GLOBALES:")
        print(f"   • Total emplois analysés: {len(jobs_with_details)}")
        print(f"   • Score total: {total_score}")
        print(f"   • Score moyen: {avg_score:.2f}")
        print(f"   • Répartition par classe:")
        for class_letter in sorted(class_distribution.keys()):
            count = class_distribution[class_letter]
            percentage = (count / len(jobs_with_details)) * 100
            print(f"     - Classe {class_letter}: {count} emplois ({percentage:.1f}%)")
        
        # Afficher les emplois par classe de pertinence
        print(f"\n🏆 EMPLOIS PAR CLASSE DE PERTINENCE:")
        
        for class_letter in ['A', 'B', 'C', 'D', 'E']:
            class_jobs = [job for job in jobs_with_details if job['relevance_analysis']['relevance_class'] == class_letter]
            if class_jobs:
                print(f"\n📋 CLASSE {class_letter} - {len(class_jobs)} emplois:")
                for i, job in enumerate(class_jobs[:5], 1):  # Top 5 par classe
                    title = job['basic_info'].get('title', 'N/A')
                    company = job['company_name']
                    score = job['relevance_analysis']['score']
                    relevance = job['relevance_analysis']['relevance']
                    print(f"   {i}. {title} - {company} (Score: {score}, {relevance})")
                
                if len(class_jobs) > 5:
                    print(f"   ... et {len(class_jobs) - 5} autres")
        
        # Sauvegarde complète
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/exports/analyse_concepteur_redacteur_{timestamp}.json"
        
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'search_params': {
                'keywords': 'Concepteur Rédacteur',
                'location': 'Paris, Île-de-France, France',
                'limit': 50
            },
            'analysis_summary': {
                'total_jobs': len(jobs_with_details),
                'total_score': total_score,
                'average_score': avg_score,
                'class_distribution': class_distribution
            },
            'jobs_analyzed': jobs_with_details
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Analyse complète sauvegardée: {filename}")
        
        return jobs_with_details
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    results = search_and_analyze_concepteur_redacteur_complete()
