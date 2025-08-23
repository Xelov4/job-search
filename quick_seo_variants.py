#!/usr/bin/env python3
"""
Version rapide de la recherche SEO avec variantes principales
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

def quick_seo_variants():
    """Test rapide des meilleures variantes SEO"""
    
    linkedin = Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=False
    )
    
    print("🚀 RECHERCHE SEO RAPIDE - VARIANTES PRINCIPALES")
    print("📋 Basée sur opérateurs LinkedIn officiels")
    print("=" * 80)
    
    # Sélection des variantes les plus prometteuses
    priority_searches = [
        {
            'name': 'Phrases exactes SEO',
            'query': '"SEO Specialist"',
            'rationale': 'Recherche exacte pour éviter la dilution'
        },
        {
            'name': 'Exclusion Casino Manager', 
            'query': 'SEO NOT (casino OR gaming)',
            'rationale': 'Éliminer le bruit identifié précédemment'
        },
        {
            'name': 'SEO Senior/Manager',
            'query': '(SEO OR référenceur) AND (senior OR manager OR lead)',
            'rationale': 'Cibler les profils expérimentés'
        },
        {
            'name': 'Multilingue avec exclusions',
            'query': '(SEO OR "référenceur SEO" OR "Search Engine Optimization") NOT (stage OR junior)',
            'rationale': 'Combinaison FR/EN sans débutants'
        },
        {
            'name': 'Growth + SEO',
            'query': '("Growth Manager" OR "Performance Marketing") AND SEO',
            'rationale': 'Rôles growth incluant du SEO'
        },
        {
            'name': 'Exclusion complète bruit',
            'query': 'SEO NOT (casino OR gaming OR "spontaneous application" OR "general manager")',
            'rationale': 'Élimination de tout le bruit identifié'
        }
    ]
    
    results = {}
    
    for search in priority_searches:
        print(f"\n🔍 {search['name']}")
        print(f"   📋 Requête: {search['query']}")
        print(f"   💡 Logique: {search['rationale']}")
        
        try:
            jobs = linkedin.search_jobs(
                keywords=search['query'],
                location="Paris, France", 
                limit=20
            )
            
            if jobs:
                print(f"   ✅ {len(jobs)} emplois trouvés")
                
                # Analyse rapide des 5 premiers titres
                seo_count = 0
                relevant_titles = []
                
                for job in jobs[:5]:
                    title = job.get('title', '')
                    if any(term in title.lower() for term in ['seo', 'référenceur', 'search engine']):
                        seo_count += 1
                        relevant_titles.append(title)
                
                print(f"   🎯 SEO direct dans top 5: {seo_count}/5")
                
                if relevant_titles:
                    print(f"   📋 Titres pertinents:")
                    for title in relevant_titles[:3]:
                        print(f"      • {title}")
                else:
                    # Afficher quelques titres pour analyse
                    print(f"   📋 Premiers titres (analyse):")
                    for job in jobs[:3]:
                        print(f"      • {job.get('title', 'N/A')}")
                
                results[search['name']] = {
                    'query': search['query'],
                    'count': len(jobs),
                    'seo_in_top5': seo_count,
                    'jobs': jobs[:5],  # Garder seulement les 5 premiers pour analyse
                    'effectiveness': seo_count / 5 * 100
                }
                
            else:
                print(f"   ❌ Aucun résultat")
                results[search['name']] = {
                    'query': search['query'],
                    'count': 0,
                    'effectiveness': 0
                }
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results[search['name']] = {
                'query': search['query'],
                'error': str(e),
                'effectiveness': 0
            }
        
        time.sleep(3)  # Pause entre recherches
    
    # Analyse comparative
    print(f"\n{'=' * 80}")
    print("📊 ANALYSE COMPARATIVE")
    print(f"{'=' * 80}")
    
    # Trier par efficacité
    valid_results = [(name, data) for name, data in results.items() 
                    if 'effectiveness' in data and data['count'] > 0]
    valid_results.sort(key=lambda x: x[1]['effectiveness'], reverse=True)
    
    print(f"🏆 CLASSEMENT PAR EFFICACITÉ:")
    
    for i, (name, data) in enumerate(valid_results, 1):
        effectiveness = data['effectiveness']
        count = data['count']
        seo_direct = data.get('seo_in_top5', 0)
        
        if effectiveness >= 60:
            emoji = "🥇"
        elif effectiveness >= 40:
            emoji = "🥈"
        elif effectiveness >= 20:
            emoji = "🥉"
        else:
            emoji = "📊"
        
        print(f"\n{i}. {emoji} {name}")
        print(f"   📈 Efficacité: {effectiveness:.1f}% ({seo_direct}/5 SEO direct)")
        print(f"   📊 Résultats: {count} emplois")
        print(f"   🔍 Requête: {data['query']}")
    
    # Identifier la meilleure stratégie
    if valid_results:
        best_name, best_data = valid_results[0]
        print(f"\n{'=' * 80}")
        print(f"🎯 MEILLEURE STRATÉGIE IDENTIFIÉE")
        print(f"{'=' * 80}")
        print(f"🏆 {best_name}")
        print(f"📈 Efficacité: {best_data['effectiveness']:.1f}%")
        print(f"🔍 Requête: {best_data['query']}")
        print(f"📊 {best_data['count']} emplois trouvés")
        
        if best_data['effectiveness'] >= 40:
            print(f"✅ RECOMMANDATION: Utiliser cette requête pour les futures recherches")
        else:
            print(f"⚠️ ATTENTION: Même la meilleure variante a une efficacité limitée ({best_data['effectiveness']:.1f}%)")
    
    # Comparaison avec nos précédents résultats
    print(f"\n📊 COMPARAISON AVEC RECHERCHES PRÉCÉDENTES:")
    print(f"   • Recherche simple 'SEO': 54.5% efficacité (6/20 pertinents)")
    print(f"   • Recherche 'SEO Search Engine Optimization': 18.0% efficacité (1/20 pertinent)")
    
    if valid_results:
        best_effectiveness = valid_results[0][1]['effectiveness']
        print(f"   • Meilleure variante actuelle: {best_effectiveness:.1f}% efficacité")
        
        if best_effectiveness > 54.5:
            print(f"   🎉 AMÉLIORATION SIGNIFICATIVE détectée !")
        elif best_effectiveness > 30:
            print(f"   🟡 Amélioration modérée")
        else:
            print(f"   🔴 Pas d'amélioration significative")
    
    # Sauvegarde
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/exports/seo_variants_quick_{timestamp}.json"
    
    save_data = {
        'timestamp': datetime.now().isoformat(),
        'searches_tested': len(priority_searches),
        'results': results,
        'ranking': [(name, data['effectiveness']) for name, data in valid_results],
        'best_query': valid_results[0][1]['query'] if valid_results else None
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Résultats sauvegardés: {filename}")
    
    return results

if __name__ == "__main__":
    results = quick_seo_variants()