#!/usr/bin/env python3
"""
Recherche et analyse de 100 emplois "SEO Specialist" avec scoring avancé
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

def analyze_seo_specialist_relevance(title, description, company_name=None):
    """Analyse la pertinence SEO Specialist avec scoring avancé"""
    
    # Normalisation des textes
    title_lower = title.lower() if title else ""
    desc_lower = description.lower() if description else ""
    
    # Mots-clés SEO Specialist primaires (score élevé)
    seo_primary = ['seo specialist', 'seo', 'référenceur', 'search engine optimization', 'search engine', 'specialist']
    seo_primary_score = 10
    
    # Mots-clés SEO Specialist secondaires (score moyen)
    seo_secondary = ['organic', 'traffic', 'ranking', 'google', 'keywords', 'meta', 'backlink', 'on-page', 'off-page', 'technical seo', 'local seo']
    seo_secondary_score = 5
    
    # Mots-clés marketing digital et spécialisation (score faible)
    seo_related = ['marketing', 'digital', 'content', 'acquisition', 'growth', 'performance', 'analytics', 'conversion', 'strategy', 'optimization']
    seo_related_score = 2
    
    # Mots-clés négatifs (déduction de points)
    seo_negative = ['casino', 'gaming', 'gambling', 'spontaneous', 'general manager', 'sales', 'business development']
    seo_negative_score = -5
    
    total_score = 0
    matches = []
    
    # Analyse du titre
    for keyword in seo_primary:
        if keyword in title_lower:
            total_score += seo_primary_score
            matches.append(f"Titre: {keyword} (+{seo_primary_score})")
    
    for keyword in seo_secondary:
        if keyword in title_lower:
            total_score += seo_secondary_score
            matches.append(f"Titre: {keyword} (+{seo_secondary_score})")
    
    # Analyse de la description
    if description:
        for keyword in seo_primary:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += seo_primary_score * min(count, 3)  # Max 3 occurrences
                matches.append(f"Description: {keyword} x{count} (+{seo_primary_score * min(count, 3)})")
        
        for keyword in seo_secondary:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += seo_secondary_score * min(count, 2)
                matches.append(f"Description: {keyword} x{count} (+{seo_secondary_score * min(count, 2)})")
        
        for keyword in seo_related:
            count = desc_lower.count(keyword)
            if count > 0:
                total_score += seo_related_score * min(count, 1)
                matches.append(f"Description: {keyword} x{count} (+{seo_related_score * min(count, 1)})")
    
    # Pénalités pour mots-clés négatifs
    for keyword in seo_negative:
        if keyword in title_lower or (description and keyword in desc_lower):
            total_score += seo_negative_score
            matches.append(f"Négatif: {keyword} ({seo_negative_score})")
    
    # Bonus pour la longueur de la description
    if description:
        desc_length = len(description)
        if desc_length > 1000:
            total_score += 3
            matches.append(f"Description longue (+3)")
        elif desc_length > 500:
            total_score += 1
            matches.append(f"Description moyenne (+1)")
    
    # Déterminer la classe de pertinence
    if total_score >= 15:
        relevance_class = "A"
        relevance = "TRÈS PERTINENT"
    elif total_score >= 8:
        relevance_class = "B"
        relevance = "PERTINENT"
    elif total_score >= 3:
        relevance_class = "C"
        relevance = "MODÉRÉMENT PERTINENT"
    elif total_score >= 0:
        relevance_class = "D"
        relevance = "PEU PERTINENT"
    else:
        relevance_class = "E"
        relevance = "NON PERTINENT"
    
    return {
        'score': total_score,
        'relevance': relevance,
        'relevance_class': relevance_class,
        'matches': matches
    }

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

def search_and_analyze_seo_specialist_100():
    """Recherche et analyse 100 emplois SEO Specialist"""
    
    # Connexion LinkedIn
    print("🔐 Connexion à LinkedIn...")
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 ANALYSE COMPLÈTE DE PERTINENCE SEO SPECIALIST")
    print("📋 Mot-clé: SEO Specialist")
    print("🌍 Localisation: Paris, Île-de-France, France")
    print("📊 Objectif: 100 emplois avec analyse complète")
    print("=" * 80)
    
    try:
        # Recherche initiale
        print("🔍 Phase 1: Recherche des emplois (100 emplois)...")
        jobs = linkedin.search_jobs(
            keywords="SEO Specialist",
            location="Paris, Île-de-France, France", 
            limit=100
        )
        
        if not jobs:
            print("❌ Aucun emploi trouvé")
            return
        
        print(f"✅ {len(jobs)} emplois trouvés\n")
        
        # Phase 2: Extraction des détails complets
        print("🔍 Phase 2: Extraction des descriptions complètes (100 emplois)...")
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
                relevance_analysis = analyze_seo_specialist_relevance(
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
                time.sleep(2)
            else:
                print(f"      ⚠️ Pas de détails disponibles")
                # Ajouter quand même l'emploi de base
                relevance_analysis = analyze_seo_specialist_relevance(job.get('title', ''), "")
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
                for i, job in enumerate(class_jobs[:10], 1):  # Top 10 par classe
                    title = job['basic_info'].get('title', 'N/A')
                    company = job['company_name']
                    score = job['relevance_analysis']['score']
                    print(f"   {i:2d}. {title} - {company} (Score: {score})")
        
        # Phase 4: Export des résultats
        print(f"\n💾 Phase 4: Export des résultats...")
        
        # Créer le dossier d'export s'il n'existe pas
        os.makedirs('data/exports', exist_ok=True)
        
        # Nom du fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/exports/seo_specialist_100_emplois_{timestamp}.json"
        
        # Sauvegarder les résultats complets
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'search_keywords': 'SEO Specialist',
                    'location': 'Paris, Île-de-France, France',
                    'total_jobs': len(jobs_with_details),
                    'timestamp': timestamp,
                    'analysis_type': 'SEO Specialist 100 emplois'
                },
                'statistics': {
                    'total_score': total_score,
                    'average_score': avg_score,
                    'class_distribution': class_distribution
                },
                'jobs': jobs_with_details
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Résultats sauvegardés dans: {filename}")
        
        # Générer un rapport markdown
        report_filename = f"data/exports/RAPPORT_SEO_SPECIALIST_100_{timestamp}.md"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"# 📊 RAPPORT D'ANALYSE SEO SPECIALIST - 100 EMPLOIS\n\n")
            f.write(f"**Date :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
            f.write(f"**Mot-clé :** SEO Specialist\n")
            f.write(f"**Localisation :** Paris, Île-de-France, France\n")
            f.write(f"**Total analysé :** {len(jobs_with_details)} emplois\n\n")
            
            f.write(f"## 📈 STATISTIQUES GLOBALES\n\n")
            f.write(f"- **Score total :** {total_score}\n")
            f.write(f"- **Score moyen :** {avg_score:.2f}\n")
            f.write(f"- **Efficacité :** {class_distribution.get('A', 0) + class_distribution.get('B', 0)} emplois pertinents sur {len(jobs_with_details)}\n\n")
            
            f.write(f"## 🏆 RÉPARTITION PAR CLASSE\n\n")
            for class_letter in ['A', 'B', 'C', 'D', 'E']:
                count = class_distribution.get(class_letter, 0)
                percentage = (count / len(jobs_with_details)) * 100
                f.write(f"### Classe {class_letter} : {count} emplois ({percentage:.1f}%)\n\n")
                
                class_jobs = [job for job in jobs_with_details if job['relevance_analysis']['relevance_class'] == class_letter]
                for i, job in enumerate(class_jobs[:5], 1):
                    title = job['basic_info'].get('title', 'N/A')
                    company = job['company_name']
                    score = job['relevance_analysis']['score']
                    f.write(f"{i}. **{title}** - {company} (Score: {score})\n")
                f.write("\n")
        
        print(f"✅ Rapport généré: {report_filename}")
        
        return {
            'total_jobs': len(jobs_with_details),
            'class_distribution': class_distribution,
            'average_score': avg_score,
            'filename': filename,
            'report_filename': report_filename
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return None

if __name__ == "__main__":
    results = search_and_analyze_seo_specialist_100()
    if results:
        print(f"\n🎉 ANALYSE TERMINÉE AVEC SUCCÈS !")
        print(f"📊 {results['total_jobs']} emplois analysés")
        print(f"📁 Résultats: {results['filename']}")
        print(f"📋 Rapport: {results['report_filename']}")
    else:
        print(f"\n❌ Échec de l'analyse")
