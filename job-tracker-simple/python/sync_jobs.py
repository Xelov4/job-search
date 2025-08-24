#!/usr/bin/env python3
"""
Script Principal de Synchronisation
Orchestre la synchronisation LinkedIn Enhanced → Supabase
"""

import sys
import os
import argparse
import json
from datetime import datetime
from pathlib import Path

# Ajout des chemins nécessaires
current_dir = Path(__file__).parent
linkedin_mcp_dir = current_dir.parent.parent / "linkedin-mcp"
sys.path.insert(0, str(linkedin_mcp_dir))
sys.path.insert(0, str(current_dir))

from linkedin_integration import LinkedInSupabaseSync
from supabase_client import SimpleJobManager

def find_latest_enhanced_json() -> str:
    """Trouve le fichier JSON Enhanced le plus récent"""
    
    exports_dir = linkedin_mcp_dir / "data" / "exports"
    
    if not exports_dir.exists():
        raise FileNotFoundError(f"Répertoire exports non trouvé: {exports_dir}")
    
    # Recherche des fichiers Enhanced
    enhanced_files = list(exports_dir.glob("analyse_pertinence_complete_*_*.json"))
    
    if not enhanced_files:
        raise FileNotFoundError("Aucun fichier Enhanced trouvé dans data/exports/")
    
    # Tri par date de modification (plus récent en premier)
    latest_file = max(enhanced_files, key=lambda f: f.stat().st_mtime)
    
    return str(latest_file)

def run_enhanced_analysis() -> str:
    """Lance l'analyse Enhanced et retourne le chemin du fichier généré"""
    
    print("🚀 Lancement de l'analyse Enhanced...")
    
    # Import et exécution du workflow Enhanced
    try:
        from analyse_pertinence_complete_enhanced import search_and_analyze_complete_enhanced
        
        # Lancer l'analyse (celle-ci génère automatiquement le JSON)
        jobs_enhanced = search_and_analyze_complete_enhanced()
        
        if jobs_enhanced:
            # Trouver le fichier généré (le plus récent)
            latest_json = find_latest_enhanced_json()
            print(f"✅ Analyse Enhanced terminée: {latest_json}")
            return latest_json
        else:
            raise Exception("L'analyse Enhanced n'a retourné aucun résultat")
            
    except ImportError as e:
        raise Exception(f"Module Enhanced non trouvé: {e}")
    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse Enhanced: {e}")

def sync_from_file(json_file: str) -> dict:
    """Synchronise depuis un fichier JSON spécifique"""
    
    print(f"📂 Synchronisation depuis: {json_file}")
    
    sync_manager = LinkedInSupabaseSync()
    stats = sync_manager.sync_from_enhanced_json(json_file)
    
    return stats

def sync_latest() -> dict:
    """Synchronise depuis le fichier Enhanced le plus récent"""
    
    try:
        latest_json = find_latest_enhanced_json()
        print(f"📂 Fichier Enhanced le plus récent: {latest_json}")
        
        return sync_from_file(latest_json)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return {"total": 0, "new": 0, "updated": 0, "errors": 1}

def sync_fresh() -> dict:
    """Lance une nouvelle analyse Enhanced puis synchronise"""
    
    try:
        # Phase 1: Analyse Enhanced
        enhanced_json = run_enhanced_analysis()
        
        # Phase 2: Synchronisation
        print(f"\n🔄 Synchronisation vers Supabase...")
        stats = sync_from_file(enhanced_json)
        
        return stats
        
    except Exception as e:
        print(f"❌ Erreur sync fresh: {e}")
        return {"total": 0, "new": 0, "updated": 0, "errors": 1}

def show_stats():
    """Affiche les statistiques de la base de données"""
    
    print("📊 STATISTIQUES BASE DE DONNÉES")
    print("=" * 50)
    
    job_manager = SimpleJobManager()
    
    if not job_manager.test_connection():
        print("❌ Impossible de se connecter à la base de données")
        return
    
    try:
        stats = job_manager.get_dashboard_stats()
        
        print(f"Total emplois: {stats.get('total_jobs', 0)}")
        print(f"Découverts: {stats.get('discovered_count', 0)}")
        print(f"Intéressants: {stats.get('interested_count', 0)}")
        print(f"Candidatures: {stats.get('applied_count', 0)}")
        print(f"Entretiens: {stats.get('interview_count', 0)}")
        print(f"Remote: {stats.get('remote_count', 0)}")
        print(f"Candidature directe: {stats.get('direct_apply_count', 0)}")
        print(f"Priorité moyenne: {stats.get('avg_priority', 0):.1f}")
        
    except Exception as e:
        print(f"❌ Erreur récupération stats: {e}")

def main():
    """Fonction principale avec gestion des arguments"""
    
    parser = argparse.ArgumentParser(
        description="Synchronisation LinkedIn Enhanced → Supabase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Synchronisation rapide (dernier fichier Enhanced)
  python sync_jobs.py --latest

  # Nouvelle analyse + synchronisation (recommandé)
  python sync_jobs.py --fresh

  # Synchronisation d'un fichier spécifique  
  python sync_jobs.py --file data/exports/analyse_*.json

  # Afficher les statistiques
  python sync_jobs.py --stats

  # Test de connexion
  python sync_jobs.py --test
        """
    )
    
    parser.add_argument('--latest', action='store_true',
                       help='Synchroniser le fichier Enhanced le plus récent')
    parser.add_argument('--fresh', action='store_true',
                       help='Lancer nouvelle analyse Enhanced puis synchroniser')
    parser.add_argument('--file', type=str,
                       help='Synchroniser un fichier JSON spécifique')
    parser.add_argument('--stats', action='store_true',
                       help='Afficher les statistiques de la base')
    parser.add_argument('--test', action='store_true',
                       help='Tester la connexion Supabase')
    
    args = parser.parse_args()
    
    # Vérification des arguments
    if not any([args.latest, args.fresh, args.file, args.stats, args.test]):
        print("❌ Aucune action spécifiée. Utiliser --help pour voir les options.")
        return
    
    print("🎯 JOB TRACKER - SYNCHRONISATION LINKEDIN → SUPABASE")
    print("=" * 60)
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Exécution selon les arguments
    try:
        if args.test:
            job_manager = SimpleJobManager()
            success = job_manager.test_connection()
            if success:
                print("🎉 Connexion Supabase opérationnelle!")
            else:
                print("❌ Problème de connexion Supabase")
            return
        
        if args.stats:
            show_stats()
            return
        
        # Synchronisation
        stats = None
        
        if args.fresh:
            stats = sync_fresh()
        elif args.latest:
            stats = sync_latest()
        elif args.file:
            if os.path.exists(args.file):
                stats = sync_from_file(args.file)
            else:
                print(f"❌ Fichier non trouvé: {args.file}")
                return
        
        # Affichage du résumé final
        if stats:
            print(f"\n🏁 SYNCHRONISATION TERMINÉE")
            print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 Résumé:")
            print(f"   Total traités: {stats.get('total', 0)}")
            print(f"   Nouveaux: {stats.get('new', 0)}")
            print(f"   Mis à jour: {stats.get('updated', 0)}")
            print(f"   Erreurs: {stats.get('errors', 0)}")
            
            if stats.get('total', 0) > 0:
                success_rate = ((stats.get('new', 0) + stats.get('updated', 0)) / stats.get('total', 1)) * 100
                print(f"   Taux succès: {success_rate:.1f}%")
            
            print(f"\n🔗 Interface web: http://localhost:3000")
            print(f"📊 Supabase: {os.getenv('SUPABASE_URL', 'Non configuré')}")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Synchronisation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()