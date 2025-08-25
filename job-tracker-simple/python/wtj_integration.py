#!/usr/bin/env python3
"""
Intégration WTJ (Welcome to the Jungle) → Supabase
=====================================================

Créé le : 2025-08-25 09:45:00 UTC
Auteur : Claude Code Assistant
Version : 1.0.0

OBJECTIF :
----------
Normalise et synchronise les données du workflow WTJ vers la base de données Supabase.
Équivalent exact du système linkedin_integration.py mais pour Welcome to the Jungle.
Permet d'intégrer les jobs WTJ dans le même pipeline que LinkedIn Enhanced.

ARCHITECTURE :
--------------
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WTJ Scraper   │───▶│ WTJNormalizer   │───▶│ Supabase DB     │
│ (JobOfferData)  │    │ (Validation +   │    │ (job_offers)    │
│                 │    │  Nettoyage)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

COMPOSANTS PRINCIPAUX :
-----------------------
1. WTJDataNormalizer : Classe de normalisation et validation des données WTJ
   - Extraction source_id intelligent depuis URLs WTJ
   - Normalisation work_mode (remote/hybrid/on-site) basée sur analyse textuelle
   - Nettoyage et validation des champs obligatoires
   - Conversion format WTJ → format Supabase compatible

2. WTJSupabaseSync : Gestionnaire de synchronisation vers base de données
   - Synchronisation batch avec gestion d'erreurs
   - Anti-doublons basé sur source_platform + source_id
   - Statistiques détaillées (nouveaux/mis à jour/erreurs)
   - Compatible avec le système existant SimpleJobManager

WORKFLOW INTÉGRATION :
----------------------
WTJ Jobs → Normalisation → Validation → Supabase → Dashboard Next.js

UTILISATION :
-------------
# Sync depuis liste de jobs WTJ
wtj_sync = WTJSupabaseSync()
stats = wtj_sync.sync_from_wtj_jobs(wtj_jobs_list)

# Sync depuis fichier JSON WTJ
stats = wtj_sync.sync_from_wtj_json("export_wtj.json")

COMPATIBILITÉ :
---------------
- Format JobOfferData unifié avec LinkedIn Enhanced
- Même système de priorités et statuts utilisateur
- Interface Dashboard Next.js identique
- Anti-doublons intelligent inter-sources
"""

import sys
import os
from datetime import datetime, timezone
from typing import List, Dict, Optional
import json

# Ajout du chemin vers le workflow WTJ existant
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wtj/'))

from supabase_client import SimpleJobManager, JobOfferData
from job_data_types import JobOfferData as JobOfferDataTypes

class WTJDataNormalizer:
    """
    Normalise les données WTJ vers le format Supabase
    ================================================
    
    Cette classe est l'équivalent exact de LinkedInDataNormalizer mais pour WTJ.
    Elle transforme les données brutes du scraper WTJ en format compatible Supabase.
    
    Fonctionnalités principales :
    - Extraction intelligente des source_id depuis les URLs WTJ
    - Détection automatique du work_mode basée sur analyse textuelle
    - Validation et nettoyage des données obligatoires
    - Conversion vers le format JobOfferData unifié
    
    Méthodes principales :
    - extract_source_id_from_wtj_data() : Extraction ID unique
    - normalize_work_mode_from_wtj() : Détection mode travail
    - clean_and_validate_wtj_data() : Nettoyage et validation
    - normalize_job() : Normalisation complète vers JobOfferData
    """
    
    @staticmethod
    def extract_source_id_from_wtj_data(wtj_job: Dict) -> Optional[str]:
        """
        Extrait un source_id unique depuis les données WTJ
        ================================================
        
        Args:
            wtj_job: Données job WTJ (JobOfferData ou dict)
            
        Returns:
            str: ID unique au format "wtj_XXXXX"
            
        Logique d'extraction :
        1. Si source_id déjà défini → l'utiliser
        2. Sinon, extraire depuis l'URL (/jobs/slug-id)
        3. Fallback : générer avec timestamp
        
        Exemples URLs WTJ :
        - https://welcometothejungle.com/fr/jobs/consultant-seo-123
        - https://welcometothejungle.com/fr/jobs/manager-seo-paris-456
        """
        # Si c'est déjà un JobOfferData de WTJ
        if hasattr(wtj_job, 'source_id'):
            return wtj_job.source_id
        
        # Si c'est un dict avec source_id
        if isinstance(wtj_job, dict) and 'source_id' in wtj_job:
            return wtj_job['source_id']
        
        # Fallback: générer un ID basé sur l'URL ou autre
        if isinstance(wtj_job, dict):
            url = wtj_job.get('source_url', '')
            if url:
                import re
                # Extraire ID de l'URL
                match = re.search(r'/jobs/([a-zA-Z0-9_-]+)', url)
                if match:
                    return f"wtj_{match.group(1)}"
        
        # Fallback final
        return f"wtj_{datetime.now().timestamp()}"
    
    @staticmethod
    def normalize_work_mode_from_wtj(wtj_job: Dict) -> str:
        """Normalise le mode de travail depuis WTJ"""
        # Si c'est déjà normalisé
        if hasattr(wtj_job, 'work_mode') and wtj_job.work_mode:
            return wtj_job.work_mode
        
        if isinstance(wtj_job, dict) and wtj_job.get('work_mode'):
            return wtj_job['work_mode']
        
        # Analyse basée sur le titre et la description
        title = wtj_job.get('title', '') if isinstance(wtj_job, dict) else getattr(wtj_job, 'title', '')
        description = wtj_job.get('description', '') if isinstance(wtj_job, dict) else getattr(wtj_job, 'description', '')
        location = wtj_job.get('location', '') if isinstance(wtj_job, dict) else getattr(wtj_job, 'location', '')
        
        text_to_analyze = f"{title} {description} {location}".lower()
        
        # Mots-clés pour détection
        remote_keywords = [
            'remote', 'télétravail', 'full remote', 'home office',
            'travail à distance', 'distanciel', 'nomade', '100% remote'
        ]
        
        hybrid_keywords = [
            'hybride', 'flexible', 'partiel', 'mixte',
            'télétravail partiel', 'hybrid', '2-3 jours', 'partiellement remote'
        ]
        
        if any(keyword in text_to_analyze for keyword in remote_keywords):
            return 'remote'
        elif any(keyword in text_to_analyze for keyword in hybrid_keywords):
            return 'hybrid'
        else:
            return 'on-site'
    
    @staticmethod
    def clean_and_validate_wtj_data(wtj_job: Dict) -> Dict:
        """Nettoie et valide les données WTJ"""
        cleaned_data = {}
        
        # Mapping des champs
        if hasattr(wtj_job, '__dict__'):
            # Si c'est un objet JobOfferData
            cleaned_data = {
                'source_platform': getattr(wtj_job, 'source_platform', 'welcometothejungle'),
                'source_id': getattr(wtj_job, 'source_id', ''),
                'source_url': getattr(wtj_job, 'source_url', ''),
                'title': getattr(wtj_job, 'title', ''),
                'company_name': getattr(wtj_job, 'company_name', ''),
                'company_url': getattr(wtj_job, 'company_url', ''),
                'location': getattr(wtj_job, 'location', ''),
                'description': getattr(wtj_job, 'description', ''),
                'work_mode': getattr(wtj_job, 'work_mode', 'on-site'),
                'job_type': getattr(wtj_job, 'job_type', 'full-time'),
                'application_url': getattr(wtj_job, 'application_url', ''),
                'salary_info': getattr(wtj_job, 'salary_info', ''),
                'posted_at': getattr(wtj_job, 'posted_at', None),
                'discovered_at': getattr(wtj_job, 'discovered_at', None)
            }
        elif isinstance(wtj_job, dict):
            # Si c'est un dictionnaire
            cleaned_data = {
                'source_platform': wtj_job.get('source_platform', 'welcometothejungle'),
                'source_id': wtj_job.get('source_id', ''),
                'source_url': wtj_job.get('source_url', ''),
                'title': wtj_job.get('title', ''),
                'company_name': wtj_job.get('company_name', ''),
                'company_url': wtj_job.get('company_url', ''),
                'location': wtj_job.get('location', ''),
                'description': wtj_job.get('description', ''),
                'work_mode': wtj_job.get('work_mode', 'on-site'),
                'job_type': wtj_job.get('job_type', 'full-time'),
                'application_url': wtj_job.get('application_url', ''),
                'salary_info': wtj_job.get('salary_info', ''),
                'posted_at': wtj_job.get('posted_at', None),
                'discovered_at': wtj_job.get('discovered_at', None)
            }
        
        # Validation et nettoyage
        cleaned_data['source_platform'] = 'welcometothejungle'
        
        # S'assurer que les champs requis ne sont pas vides
        if not cleaned_data['source_id']:
            cleaned_data['source_id'] = WTJDataNormalizer.extract_source_id_from_wtj_data(wtj_job)
        
        if not cleaned_data['title']:
            cleaned_data['title'] = 'Job WTJ'
        
        if not cleaned_data['company_name']:
            cleaned_data['company_name'] = 'Entreprise WTJ'
        
        # Normaliser le work_mode
        cleaned_data['work_mode'] = WTJDataNormalizer.normalize_work_mode_from_wtj(wtj_job)
        
        # S'assurer que discovered_at est défini
        if not cleaned_data['discovered_at']:
            cleaned_data['discovered_at'] = datetime.now(timezone.utc).isoformat()
        
        return cleaned_data
    
    @classmethod
    def normalize_job(cls, wtj_job) -> Optional[JobOfferData]:
        """
        Normalise un emploi WTJ vers JobOfferData pour Supabase
        
        Args:
            wtj_job: Job WTJ (JobOfferData ou dict)
        
        Returns:
            JobOfferData normalisé ou None si erreur
        """
        try:
            # Nettoyer et valider les données
            cleaned_data = cls.clean_and_validate_wtj_data(wtj_job)
            
            # Créer l'objet JobOfferData pour Supabase
            return JobOfferData(
                source_platform=cleaned_data['source_platform'],
                source_id=cleaned_data['source_id'],
                source_url=cleaned_data['source_url'],
                title=cleaned_data['title'],
                company_name=cleaned_data['company_name'],
                company_url=cleaned_data.get('company_url', None),
                location=cleaned_data['location'],
                description=cleaned_data['description'],
                work_mode=cleaned_data['work_mode'],
                job_type=cleaned_data['job_type'],
                application_url=cleaned_data['application_url'],
                salary_info=cleaned_data['salary_info'],
                posted_at=cleaned_data.get('posted_at'),
                priority=0,  # Défaut utilisateur
                notes=None
            )
            
        except Exception as e:
            print(f"❌ Erreur normalisation job WTJ: {e}")
            if hasattr(wtj_job, 'title'):
                print(f"   Job title: {getattr(wtj_job, 'title', 'N/A')}")
            elif isinstance(wtj_job, dict):
                print(f"   Job title: {wtj_job.get('title', 'N/A')}")
            return None

class WTJSupabaseSync:
    """
    Gestionnaire de synchronisation WTJ → Supabase
    ===============================================
    
    Cette classe gère la synchronisation complète des jobs WTJ vers la base Supabase.
    Équivalent exact de LinkedInSupabaseSync mais pour Welcome to the Jungle.
    
    Fonctionnalités :
    - Normalisation automatique via WTJDataNormalizer
    - Synchronisation batch avec statistiques détaillées
    - Gestion des erreurs de normalisation
    - Intégration avec SimpleJobManager existant
    - Synchronisation depuis listes de jobs ou fichiers JSON
    
    Workflow :
    Jobs WTJ → Normalisation → Validation → Supabase → Statistiques
    
    Utilisation typique :
    sync = WTJSupabaseSync()
    stats = sync.sync_from_wtj_jobs(job_list)
    # Résultat : {'total': 50, 'new': 30, 'updated': 15, 'errors': 5}
    """
    
    def __init__(self):
        self.job_manager = SimpleJobManager()
        self.normalizer = WTJDataNormalizer()
        print("🔄 Synchronisation WTJ → Supabase initialisée")
    
    def sync_from_wtj_jobs(self, wtj_jobs: List) -> Dict[str, int]:
        """
        Synchronise les jobs WTJ vers Supabase
        
        Args:
            wtj_jobs: Liste des emplois WTJ (JobOfferData ou dict)
            
        Returns:
            Statistiques de synchronisation
        """
        if not wtj_jobs:
            print("⚠️ Aucun job WTJ à synchroniser")
            return {"total": 0, "new": 0, "updated": 0, "errors": 0}
        
        print(f"🔄 Début synchronisation: {len(wtj_jobs)} jobs WTJ")
        
        # Phase 1: Normalisation
        normalized_jobs = []
        normalization_errors = 0
        
        for i, wtj_job in enumerate(wtj_jobs, 1):
            normalized_job = self.normalizer.normalize_job(wtj_job)
            
            if normalized_job:
                normalized_jobs.append(normalized_job)
            else:
                normalization_errors += 1
                print(f"   ❌ [{i}/{len(wtj_jobs)}] Échec normalisation")
        
        print(f"✅ Normalisation terminée: {len(normalized_jobs)} jobs prêts (erreurs: {normalization_errors})")
        
        # Phase 2: Sauvegarde en base
        if normalized_jobs:
            sync_stats = self.job_manager.save_jobs_batch(normalized_jobs)
            sync_stats["normalization_errors"] = normalization_errors
            return sync_stats
        else:
            return {"total": len(wtj_jobs), "new": 0, "updated": 0, "errors": len(wtj_jobs)}
    
    def sync_from_wtj_json(self, json_file_path: str) -> Dict[str, int]:
        """
        Synchronise à partir d'un fichier JSON WTJ exporté
        
        Args:
            json_file_path: Chemin vers le fichier JSON WTJ
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                wtj_data = json.load(f)
            
            # Différents formats possibles
            if 'jobs' in wtj_data:
                jobs_list = wtj_data['jobs']
            elif 'all_jobs_normalized' in wtj_data:
                jobs_list = wtj_data['all_jobs_normalized']
            elif isinstance(wtj_data, list):
                jobs_list = wtj_data
            else:
                jobs_list = []
            
            print(f"📂 Fichier WTJ chargé: {len(jobs_list)} jobs")
            
            return self.sync_from_wtj_jobs(jobs_list)
            
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {json_file_path}")
            return {"total": 0, "new": 0, "updated": 0, "errors": 1}
        except json.JSONDecodeError as e:
            print(f"❌ Erreur lecture JSON: {e}")
            return {"total": 0, "new": 0, "updated": 0, "errors": 1}
        except Exception as e:
            print(f"❌ Erreur sync depuis JSON: {e}")
            return {"total": 0, "new": 0, "updated": 0, "errors": 1}

# Fonction utilitaire pour tests
def test_wtj_normalization():
    """Test de normalisation avec données exemple WTJ"""
    
    # Exemple de données WTJ (structure réelle du module wtj)
    from wtj.fast_scraper import JobOfferData as WTJJobOfferData
    
    test_wtj_job = WTJJobOfferData(
        source_platform='welcometothejungle',
        source_id='wtj_test_123',
        source_url='https://www.welcometothejungle.com/fr/jobs/test-seo-123',
        title='SEO Specialist Test',
        company_name='Test Company WTJ',
        company_url=None,
        location='Paris, France',
        description='Nous recherchons un SEO Specialist expérimenté pour optimiser notre présence en ligne...',
        work_mode='remote',
        job_type='full-time',
        application_url='https://company.com/jobs/apply/seo',
        salary_info='45-55K€',
        posted_at=None,
        discovered_at=datetime.now().isoformat()
    )
    
    normalizer = WTJDataNormalizer()
    result = normalizer.normalize_job(test_wtj_job)
    
    if result:
        print("✅ Test normalisation WTJ réussi:")
        print(f"   Platform: {result.source_platform}")
        print(f"   ID: {result.source_id}")
        print(f"   URL: {result.source_url}")
        print(f"   Titre: {result.title}")
        print(f"   Entreprise: {result.company_name}")
        print(f"   Mode travail: {result.work_mode}")
        print(f"   URL candidature: {result.application_url}")
        print(f"   Date découverte: {result.discovered_at}")
    else:
        print("❌ Test normalisation WTJ échoué")

if __name__ == "__main__":
    print("🧪 Test du système de normalisation WTJ")
    test_wtj_normalization()