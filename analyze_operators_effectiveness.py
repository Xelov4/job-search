#!/usr/bin/env python3
"""
Analyse approfondie de l'efficacité des opérateurs LinkedIn
"""
import json
from datetime import datetime

def analyze_operators_impact():
    """Analyse rigoureuse de l'impact des opérateurs LinkedIn"""
    
    print("🔬 ANALYSE RIGOUREUSE - IMPACT DES OPÉRATEURS LINKEDIN")
    print("=" * 90)
    
    # Résultats de nos 3 tests comparatifs
    test_results = {
        'simple_seo': {
            'query': 'SEO',
            'total_jobs': 20,
            'highly_relevant': 6,
            'moderately_relevant': 4, 
            'poorly_relevant': 7,
            'completely_irrelevant': 3,
            'effectiveness': 54.5,
            'seo_in_title': 3,
            'casino_manager_present': True
        },
        'compound_keywords': {
            'query': 'SEO Search Engine Optimization',
            'total_jobs': 20,
            'highly_relevant': 1,
            'moderately_relevant': 2,
            'poorly_relevant': 10,
            'completely_irrelevant': 7,
            'effectiveness': 18.0,
            'seo_in_title': 1,
            'casino_manager_present': True
        },
        'linkedin_operators': {
            'exact_phrase': {
                'query': '"SEO Specialist"',
                'total_jobs': 1,
                'seo_direct': 1,
                'effectiveness': 100.0,  # 1/1 pertinent
                'casino_manager_present': False
            },
            'exclusion_operators': {
                'query': 'SEO NOT (casino OR gaming)',
                'total_jobs': 0,
                'effectiveness': 0.0,
                'casino_manager_present': False
            },
            'complex_boolean': {
                'query': '(SEO OR référenceur) AND (senior OR manager OR lead)',
                'total_jobs': 0,
                'effectiveness': 0.0
            }
        }
    }
    
    print("📊 RÉSULTATS COMPARATIFS DÉTAILLÉS")
    print("-" * 90)
    
    # Test 1: Simple SEO
    print(f"\n🔍 TEST 1: Recherche simple 'SEO'")
    print(f"   📊 Résultats: {test_results['simple_seo']['total_jobs']} emplois")
    print(f"   ✅ Hautement pertinents: {test_results['simple_seo']['highly_relevant']}/20 (30%)")
    print(f"   🎯 SEO dans titre: {test_results['simple_seo']['seo_in_title']}/20 (15%)")
    print(f"   ❌ Complètement hors sujet: {test_results['simple_seo']['completely_irrelevant']}/20 (15%)")
    print(f"   🎰 Casino Manager présent: {'Oui' if test_results['simple_seo']['casino_manager_present'] else 'Non'}")
    print(f"   📈 Efficacité globale: {test_results['simple_seo']['effectiveness']}%")
    
    # Test 2: Mots-clés composés
    print(f"\n🔍 TEST 2: Recherche composée 'SEO Search Engine Optimization'")
    print(f"   📊 Résultats: {test_results['compound_keywords']['total_jobs']} emplois")
    print(f"   ✅ Hautement pertinents: {test_results['compound_keywords']['highly_relevant']}/20 (5%)")
    print(f"   🎯 SEO dans titre: {test_results['compound_keywords']['seo_in_title']}/20 (5%)")
    print(f"   ❌ Complètement hors sujet: {test_results['compound_keywords']['completely_irrelevant']}/20 (35%)")
    print(f"   🎰 Casino Manager présent: {'Oui' if test_results['compound_keywords']['casino_manager_present'] else 'Non'}")
    print(f"   📈 Efficacité globale: {test_results['compound_keywords']['effectiveness']}%")
    
    # Test 3: Opérateurs LinkedIn
    print(f"\n🔍 TEST 3: Opérateurs LinkedIn officiels")
    
    operators_data = test_results['linkedin_operators']
    
    print(f"   3a. Phrase exacte '\"SEO Specialist\"':")
    print(f"       📊 Résultats: {operators_data['exact_phrase']['total_jobs']} emploi")
    print(f"       ✅ Pertinence: {operators_data['exact_phrase']['effectiveness']}%")
    print(f"       🎰 Casino Manager: {'Absent' if not operators_data['exact_phrase']['casino_manager_present'] else 'Présent'}")
    
    print(f"   3b. Exclusion 'SEO NOT (casino OR gaming)':")
    print(f"       📊 Résultats: {operators_data['exclusion_operators']['total_jobs']} emplois")
    print(f"       ✅ Pertinence: {operators_data['exclusion_operators']['effectiveness']}%")
    print(f"       🚫 Effet: Élimination TOTALE des résultats")
    
    print(f"   3c. Boolean complexe '(SEO OR référenceur) AND (senior OR manager)':")
    print(f"       📊 Résultats: {operators_data['complex_boolean']['total_jobs']} emplois")
    print(f"       ✅ Pertinence: {operators_data['complex_boolean']['effectiveness']}%")
    print(f"       🚫 Effet: Aucun résultat trouvé")
    
    # Analyse des patterns découverts
    print(f"\n{'=' * 90}")
    print("🧠 DÉCOUVERTES CRITIQUES SUR L'ALGORITHME LINKEDIN")
    print(f"{'=' * 90}")
    
    print(f"\n🚨 PATTERN 1: Sur-spécification = Élimination totale")
    print(f"   • Opérateurs d'exclusion (NOT) → 0 résultats")
    print(f"   • Boolean complexes (AND/OR) → 0 résultats")
    print(f"   • CONCLUSION: LinkedIn ne supporte pas vraiment les opérateurs complexes")
    
    print(f"\n🔍 PATTERN 2: Phrases exactes = Ultra-restriction")
    print(f"   • '\"SEO Specialist\"' → 1 seul résultat (mais 100% pertinent)")
    print(f"   • Avantage: Pertinence parfaite, élimine le bruit")
    print(f"   • Inconvénient: Volume très faible")
    
    print(f"\n📊 PATTERN 3: Mots-clés simples = Meilleur compromis")
    print(f"   • 'SEO' seul → 20 résultats, 54.5% efficacité")
    print(f"   • Équilibre volume/pertinence optimal")
    print(f"   • Mais inclusion de bruit (Casino Manager)")
    
    print(f"\n⚠️ PATTERN 4: Algorithme LinkedIn imprévisible")
    print(f"   • Documentation officielle vs réalité = Décalage majeur")
    print(f"   • Opérateurs 'supportés' mais non fonctionnels")
    print(f"   • Comportement différent entre interface web et API")
    
    # Calcul de l'impact réel des opérateurs
    print(f"\n{'=' * 90}")
    print("📈 IMPACT QUANTIFIÉ DES OPÉRATEURS LINKEDIN")
    print(f"{'=' * 90}")
    
    # Efficacité relative
    simple_effectiveness = test_results['simple_seo']['effectiveness']
    exact_phrase_jobs = operators_data['exact_phrase']['total_jobs']
    
    if exact_phrase_jobs > 0:
        volume_reduction = (1 - exact_phrase_jobs / test_results['simple_seo']['total_jobs']) * 100
        quality_improvement = operators_data['exact_phrase']['effectiveness'] - simple_effectiveness
        
        print(f"📊 PHRASES EXACTES vs RECHERCHE SIMPLE:")
        print(f"   📉 Réduction de volume: -{volume_reduction:.1f}% ({test_results['simple_seo']['total_jobs']} → {exact_phrase_jobs})")
        print(f"   📈 Amélioration qualité: +{quality_improvement:.1f}% ({simple_effectiveness:.1f}% → {operators_data['exact_phrase']['effectiveness']:.1f}%)")
        print(f"   ✅ Trade-off: -95% volume pour +45.5% qualité")
    
    # Exclusions - impact négatif
    exclusion_jobs = operators_data['exclusion_operators']['total_jobs']
    print(f"\n📊 OPÉRATEURS D'EXCLUSION:")
    print(f"   📉 Impact volume: {test_results['simple_seo']['total_jobs']} → {exclusion_jobs} (-100%)")
    print(f"   ❌ VERDICT: Inutilisables (élimination totale)")
    
    # Recommandations stratégiques
    print(f"\n{'=' * 90}")
    print("💡 RECOMMANDATIONS STRATÉGIQUES FINALES")
    print(f"{'=' * 90}")
    
    print(f"\n🎯 STRATÉGIE OPTIMALE IDENTIFIÉE:")
    print(f"   1. RECHERCHE DE VOLUME: Utiliser 'SEO' simple")
    print(f"      • Volume: 20 résultats")
    print(f"      • Pertinents: 10-12 emplois utilisables")
    print(f"      • Efficacité: 54.5%")
    
    print(f"\n   2. FILTRAGE POST-RECHERCHE OBLIGATOIRE:")
    print(f"      • Éliminer manuellement: 'Casino Manager', 'Spontaneous Application'")
    print(f"      • Scorer par pertinence: titre > description > métadonnées")
    print(f"      • Réordonner par score de pertinence")
    
    print(f"\n   3. RECHERCHE DE PRÉCISION: Utiliser phrases exactes en complément")
    print(f"      • '\"SEO Specialist\"' → 1 résultat parfait")
    print(f"      • '\"Référenceur SEO\"' → Test recommandé")
    print(f"      • Combiner plusieurs phrases exactes")
    
    print(f"\n❌ STRATÉGIES À ÉVITER:")
    print(f"   • Opérateurs d'exclusion (NOT) → 0 résultats")
    print(f"   • Boolean complexes (AND/OR multiples) → 0 résultats") 
    print(f"   • Mots-clés composés longs → Dégradation qualité")
    
    # Architecture de recherche recommandée
    print(f"\n🏗️ ARCHITECTURE DE RECHERCHE RECOMMANDÉE:")
    print(f"""
    def optimized_linkedin_search():
        results = []
        
        # Phase 1: Volume avec mot-clé simple
        volume_jobs = search_jobs(keywords='SEO', limit=20)
        filtered_volume = post_filter(volume_jobs)  # Éliminer Casino Manager etc
        results.extend(filtered_volume)
        
        # Phase 2: Précision avec phrases exactes
        exact_queries = ['"SEO Specialist"', '"Référenceur SEO"', '"SEO Manager"']
        for query in exact_queries:
            exact_jobs = search_jobs(keywords=query, limit=10)
            results.extend(exact_jobs)
        
        # Phase 3: Déduplication et scoring
        unique_jobs = deduplicate(results)
        scored_jobs = calculate_relevance_score(unique_jobs)
        
        return sort_by_score(scored_jobs)
    """)
    
    # Métriques de suivi
    print(f"\n📊 MÉTRIQUES DE SUIVI RECOMMANDÉES:")
    metrics = {
        'baseline_simple_seo': 54.5,
        'target_with_filtering': 75.0,
        'target_with_exact_phrases': 85.0,
        'acceptable_minimum': 60.0
    }
    
    for metric, value in metrics.items():
        print(f"   • {metric.replace('_', ' ').title()}: {value}%")
    
    # Sauvegarde de l'analyse
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/exports/operators_analysis_final_{timestamp}.json"
    
    analysis_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'test_results': test_results,
        'key_findings': {
            'best_simple_approach': 'SEO (54.5% efficacité)',
            'best_precise_approach': '"SEO Specialist" (100% efficacité, 1 résultat)',
            'operators_effectiveness': 'Très limitée, documentation trompeuse',
            'recommended_strategy': 'Recherche simple + filtrage post-recherche'
        },
        'metrics': metrics
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Analyse complète sauvegardée: {filename}")
    
    return analysis_data

if __name__ == "__main__":
    analysis = analyze_operators_impact()