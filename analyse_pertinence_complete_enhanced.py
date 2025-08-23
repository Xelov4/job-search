#!/usr/bin/env python3
"""
Analyse complète de pertinence avec exploitation EXHAUSTIVE de tous les champs LinkedIn
Version Enhanced avec tous les champs utiles et génération de rapport Markdown complet
"""
import sys
sys.path.insert(0, 'src')

from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime, timedelta
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

def extract_enhanced_job_info(job_basic, job_details):
    """Extrait TOUTES les informations utiles d'un emploi (version enhanced)"""
    
    # === INFORMATIONS DE BASE ===
    title = job_basic.get('title', 'N/A')
    entity_urn = job_basic.get('entityUrn', '')
    tracking_urn = job_basic.get('trackingUrn', '')
    poster_id = job_basic.get('posterId', '')
    is_reposted = job_basic.get('repostedJob', False)
    content_source = job_basic.get('contentSource', '')
    
    # === INFORMATIONS DÉTAILLÉES ===
    if not job_details:
        return create_basic_job_info(job_basic)
    
    # 1. IDs et URLs LinkedIn
    job_posting_id = job_details.get('jobPostingId', 0)
    linkedin_job_url = f"https://www.linkedin.com/jobs/view/{job_posting_id}" if job_posting_id else ""
    
    # 2. Description complète
    description = ""
    if 'description' in job_details:
        desc_data = job_details['description']
        if isinstance(desc_data, dict) and 'text' in desc_data:
            description = desc_data['text']
        elif isinstance(desc_data, str):
            description = desc_data
    
    # 3. Informations entreprise complètes
    company_info = extract_company_info(job_details)
    
    # 4. Localisation et mode de travail
    location_info = extract_location_and_work_info(job_details)
    
    # 5. Informations temporelles
    temporal_info = extract_temporal_info(job_details)
    
    # 6. URLs de candidature
    application_info = extract_application_info(job_details)
    
    # 7. État de l'offre
    job_state = job_details.get('jobState', 'UNKNOWN')
    talent_hub_job = job_details.get('talentHubJob', False)
    
    return {
        # Informations de base
        'title': title,
        'entity_urn': entity_urn,
        'tracking_urn': tracking_urn,
        'job_posting_id': job_posting_id,
        'linkedin_job_url': linkedin_job_url,
        'poster_id': poster_id,
        'is_reposted': is_reposted,
        'content_source': content_source,
        
        # Description
        'description': description,
        'description_length': len(description),
        
        # Informations entreprise
        **company_info,
        
        # Localisation et mode de travail
        **location_info,
        
        # Informations temporelles
        **temporal_info,
        
        # Application
        **application_info,
        
        # État
        'job_state': job_state,
        'is_talent_hub_job': talent_hub_job,
        
        # Données brutes pour référence
        'raw_basic_info': job_basic,
        'raw_detailed_info': job_details
    }

def extract_company_info(job_details):
    """Extrait toutes les informations de l'entreprise"""
    company_info = {
        'company_name': 'N/A',
        'company_linkedin_url': '',
        'company_universal_name': '',
        'company_entity_urn': '',
        'company_logo_url': ''
    }
    
    if 'companyDetails' in job_details:
        comp_details = job_details['companyDetails']
        if isinstance(comp_details, dict):
            for key in comp_details:
                if 'companyResolutionResult' in comp_details[key]:
                    comp_result = comp_details[key]['companyResolutionResult']
                    if isinstance(comp_result, dict):
                        company_info.update({
                            'company_name': comp_result.get('name', 'N/A'),
                            'company_linkedin_url': comp_result.get('url', ''),
                            'company_universal_name': comp_result.get('universalName', ''),
                            'company_entity_urn': comp_result.get('entityUrn', '')
                        })
                        
                        # Logo entreprise
                        if 'logo' in comp_result:
                            logo_data = comp_result['logo']
                            if 'image' in logo_data:
                                image_data = logo_data['image']
                                if 'com.linkedin.common.VectorImage' in image_data:
                                    vector_img = image_data['com.linkedin.common.VectorImage']
                                    root_url = vector_img.get('rootUrl', '')
                                    if 'artifacts' in vector_img and vector_img['artifacts']:
                                        # Prendre le logo 200x200 si disponible
                                        for artifact in vector_img['artifacts']:
                                            if artifact.get('width') == 200:
                                                company_info['company_logo_url'] = root_url + artifact.get('fileIdentifyingUrlPathSegment', '')
                                                break
                        break
    
    return company_info

def extract_location_and_work_info(job_details):
    """Extrait les informations de localisation et mode de travail"""
    location_info = {
        'formatted_location': job_details.get('formattedLocation', ''),
        'work_remote_allowed': job_details.get('workRemoteAllowed', False),
        'workplace_types': job_details.get('workplaceTypes', []),
        'workplace_type_labels': []
    }
    
    # Résolution des types de lieu de travail
    workplace_resolution = job_details.get('workplaceTypesResolutionResults', {})
    for workplace_type in location_info['workplace_types']:
        if workplace_type in workplace_resolution:
            label = workplace_resolution[workplace_type].get('localizedName', '')
            if label:
                location_info['workplace_type_labels'].append(label)
    
    # Déterminer le type de travail principal
    if location_info['workplace_type_labels']:
        location_info['work_type'] = ', '.join(location_info['workplace_type_labels'])
    elif location_info['work_remote_allowed']:
        location_info['work_type'] = 'Remote'
    else:
        location_info['work_type'] = 'On-site'
    
    return location_info

def extract_temporal_info(job_details):
    """Extrait les informations temporelles"""
    listed_at_timestamp = job_details.get('listedAt', 0)
    
    temporal_info = {
        'listed_at_timestamp': listed_at_timestamp,
        'posted_date': '',
        'days_since_posted': 0,
        'freshness_category': ''
    }
    
    if listed_at_timestamp:
        try:
            posted_date = datetime.fromtimestamp(listed_at_timestamp / 1000)
            temporal_info['posted_date'] = posted_date.strftime('%Y-%m-%d %H:%M:%S')
            
            days_since = (datetime.now() - posted_date).days
            temporal_info['days_since_posted'] = days_since
            
            # Catégorisation de la fraîcheur
            if days_since == 0:
                temporal_info['freshness_category'] = 'Aujourd\'hui'
            elif days_since <= 3:
                temporal_info['freshness_category'] = 'Très récent'
            elif days_since <= 7:
                temporal_info['freshness_category'] = 'Récent'
            elif days_since <= 14:
                temporal_info['freshness_category'] = 'Moyen'
            else:
                temporal_info['freshness_category'] = 'Ancien'
        except:
            pass
    
    return temporal_info

def extract_application_info(job_details):
    """Extrait les informations de candidature"""
    application_info = {
        'apply_url': '',
        'apply_method_type': '',
        'in_page_apply': False
    }
    
    if 'applyMethod' in job_details:
        apply_method = job_details['applyMethod']
        if isinstance(apply_method, dict):
            for key, value in apply_method.items():
                if isinstance(value, dict):
                    application_info.update({
                        'apply_url': value.get('companyApplyUrl', ''),
                        'apply_method_type': key.split('.')[-1] if '.' in key else key,
                        'in_page_apply': value.get('inPageOffsiteApply', False)
                    })
                    break
    
    return application_info

def create_basic_job_info(job_basic):
    """Crée les informations de base si les détails ne sont pas disponibles"""
    return {
        'title': job_basic.get('title', 'N/A'),
        'entity_urn': job_basic.get('entityUrn', ''),
        'tracking_urn': job_basic.get('trackingUrn', ''),
        'job_posting_id': 0,
        'linkedin_job_url': '',
        'poster_id': job_basic.get('posterId', ''),
        'is_reposted': job_basic.get('repostedJob', False),
        'content_source': job_basic.get('contentSource', ''),
        'description': '',
        'description_length': 0,
        'company_name': 'N/A',
        'company_linkedin_url': '',
        'formatted_location': '',
        'work_remote_allowed': False,
        'work_type': 'Unknown',
        'posted_date': '',
        'days_since_posted': 0,
        'freshness_category': 'Unknown',
        'apply_url': '',
        'job_state': 'UNKNOWN',
        'raw_basic_info': job_basic,
        'raw_detailed_info': None
    }

def analyze_seo_relevance(title, description, company_name=None):
    """Analyse la pertinence SEO d'un emploi avec scoring avancé"""
    
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
    
    # Bonus pour la longueur de la description (plus de détails = plus de contexte)
    if description:
        desc_length = len(description)
        if desc_length > 1000:
            total_score += 3
            matches.append(f"Description longue (+3)")
        elif desc_length > 500:
            total_score += 1
            matches.append(f"Description moyenne (+1)")
    
    # Catégorisation de pertinence
    if total_score >= 15:
        relevance = "TRÈS PERTINENT"
        relevance_class = "A"
    elif total_score >= 8:
        relevance = "PERTINENT"
        relevance_class = "B"
    elif total_score >= 3:
        relevance = "MODÉRÉMENT PERTINENT"
        relevance_class = "C"
    elif total_score >= 0:
        relevance = "PEU PERTINENT"
        relevance_class = "D"
    else:
        relevance = "NON PERTINENT"
        relevance_class = "E"
    
    return {
        'score': total_score,
        'relevance': relevance,
        'relevance_class': relevance_class,
        'matches': matches,
        'title_analysis': {
            'has_seo_primary': any(kw in title_lower for kw in seo_primary),
            'has_seo_secondary': any(kw in title_lower for kw in seo_secondary),
            'has_negative': any(kw in title_lower for kw in seo_negative)
        },
        'description_analysis': {
            'length': len(description) if description else 0,
            'seo_primary_count': sum(desc_lower.count(kw) for kw in seo_primary) if description else 0,
            'seo_secondary_count': sum(desc_lower.count(kw) for kw in seo_secondary) if description else 0,
            'seo_related_count': sum(desc_lower.count(kw) for kw in seo_related) if description else 0
        }
    }

def generate_enhanced_markdown_report(jobs_data, search_params, analysis_summary, timestamp):
    """Génère un rapport Markdown complet avec TOUTES les informations"""
    
    # Calculer les statistiques avancées
    advanced_stats = calculate_advanced_statistics(jobs_data)
    
    report_content = f"""# 🔬 RAPPORT D'ANALYSE COMPLÈTE - {analysis_summary['total_jobs']} EMPLOIS ANALYSÉS

**Date d'analyse :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}  
**Méthodologie :** Analyse approfondie avec extraction complète de tous les champs LinkedIn  
**Mots-clés :** {search_params['keywords']}  
**Localisation :** {search_params['location']}  
**Volume analysé :** {analysis_summary['total_jobs']} emplois  

---

## 📊 SYNTHÈSE EXÉCUTIVE

### 🎯 PERFORMANCE GLOBALE
- **Efficacité globale :** {(analysis_summary['class_distribution'].get('A', 0) / analysis_summary['total_jobs'] * 100):.1f}% (Classe A)
- **Score moyen :** {analysis_summary['average_score']:.2f}/100
- **Score total :** {analysis_summary['total_score']} points
- **Taux d'extraction détails :** {advanced_stats['extraction_rate']:.1f}%

### 📈 RÉPARTITION PAR CLASSE DE PERTINENCE
- **🏆 Classe A (TRÈS PERTINENTS) :** {analysis_summary['class_distribution'].get('A', 0)} emplois ({(analysis_summary['class_distribution'].get('A', 0) / analysis_summary['total_jobs'] * 100):.1f}%)
- **🥈 Classe B (PERTINENTS) :** {analysis_summary['class_distribution'].get('B', 0)} emplois ({(analysis_summary['class_distribution'].get('B', 0) / analysis_summary['total_jobs'] * 100):.1f}%)
- **🥉 Classe C (MODÉRÉMENT PERTINENTS) :** {analysis_summary['class_distribution'].get('C', 0)} emplois ({(analysis_summary['class_distribution'].get('C', 0) / analysis_summary['total_jobs'] * 100):.1f}%)
- **📉 Classe D (PEU PERTINENTS) :** {analysis_summary['class_distribution'].get('D', 0)} emplois ({(analysis_summary['class_distribution'].get('D', 0) / analysis_summary['total_jobs'] * 100):.1f}%)
- **❌ Classe E (NON PERTINENTS) :** {analysis_summary['class_distribution'].get('E', 0)} emplois ({(analysis_summary['class_distribution'].get('E', 0) / analysis_summary['total_jobs'] * 100):.1f}%)

### 🌍 ANALYSE GÉOGRAPHIQUE ET MODE DE TRAVAIL
- **Télétravail autorisé :** {advanced_stats['remote_jobs']} emplois ({(advanced_stats['remote_jobs'] / analysis_summary['total_jobs'] * 100):.1f}%)
- **Mode hybride :** {advanced_stats['hybrid_jobs']} emplois ({(advanced_stats['hybrid_jobs'] / analysis_summary['total_jobs'] * 100):.1f}%)
- **Présentiel uniquement :** {advanced_stats['onsite_jobs']} emplois ({(advanced_stats['onsite_jobs'] / analysis_summary['total_jobs'] * 100):.1f}%)

### ⏰ ANALYSE TEMPORELLE
- **Emplois postés aujourd'hui :** {advanced_stats['today_jobs']} emplois
- **Emplois très récents (≤3j) :** {advanced_stats['very_recent_jobs']} emplois
- **Emplois récents (≤7j) :** {advanced_stats['recent_jobs']} emplois
- **Âge moyen des offres :** {advanced_stats['average_age']:.1f} jours

---

## 🏆 TOP 10 DES EMPLOIS LES PLUS PERTINENTS

"""

    # Top 10 des emplois
    top_jobs = sorted(jobs_data, key=lambda x: x['relevance_analysis']['score'], reverse=True)[:10]
    
    for i, job in enumerate(top_jobs, 1):
        job_info = job['enhanced_info']
        relevance = job['relevance_analysis']
        
        report_content += f"""### {i}. {job_info['title']} - {job_info['company_name']}
**Score :** {relevance['score']} points | **Classe :** {relevance['relevance_class']} | **Pertinence :** {relevance['relevance']}

- **🔗 Lien LinkedIn :** [{job_info['linkedin_job_url']}]({job_info['linkedin_job_url']})
- **🏢 Entreprise :** {job_info['company_name']} ([Profil LinkedIn]({job_info['company_linkedin_url']}))
- **📍 Localisation :** {job_info['formatted_location']}
- **💼 Mode de travail :** {job_info['work_type']}{'🏠 Télétravail autorisé' if job_info['work_remote_allowed'] else ''}
- **📅 Publié le :** {job_info['posted_date']} ({job_info['freshness_category']})
- **🎯 URL Candidature :** [{job_info['apply_url'][:50]}...]({job_info['apply_url']}) {' ✅' if job_info['apply_url'] else '❌ Non disponible'}

**Analyse de pertinence :**
{chr(10).join([f"- {match}" for match in relevance['matches'][:5]])}

---

"""

    # Analyse par classe
    report_content += """## 📋 ANALYSE DÉTAILLÉE PAR CLASSE

"""

    for class_letter in ['A', 'B', 'C', 'D', 'E']:
        class_jobs = [job for job in jobs_data if job['relevance_analysis']['relevance_class'] == class_letter]
        if class_jobs:
            class_names = {'A': 'TRÈS PERTINENTS', 'B': 'PERTINENTS', 'C': 'MODÉRÉMENT PERTINENTS', 'D': 'PEU PERTINENTS', 'E': 'NON PERTINENTS'}
            
            report_content += f"""### 📊 CLASSE {class_letter} - {class_names[class_letter]} ({len(class_jobs)} emplois)

| Titre | Entreprise | Score | Mode Travail | Fraîcheur | Lien LinkedIn |
|-------|------------|-------|--------------|-----------|---------------|
"""
            
            for job in class_jobs[:10]:  # Top 10 par classe
                info = job['enhanced_info']
                score = job['relevance_analysis']['score']
                work_mode = "🏠" if info['work_remote_allowed'] else ("🏢/🏠" if 'Hybrid' in info['work_type'] else "🏢")
                
                report_content += f"| {info['title'][:40]}... | {info['company_name'][:20]}... | {score} | {work_mode} {info['work_type']} | {info['freshness_category']} | [Voir]({info['linkedin_job_url']}) |\\n"
            
            if len(class_jobs) > 10:
                report_content += f"\\n*... et {len(class_jobs) - 10} autres emplois de classe {class_letter}*\\n"
            
            report_content += "\\n---\\n\\n"

    # Analyses avancées
    report_content += f"""## 🔍 ANALYSES AVANCÉES

### 🏢 TOP 10 DES ENTREPRISES QUI RECRUTENT
"""

    # Top entreprises
    company_stats = {}
    for job in jobs_data:
        company = job['enhanced_info']['company_name']
        if company != 'N/A':
            if company not in company_stats:
                company_stats[company] = {'count': 0, 'avg_score': 0, 'total_score': 0, 'url': job['enhanced_info']['company_linkedin_url']}
            company_stats[company]['count'] += 1
            company_stats[company]['total_score'] += job['relevance_analysis']['score']
            company_stats[company]['avg_score'] = company_stats[company]['total_score'] / company_stats[company]['count']

    top_companies = sorted(company_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
    
    for i, (company, stats) in enumerate(top_companies, 1):
        report_content += f"{i}. **{company}** - {stats['count']} emplois (Score moyen: {stats['avg_score']:.1f}) [Profil LinkedIn]({stats['url']})\\n"

    report_content += f"""

### 🌍 RÉPARTITION GÉOGRAPHIQUE
"""

    # Analyse des localisations
    location_stats = {}
    for job in jobs_data:
        location = job['enhanced_info']['formatted_location']
        if location:
            if location not in location_stats:
                location_stats[location] = 0
            location_stats[location] += 1

    top_locations = sorted(location_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    for location, count in top_locations:
        report_content += f"- **{location}** : {count} emplois ({(count/analysis_summary['total_jobs']*100):.1f}%)\\n"

    # Recommandations finales
    report_content += f"""

---

## 🎯 RECOMMANDATIONS STRATÉGIQUES

### 🚀 ACTIONS IMMÉDIATES
1. **Postuler en priorité** aux {analysis_summary['class_distribution'].get('A', 0)} emplois de classe A
2. **Examiner attentivement** les {analysis_summary['class_distribution'].get('B', 0)} emplois de classe B
3. **Prioriser** les emplois avec télétravail si recherché ({advanced_stats['remote_jobs']} disponibles)
4. **Cibler** les offres récentes (≤7j) : {advanced_stats['recent_jobs']} emplois

### 📊 OPTIMISATIONS DE RECHERCHE
- **Efficacité actuelle :** {(analysis_summary['class_distribution'].get('A', 0) / analysis_summary['total_jobs'] * 100):.1f}% (objectif: >40%)
- **Score moyen :** {analysis_summary['average_score']:.1f} (objectif: >15)
- **Verdict :** {'✅ Configuration optimale' if (analysis_summary['class_distribution'].get('A', 0) / analysis_summary['total_jobs'] * 100) > 40 else '⚠️ Configuration à améliorer'}

### 🔧 AMÉLIORATIONS SUGGÉRÉES
{'- Mots-clés parfaitement adaptés, continuez ainsi !' if (analysis_summary['class_distribution'].get('A', 0) / analysis_summary['total_jobs'] * 100) > 40 else '- Ajuster les mots-clés pour améliorer la pertinence'}

---

## 📁 DONNÉES TECHNIQUES

### 📊 STATISTIQUES D'EXTRACTION
- **Total emplois recherchés :** {analysis_summary['total_jobs']}
- **Détails extraits avec succès :** {advanced_stats['successful_extractions']}
- **Taux de réussite extraction :** {advanced_stats['extraction_rate']:.1f}%
- **Emplois avec URL candidature directe :** {advanced_stats['jobs_with_apply_url']}
- **Emplois republications détectées :** {advanced_stats['reposted_jobs']}

### 🔗 FICHIERS GÉNÉRÉS
- **Données JSON complètes :** `data/exports/analyse_pertinence_complete_{timestamp}.json`
- **Rapport Markdown :** Ce document
- **Horodatage :** {timestamp}

---

*Rapport généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}*  
*Système d'analyse LinkedIn avec extraction complète de tous les champs disponibles*  
*Version Enhanced avec URLs LinkedIn, télétravail, fraîcheur et candidature directe*
"""

    return report_content

def calculate_advanced_statistics(jobs_data):
    """Calcule des statistiques avancées pour le rapport"""
    stats = {
        'extraction_rate': 0,
        'successful_extractions': 0,
        'remote_jobs': 0,
        'hybrid_jobs': 0,
        'onsite_jobs': 0,
        'today_jobs': 0,
        'very_recent_jobs': 0,
        'recent_jobs': 0,
        'average_age': 0,
        'jobs_with_apply_url': 0,
        'reposted_jobs': 0
    }
    
    total_jobs = len(jobs_data)
    total_age_days = 0
    jobs_with_dates = 0
    
    for job in jobs_data:
        info = job['enhanced_info']
        
        # Taux d'extraction
        if info.get('raw_detailed_info'):
            stats['successful_extractions'] += 1
        
        # Mode de travail
        if info['work_remote_allowed']:
            stats['remote_jobs'] += 1
        elif 'Hybrid' in info.get('work_type', ''):
            stats['hybrid_jobs'] += 1
        else:
            stats['onsite_jobs'] += 1
        
        # Fraîcheur
        days_since = info.get('days_since_posted', 0)
        if days_since == 0:
            stats['today_jobs'] += 1
        if days_since <= 3:
            stats['very_recent_jobs'] += 1
        if days_since <= 7:
            stats['recent_jobs'] += 1
        
        if days_since > 0:
            total_age_days += days_since
            jobs_with_dates += 1
        
        # URLs et republications
        if info.get('apply_url'):
            stats['jobs_with_apply_url'] += 1
        
        if info.get('is_reposted'):
            stats['reposted_jobs'] += 1
    
    # Calculs finaux
    if total_jobs > 0:
        stats['extraction_rate'] = (stats['successful_extractions'] / total_jobs) * 100
    
    if jobs_with_dates > 0:
        stats['average_age'] = total_age_days / jobs_with_dates
    
    return stats

def search_and_analyze_complete_enhanced():
    """Recherche et analyse complète avec tous les champs LinkedIn (version enhanced)"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 ANALYSE COMPLÈTE ENHANCED - TOUS CHAMPS LINKEDIN")
    print("📋 Mot-clé: SEO")
    print("🌍 Localisation: Paris, Île-de-France, France")
    print("📊 Objectif: 50 emplois avec analyse exhaustive")
    print("⚡ Nouveautés: URLs LinkedIn, télétravail, fraîcheur, candidature directe")
    print("=" * 80)
    
    try:
        # Recherche initiale
        print("🔍 Phase 1: Recherche des emplois (50 emplois)...")
        jobs = linkedin.search_jobs(
            keywords="SEO",
            location="Paris, Île-de-France, France", 
            limit=50
        )
        
        if not jobs:
            print("❌ Aucun emploi trouvé")
            return
        
        print(f"✅ {len(jobs)} emplois trouvés\n")
        
        # Phase 2: Extraction exhaustive des détails
        print("🔍 Phase 2: Extraction exhaustive des détails (TOUS LES CHAMPS)...")
        jobs_with_enhanced_details = []
        
        for i, job in enumerate(jobs, 1):
            print(f"   📋 Emploi {i}/{len(jobs)}: {job.get('title', 'N/A')}")
            
            # Extraction des détails complets
            job_details = extract_job_details(linkedin, job)
            
            # Extraction enhanced de TOUTES les informations
            enhanced_info = extract_enhanced_job_info(job, job_details)
            
            # Analyse de pertinence
            relevance_analysis = analyze_seo_relevance(
                enhanced_info['title'],
                enhanced_info['description'],
                enhanced_info['company_name']
            )
            
            job_complete = {
                'enhanced_info': enhanced_info,
                'relevance_analysis': relevance_analysis
            }
            
            jobs_with_enhanced_details.append(job_complete)
            
            # Affichage enrichi
            linkedin_url = f" | 🔗 {enhanced_info['linkedin_job_url']}" if enhanced_info['linkedin_job_url'] else ""
            remote_info = f" | 🏠 {enhanced_info['work_type']}" if enhanced_info['work_type'] != 'Unknown' else ""
            freshness_info = f" | ⏰ {enhanced_info['freshness_category']}" if enhanced_info['freshness_category'] != 'Unknown' else ""
            
            print(f"      ✅ Score: {relevance_analysis['score']} - {relevance_analysis['relevance']}{linkedin_url}{remote_info}{freshness_info}")
            
            # Pause pour éviter le rate limiting
            time.sleep(1)
        
        print(f"\n✅ Extraction enhanced terminée: {len(jobs_with_enhanced_details)} emplois analysés\n")
        
        # Phase 3: Analyse et classement enrichi
        print("🔍 Phase 3: Analyse et classement enrichi...")
        
        # Classer par score de pertinence
        jobs_with_enhanced_details.sort(key=lambda x: x['relevance_analysis']['score'], reverse=True)
        
        # Statistiques globales
        total_score = sum(job['relevance_analysis']['score'] for job in jobs_with_enhanced_details)
        avg_score = total_score / len(jobs_with_enhanced_details)
        
        # Répartition par classe de pertinence
        class_distribution = {}
        for job in jobs_with_enhanced_details:
            relevance_class = job['relevance_analysis']['relevance_class']
            class_distribution[relevance_class] = class_distribution.get(relevance_class, 0) + 1
        
        # Statistiques avancées
        advanced_stats = calculate_advanced_statistics(jobs_with_enhanced_details)
        
        print(f"📊 STATISTIQUES ENHANCED:")
        print(f"   • Total emplois analysés: {len(jobs_with_enhanced_details)}")
        print(f"   • Score total: {total_score}")
        print(f"   • Score moyen: {avg_score:.2f}")
        print(f"   • Taux d'extraction détails: {advanced_stats['extraction_rate']:.1f}%")
        print(f"   • Emplois avec télétravail: {advanced_stats['remote_jobs']}")
        print(f"   • Emplois avec URLs candidature: {advanced_stats['jobs_with_apply_url']}")
        print(f"   • Âge moyen des offres: {advanced_stats['average_age']:.1f} jours")
        print(f"   • Répartition par classe:")
        for class_letter in sorted(class_distribution.keys()):
            count = class_distribution[class_letter]
            percentage = (count / len(jobs_with_enhanced_details)) * 100
            print(f"     - Classe {class_letter}: {count} emplois ({percentage:.1f}%)")
        
        # Affichage du Top 5 avec informations enrichies
        print(f"\n🏆 TOP 5 AVEC INFORMATIONS COMPLÈTES:")
        for i, job in enumerate(jobs_with_enhanced_details[:5], 1):
            info = job['enhanced_info']
            relevance = job['relevance_analysis']
            
            print(f"\n   {i}. {info['title']} - {info['company_name']}")
            print(f"      💯 Score: {relevance['score']} | 🎯 Classe: {relevance['relevance_class']} | 📊 Pertinence: {relevance['relevance']}")
            print(f"      🔗 LinkedIn: {info['linkedin_job_url']}")
            print(f"      📍 Localisation: {info['formatted_location']}")
            print(f"      💼 Mode travail: {info['work_type']} {'(Télétravail ✅)' if info['work_remote_allowed'] else ''}")
            print(f"      📅 Publié: {info['posted_date']} ({info['freshness_category']})")
            if info['apply_url']:
                print(f"      🎯 Candidature: {info['apply_url'][:60]}...")
        
        # Phase 4: Sauvegarde complète
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/exports/analyse_pertinence_complete_{timestamp}.json"
        
        # Données pour sauvegarde JSON
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'search_params': {
                'keywords': 'SEO',
                'location': 'Paris, Île-de-France, France',
                'limit': 50
            },
            'analysis_summary': {
                'total_jobs': len(jobs_with_enhanced_details),
                'total_score': total_score,
                'average_score': avg_score,
                'class_distribution': class_distribution,
                'advanced_statistics': advanced_stats
            },
            'jobs_analyzed': jobs_with_enhanced_details
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Données complètes sauvegardées: {filename}")
        
        # Phase 5: Génération du rapport Markdown enhanced
        print("🔍 Phase 5: Génération du rapport Markdown complet...")
        
        report_content = generate_enhanced_markdown_report(
            jobs_with_enhanced_details, 
            save_data['search_params'],
            save_data['analysis_summary'], 
            timestamp
        )
        
        report_filename = f"RAPPORT_ANALYSE_COMPLETE_{timestamp}.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📝 Rapport Markdown enhanced généré: {report_filename}")
        print(f"🎯 Contient: URLs LinkedIn, télétravail, fraîcheur, candidature directe, analyses avancées")
        
        return jobs_with_enhanced_details
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    results = search_and_analyze_complete_enhanced()