#!/usr/bin/env python3
"""
Script de démarrage rapide pour le workflow d'analyse de pertinence avancée
"""
import os
import sys
import subprocess
import time
from datetime import datetime

def check_environment():
    """Vérifie que l'environnement est prêt"""
    print("🔍 VÉRIFICATION DE L'ENVIRONNEMENT")
    print("=" * 50)
    
    # Vérifier Python
    try:
        python_version = subprocess.check_output(['python', '--version'], text=True).strip()
        print(f"✅ Python: {python_version}")
    except:
        print("❌ Python non trouvé")
        return False
    
    # Vérifier l'environnement virtuel
    if 'VIRTUAL_ENV' in os.environ:
        print(f"✅ Environnement virtuel activé: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️ Environnement virtuel non activé")
        print("   Exécutez: source venv/bin/activate")
        return False
    
    # Vérifier les dépendances
    try:
        import linkedin_api
        print(f"✅ linkedin-api: {linkedin_api.__version__}")
    except ImportError:
        print("❌ linkedin-api non installé")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv installé")
    except ImportError:
        print("❌ python-dotenv non installé")
        return False
    
    # Vérifier le fichier .env
    if os.path.exists('config/.env'):
        print("✅ Fichier .env trouvé")
    else:
        print("❌ Fichier .env manquant dans config/")
        return False
    
    # Vérifier le dossier data/exports
    if os.path.exists('data/exports'):
        print("✅ Dossier data/exports accessible")
    else:
        print("❌ Dossier data/exports manquant")
        return False
    
    print("✅ Environnement prêt !")
    return True

def show_menu():
    """Affiche le menu principal"""
    print("\n🚀 WORKFLOW D'ANALYSE DE PERTINENCE AVANCÉE LINKEDIN")
    print("=" * 60)
    print("1. 🔍 Lancer l'analyse complète (50 emplois)")
    print("2. 📊 Recherche simple sans analyse")
    print("3. 🔬 Test de variantes de recherche")
    print("4. 📚 Voir la documentation")
    print("5. ⚙️ Vérifier l'environnement")
    print("6. 🚪 Quitter")
    print("=" * 60)

def run_complete_analysis():
    """Lance l'analyse complète de pertinence"""
    print("\n🔍 LANCEMENT DE L'ANALYSE COMPLÈTE")
    print("=" * 50)
    print("📋 Méthode: Extraction des descriptions + scoring avancé")
    print("📊 Objectif: 50 emplois avec analyse de pertinence")
    print("⏱️ Temps estimé: 5-10 minutes")
    print("🎯 Efficacité attendue: >40% d'emplois très pertinents")
    print("=" * 50)
    
    confirm = input("\n🚀 Lancer l'analyse ? (o/n): ").lower()
    if confirm in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Lancement de l'analyse...")
        try:
            result = subprocess.run(['python', 'analyse_pertinence_complete.py'], 
                                  capture_output=False, text=True)
            if result.returncode == 0:
                print("\n✅ Analyse terminée avec succès !")
                print("📁 Résultats sauvegardés dans data/exports/")
            else:
                print("\n❌ Erreur lors de l'analyse")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    else:
        print("❌ Analyse annulée")

def run_simple_search():
    """Lance une recherche simple sans analyse"""
    print("\n📊 RECHERCHE SIMPLE SANS ANALYSE")
    print("=" * 50)
    print("📋 Méthode: Recherche basique LinkedIn")
    print("📊 Objectif: 50 emplois sans scoring")
    print("⏱️ Temps estimé: 1-2 minutes")
    print("=" * 50)
    
    confirm = input("\n🚀 Lancer la recherche simple ? (o/n): ").lower()
    if confirm in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Lancement de la recherche...")
        try:
            result = subprocess.run(['python', 'search_seo_50_jobs.py'], 
                                  capture_output=False, text=True)
            if result.returncode == 0:
                print("\n✅ Recherche terminée avec succès !")
                print("📁 Résultats sauvegardés dans data/exports/")
            else:
                print("\n❌ Erreur lors de la recherche")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    else:
        print("❌ Recherche annulée")

def run_variants_test():
    """Lance le test de variantes de recherche"""
    print("\n🔬 TEST DE VARIANTES DE RECHERCHE")
    print("=" * 50)
    print("📋 Méthode: Comparaison de différentes stratégies")
    print("📊 Objectif: Identifier la meilleure approche")
    print("⏱️ Temps estimé: 2-3 minutes")
    print("=" * 50)
    
    confirm = input("\n🚀 Lancer le test de variantes ? (o/n): ").lower()
    if confirm in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Lancement du test...")
        try:
            result = subprocess.run(['python', 'quick_seo_variants.py'], 
                                  capture_output=False, text=True)
            if result.returncode == 0:
                print("\n✅ Test terminé avec succès !")
                print("📁 Résultats sauvegardés dans data/exports/")
            else:
                print("\n❌ Erreur lors du test")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    else:
        print("❌ Test annulé")

def show_documentation():
    """Affiche les informations sur la documentation"""
    print("\n📚 DOCUMENTATION DISPONIBLE")
    print("=" * 50)
    print("📖 WORKFLOW_ANALYSE_COMPLETE.md - Workflow complet et détaillé")
    print("📊 RAPPORT_ANALYSE_PERTINENCE_COMPLETE.md - Rapport d'analyse détaillé")
    print("📋 RESUME_REVOLUTION_ANALYSE.md - Synthèse exécutive")
    print("🔧 WORKFLOW.md - Workflow original du projet")
    print("=" * 50)
    print("💡 Tous les fichiers sont dans le dossier linkedin-mcp/")
    print("📁 Ouvrez-les avec votre éditeur de texte préféré")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DU WORKFLOW LINKEDIN")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Vérifier l'environnement au démarrage
    if not check_environment():
        print("\n❌ Environnement non prêt. Vérifiez la configuration.")
        return
    
    # Boucle principale
    while True:
        show_menu()
        choice = input("\n🎯 Votre choix (1-6): ").strip()
        
        if choice == '1':
            run_complete_analysis()
        elif choice == '2':
            run_simple_search()
        elif choice == '3':
            run_variants_test()
        elif choice == '4':
            show_documentation()
        elif choice == '5':
            check_environment()
        elif choice == '6':
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide. Veuillez choisir 1-6.")
        
        # Pause avant de revenir au menu
        if choice != '6':
            input("\n⏸️ Appuyez sur Entrée pour continuer...")
            print("\n" + "="*60)

if __name__ == "__main__":
    main()
