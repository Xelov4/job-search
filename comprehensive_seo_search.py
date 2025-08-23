#!/usr/bin/env python3
"""
Recherche SEO exhaustive avec toutes les variantes de mots-clés
Utilisant les opérateurs LinkedIn officiels
"""
import sys
sys.path.insert(0, 'src')

from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

load_dotenv('config/.env')

def comprehensive_seo_search():
    """Recherche exhaustive SEO avec variantes de mots-clés et opérateurs LinkedIn"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🔍 RECHERCHE SEO EXHAUSTIVE - TOUTES LES VARIANTES")
    print("📋 Basée sur les opérateurs LinkedIn officiels")
    print("=" * 90)
    
    # Définir toutes les variantes SEO possibles
    seo_variations = {
        'exact_titles': [
            '"SEO Specialist"',
            '"SEO Manager"', 
            '"SEO Consultant"',
            '"Senior SEO Specialist"',
            '"SEO Expert"',
            '"Search Engine Optimization Specialist"',
            '"Référenceur SEO"',
            '"Chef de projet SEO"',
            '"SEO Content Manager"',
            '"Technical SEO Specialist"'
        ],
        'role_variants': [
            '("SEO Specialist" OR "SEO Manager" OR "SEO Consultant")',
            '("Senior SEO" OR "Lead SEO" OR "Head of SEO")',
            '("Search Engine Optimization" OR "référenceur" OR "SEO")',
            '("Growth Manager" AND SEO)',
            '("Digital Marketing Manager" AND SEO)',
            '("Content Manager" AND SEO)',
            '("Marketing Manager" AND "search engine")'
        ],
        'comprehensive_search': [
            # Super recherche combinant tout
            '("SEO Specialist" OR "SEO Manager" OR "SEO Consultant" OR "référenceur SEO" OR "Search Engine Optimization Specialist") NOT (stage OR junior OR alternance)',
            
            # Recherche par niveau d'expérience
            '(SEO OR référenceur) AND (senior OR "chef de projet" OR manager OR lead OR head) NOT stage',
            
            # Recherche technique vs content
            '("Technical SEO" OR "SEO technique" OR "SEO Content" OR "Content SEO")',
            
            # Recherche par domaine
            'SEO AND (e-commerce OR ecommerce OR agency OR agence OR SaaS OR startup)',
            
            # Exclusion des faux positifs identifiés
            'SEO NOT (casino OR gaming OR "spontaneous application" OR "general manager" OR sales)'
        ],
        'growth_related': [
            # Variantes Growth qui peuvent inclure du SEO
            '"Growth Manager" AND (SEO OR "search engine" OR "organic traffic")',
            '"Performance Marketing" AND SEO',
            '"Digital Marketing" AND ("search engine optimization" OR SEO)',
            '"Acquisition Manager" AND (SEO OR "organic search")',
            '"Content Marketing" AND SEO'
        ]
    }
    
    all_results = {}
    total_jobs_found = 0
    
    # Tester chaque catégorie
    for category, searches in seo_variations.items():
        print(f"\n📂 CATÉGORIE : {category.upper().replace('_', ' ')}")
        print("-" * 70)
        
        category_results = {}
        
        for i, search_query in enumerate(searches, 1):
            print(f"\n🔍 Test {i}/{len(searches)}: {search_query[:60]}{'...' if len(search_query) > 60 else ''}")
            
            try:
                # Effectuer la recherche
                jobs = linkedin.search_jobs(
                    keywords=search_query,
                    location="Paris, France",
                    limit=20
                )
                
                if jobs:
                    print(f"   ✅ {len(jobs)} emplois trouvés")
                    
                    # Analyse rapide de pertinence
                    relevant_count = 0
                    seo_in_title_count = 0
                    
                    for job in jobs[:10]:  # Analyser les 10 premiers
                        title = job.get('title', '').lower()
                        if any(term in title for term in ['seo', 'référenceur', 'search engine', 'référencement']):
                            seo_in_title_count += 1
                        
                        # Critères de pertinence plus larges
                        if any(term in title for term in ['seo', 'référenceur', 'search engine', 'marketing', 'growth', 'content']):
                            relevant_count += 1
                    
                    print(f"   📊 Top 10 - SEO dans titre: {seo_in_title_count}/10, Pertinents: {relevant_count}/10")
                    
                    # Afficher quelques titres intéressants
                    interesting_titles = []
                    for job in jobs[:5]:
                        title = job.get('title', '')
                        if any(term in title.lower() for term in ['seo', 'référenceur', 'search engine']):
                            interesting_titles.append(title)
                    
                    if interesting_titles:
                        print(f"   🎯 Titres pertinents:")
                        for title in interesting_titles[:3]:
                            print(f"      • {title}")
                    
                    category_results[f"search_{i}"] = {
                        'query': search_query,
                        'count': len(jobs),
                        'seo_in_title_top10': seo_in_title_count,
                        'relevant_top10': relevant_count,
                        'jobs': jobs
                    }
                    
                    total_jobs_found += len(jobs)
                    
                else:
                    print(f"   ❌ Aucun résultat")
                    category_results[f"search_{i}"] = {
                        'query': search_query,
                        'count': 0,
                        'jobs': []
                    }
                
                # Pause entre recherches
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                category_results[f"search_{i}"] = {
                    'query': search_query,
                    'error': str(e)
                }
        
        all_results[category] = category_results
    
    # Analyse comparative des catégories
    print(f"\n{'=' * 90}")
    print("📊 RÉSUMÉ PAR CATÉGORIE")
    print(f"{'=' * 90}")
    
    best_searches = []
    
    for category, results in all_results.items():
        valid_searches = [r for r in results.values() if 'count' in r and r['count'] > 0]
        
        if valid_searches:
            avg_results = sum(r['count'] for r in valid_searches) / len(valid_searches)
            avg_seo_in_title = sum(r.get('seo_in_title_top10', 0) for r in valid_searches) / len(valid_searches)
            avg_relevant = sum(r.get('relevant_top10', 0) for r in valid_searches) / len(valid_searches)
            
            print(f"\n📂 {category.replace('_', ' ').upper()}:")
            print(f"   📊 Recherches réussies: {len(valid_searches)}")
            print(f"   📈 Moyenne résultats: {avg_results:.1f} emplois")
            print(f"   🎯 SEO dans titre (top 10): {avg_seo_in_title:.1f}/10")
            print(f"   ✅ Pertinence globale: {avg_relevant:.1f}/10")
            
            # Identifier les meilleures recherches de cette catégorie
            for search_key, search_data in results.items():
                if 'count' in search_data and search_data['count'] > 0:
                    score = (search_data.get('seo_in_title_top10', 0) * 2 + 
                            search_data.get('relevant_top10', 0)) / 3
                    
                    if score >= 3:  # Score significatif
                        best_searches.append({
                            'category': category,
                            'query': search_data['query'],
                            'score': score,
                            'count': search_data['count'],
                            'seo_in_title': search_data.get('seo_in_title_top10', 0)
                        })
    
    # Top des meilleures recherches
    print(f"\n{'=' * 90}")
    print("🏆 TOP DES MEILLEURES RECHERCHES")
    print(f"{'=' * 90}")
    
    best_searches.sort(key=lambda x: x['score'], reverse=True)
    
    for i, search in enumerate(best_searches[:5], 1):
        print(f"\n{i}. Score: {search['score']:.1f}/10")
        print(f"   📋 Requête: {search['query']}")
        print(f"   📊 Résultats: {search['count']} emplois")
        print(f"   🎯 SEO dans titre: {search['seo_in_title']}/10")
        print(f"   📂 Catégorie: {search['category']}")
    
    # Sauvegarder tous les résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/exports/comprehensive_seo_search_{timestamp}.json"
    
    # Préparer les données pour la sauvegarde
    save_data = {
        'search_timestamp': datetime.now().isoformat(),
        'total_searches': sum(len(cat_results) for cat_results in all_results.values()),
        'total_jobs_found': total_jobs_found,
        'categories': all_results,
        'best_searches': best_searches[:10],
        'search_parameters': {
            'location': "Paris, France",
            'limit_per_search': 20
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Résultats complets sauvegardés: {filename}")
    print(f"📊 Total: {sum(len(cat_results) for cat_results in all_results.values())} recherches")
    print(f"📊 Emplois trouvés: {total_jobs_found}")
    
    # Recommandations finales
    print(f"\n{'=' * 90}")
    print("💡 RECOMMANDATIONS FINALES")
    print(f"{'=' * 90}")
    
    if best_searches:
        best_query = best_searches[0]['query']
        print(f"🏆 Meilleure requête identifiée:")
        print(f"   {best_query}")
        print(f"   Score: {best_searches[0]['score']:.1f}/10")
        print(f"   SEO direct: {best_searches[0]['seo_in_title']}/10 dans le top 10")
        
        # Effectuer une extraction complète avec la meilleure requête
        print(f"\n🔄 Lancement extraction complète avec la meilleure requête...")
        return run_full_extraction(best_query)
    else:
        print("⚠️ Aucune recherche n'a donné de résultats suffisamment pertinents")
        return None

def extract_complete_job_info(job_details):
    """Extraction complète des informations (version simplifiée)"""
    if not job_details or not isinstance(job_details, dict):
        return {}
    
    # Extraction des informations de base
    basic_info = {
        'title': job_details.get('title', 'N/A'),
        'job_id': job_details.get('jobPostingId', 'N/A'),
        'entity_urn': job_details.get('entityUrn', 'N/A'),
        'job_state': job_details.get('jobState', 'N/A')
    }
    
    # Extraction entreprise (simplifiée)
    company_details = job_details.get('companyDetails', {})
    company_info = {'name': 'N/A', 'logo_urls': []}
    
    if company_details:
        for key in company_details:
            if isinstance(company_details[key], dict):
                comp_result = company_details[key].get('companyResolutionResult', {})
                if isinstance(comp_result, dict) and 'name' in comp_result:
                    company_info['name'] = comp_result['name']
                    break
    
    # Description
    description = job_details.get('description', {})
    desc_text = ''
    if isinstance(description, dict):
        desc_text = description.get('text', '')
    elif isinstance(description, str):
        desc_text = description
    
    return {
        'basic_info': basic_info,
        'company': company_info,
        'description': {'text': desc_text},
        'workplace': {
            'formatted_location': job_details.get('formattedLocation', 'N/A'),
            'detailed_types': []
        }
    }

def run_full_extraction(best_query):
    """Effectue l'extraction complète avec la meilleure requête identifiée"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print(f"\n🎯 EXTRACTION COMPLÈTE AVEC LA MEILLEURE REQUÊTE")
    print(f"📋 Requête: {best_query}")
    print("-" * 70)
    
    # Recherche avec la meilleure requête
    search_results = linkedin.search_jobs(
        keywords=best_query,
        location="Paris, France",
        limit=20
    )
    
    if not search_results:
        print("❌ Aucun résultat pour l'extraction complète")
        return None
    
    print(f"✅ {len(search_results)} emplois trouvés pour extraction détaillée")
    
    all_jobs_complete = []
    
    # Extraction détaillée
    for i, job in enumerate(search_results, 1):
        print(f"\n📋 EXTRACTION {i}/{len(search_results)}")
        
        basic_job_data = {
            'search_result_data': job,
            'detailed_data': None,
            'extraction_timestamp': datetime.now().isoformat(),
            'search_query_used': best_query
        }
        
        # Récupérer détails
        if 'entityUrn' in job:
            job_id = job['entityUrn'].split(':')[-1]
            try:
                job_details = linkedin.get_job(job_id)
                if job_details:
                    complete_info = extract_complete_job_info(job_details)
                    basic_job_data['detailed_data'] = complete_info
                    
                    title = complete_info['basic_info']['title']
                    company = complete_info['company']['name']
                    print(f"   ✅ {title} - {company}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                basic_job_data['error'] = str(e)
        
        all_jobs_complete.append(basic_job_data)
    
    # Sauvegarde extraction complète
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/exports/best_seo_extraction_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_jobs_complete, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Extraction complète sauvegardée: {filename}")
    return filename

if __name__ == "__main__":
    result_file = comprehensive_seo_search()