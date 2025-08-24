#!/usr/bin/env python3
"""
Intégration LinkedIn Enhanced → Supabase
Normalise et synchronise les données du workflow Enhanced vers la base de données
"""

import sys
import os
from datetime import datetime, timezone
from typing import List, Dict, Optional
import json

# Ajout du chemin vers le workflow Enhanced existant
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from supabase_client import SimpleJobManager, JobOfferData

class LinkedInDataNormalizer:
    """Normalise les données LinkedIn Enhanced vers le format Supabase"""
    
    @staticmethod
    def extract_job_posting_id(job_basic: Dict, job_detailed: Optional[Dict] = None) -> Optional[str]:
        """Extrait le jobPostingId de différentes sources"""
        # Priorité 1: jobPostingId dans detailed_info
        if job_detailed and 'jobPostingId' in job_detailed:
            return str(job_detailed['jobPostingId'])
        
        # Priorité 2: entityUrn dans basic_info
        if 'entityUrn' in job_basic:
            entity_urn = job_basic['entityUrn']
            if ':' in entity_urn:
                return entity_urn.split(':')[-1]
        
        # Priorité 3: trackingUrn dans basic_info
        if 'trackingUrn' in job_basic:
            tracking_urn = job_basic['trackingUrn']
            if ':' in tracking_urn:
                return tracking_urn.split(':')[-1]
        
        return None
    
    @staticmethod
    def extract_company_info(job_detailed: Optional[Dict] = None) -> tuple[Optional[str], Optional[str]]:
        """Extrait le nom et l'URL LinkedIn de l'entreprise"""
        company_name = None
        company_url = None
        
        if not job_detailed or 'companyDetails' not in job_detailed:
            return company_name, company_url
        
        company_details = job_detailed['companyDetails']
        
        # Parcours des clés de companyDetails pour trouver companyResolutionResult
        for key, value in company_details.items():
            if isinstance(value, dict) and 'companyResolutionResult' in value:
                company_result = value['companyResolutionResult']
                
                if isinstance(company_result, dict):
                    company_name = company_result.get('name')
                    if 'url' in company_result:
                        company_url = company_result['url']
                    break
        
        return company_name, company_url
    
    @staticmethod
    def extract_work_mode(job_detailed: Optional[Dict] = None) -> str:
        """Détermine le mode de travail à partir des données Enhanced"""
        if not job_detailed:
            return "unknown"
        
        # workRemoteAllowed = true → remote
        if job_detailed.get('workRemoteAllowed', False):
            return "remote"
        
        # Analyse des workplaceTypesResolutionResults si disponible
        workplace_types = job_detailed.get('workplaceTypesResolutionResults', {})
        if workplace_types:
            # Logique simplifiée pour détecter hybrid vs on-site
            for key, value in workplace_types.items():
                if isinstance(value, dict):
                    workplace_type = value.get('workplaceType')
                    if 'workplaceType:2' in str(workplace_type):  # Remote
                        return "remote"
                    elif 'workplaceType:3' in str(workplace_type):  # Hybrid
                        return "hybrid"
        
        # Par défaut: on-site
        return "on-site"
    
    @staticmethod
    def extract_application_url(job_detailed: Optional[Dict] = None) -> Optional[str]:
        """Extrait l'URL de candidature directe"""
        if not job_detailed or 'applyMethod' not in job_detailed:
            return None
        
        apply_method = job_detailed['applyMethod']
        
        # Parcours des méthodes de candidature
        for key, value in apply_method.items():
            if isinstance(value, dict):
                # Recherche companyApplyUrl
                if 'companyApplyUrl' in value:
                    return value['companyApplyUrl']
        
        return None
    
    @staticmethod
    def extract_posted_date(job_detailed: Optional[Dict] = None) -> Optional[datetime]:
        """Extrait et convertit la date de publication"""
        if not job_detailed or 'listedAt' not in job_detailed:
            return None
        
        try:
            # listedAt est en timestamp Unix (millisecondes)
            timestamp_ms = job_detailed['listedAt']
            timestamp_s = timestamp_ms / 1000
            return datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        except (ValueError, TypeError, KeyError):
            return None
    
    @staticmethod
    def extract_description(job_detailed: Optional[Dict] = None) -> Optional[str]:
        """Extrait la description complète"""
        if not job_detailed or 'description' not in job_detailed:
            return None
        
        description_data = job_detailed['description']
        
        # Si c'est un dict avec 'text'
        if isinstance(description_data, dict) and 'text' in description_data:
            return description_data['text']
        
        # Si c'est directement une string
        if isinstance(description_data, str):
            return description_data
        
        return None
    
    @classmethod
    def normalize_job(cls, job_enhanced: Dict) -> Optional[JobOfferData]:
        """
        Normalise un emploi du format Enhanced vers JobOfferData
        
        Args:
            job_enhanced: Dict avec 'enhanced_info', 'relevance_analysis', etc.
        """
        try:
            # Structure Enhanced actuelle: job_enhanced['enhanced_info'] contient tout
            enhanced_info = job_enhanced.get('enhanced_info', {})
            
            if not enhanced_info:
                print(f"⚠️ Pas d'enhanced_info dans l'emploi")
                return None
            
            # Extraction directe depuis enhanced_info (déjà normalisé)
            job_posting_id = enhanced_info.get('job_posting_id')
            if not job_posting_id:
                print(f"⚠️ Pas de job_posting_id pour: {enhanced_info.get('title', 'Unknown')}")
                return None
            
            # Conversion de la date si nécessaire
            posted_at = None
            if 'posted_date' in enhanced_info and enhanced_info['posted_date']:
                try:
                    from datetime import datetime
                    posted_at = datetime.fromisoformat(enhanced_info['posted_date'].replace('Z', '+00:00'))
                except:
                    posted_at = None
            
            # Détermination du mode de travail
            work_mode = "unknown"
            if enhanced_info.get('work_remote_allowed', False):
                work_mode = "remote"
            elif enhanced_info.get('workplace_type_labels'):
                # Analyse des labels de workplace
                labels = enhanced_info['workplace_type_labels']
                if isinstance(labels, list):
                    if any('hybrid' in str(label).lower() for label in labels):
                        work_mode = "hybrid"
                    elif any('remote' in str(label).lower() for label in labels):
                        work_mode = "remote"
                    else:
                        work_mode = "on-site"
            else:
                work_mode = "on-site"
            
            # Création de l'objet normalisé
            return JobOfferData(
                source_platform="linkedin",
                source_id=str(job_posting_id),
                source_url=enhanced_info.get('linkedin_job_url'),
                title=enhanced_info.get('title', 'Unknown Title'),
                company_name=enhanced_info.get('company_name'),
                company_url=enhanced_info.get('company_linkedin_url'),
                location=enhanced_info.get('formatted_location', ''),
                description=enhanced_info.get('description', ''),
                work_mode=work_mode,
                job_type="full-time",  # Défaut, peut être enrichi plus tard
                application_url=enhanced_info.get('apply_url'),
                salary_info=None,  # Pas d'info salaire dans Enhanced actuellement
                posted_at=posted_at,
                priority=0,  # Défaut utilisateur
                notes=None
            )
            
        except Exception as e:
            print(f"❌ Erreur normalisation emploi: {e}")
            print(f"   Enhanced info keys: {list(enhanced_info.keys()) if enhanced_info else 'None'}")
            return None

class LinkedInSupabaseSync:
    """Gestionnaire de synchronisation LinkedIn → Supabase"""
    
    def __init__(self):
        self.job_manager = SimpleJobManager()
        self.normalizer = LinkedInDataNormalizer()
        print("🔄 Synchronisation LinkedIn → Supabase initialisée")
    
    def sync_from_enhanced_data(self, jobs_enhanced: List[Dict]) -> Dict[str, int]:
        """
        Synchronise les données Enhanced vers Supabase
        
        Args:
            jobs_enhanced: Liste des emplois au format Enhanced
            
        Returns:
            Statistiques de synchronisation
        """
        if not jobs_enhanced:
            print("⚠️ Aucun emploi à synchroniser")
            return {"total": 0, "new": 0, "updated": 0, "errors": 0}
        
        print(f"🔄 Début normalisation: {len(jobs_enhanced)} emplois Enhanced")
        
        # Phase 1: Normalisation
        normalized_jobs = []
        normalization_errors = 0
        
        for i, job_enhanced in enumerate(jobs_enhanced, 1):
            normalized_job = self.normalizer.normalize_job(job_enhanced)
            
            if normalized_job:
                normalized_jobs.append(normalized_job)
            else:
                normalization_errors += 1
                print(f"   ❌ [{i}/{len(jobs_enhanced)}] Échec normalisation")
        
        print(f"✅ Normalisation terminée: {len(normalized_jobs)} emplois prêts (erreurs: {normalization_errors})")
        
        # Phase 2: Sauvegarde en base
        if normalized_jobs:
            sync_stats = self.job_manager.save_jobs_batch(normalized_jobs)
            sync_stats["normalization_errors"] = normalization_errors
            return sync_stats
        else:
            return {"total": len(jobs_enhanced), "new": 0, "updated": 0, "errors": len(jobs_enhanced)}
    
    def sync_from_enhanced_json(self, json_file_path: str) -> Dict[str, int]:
        """
        Synchronise à partir d'un fichier JSON Enhanced exporté
        
        Args:
            json_file_path: Chemin vers le fichier JSON Enhanced
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                enhanced_data = json.load(f)
            
            jobs_analyzed = enhanced_data.get('jobs_analyzed', [])
            print(f"📂 Fichier Enhanced chargé: {len(jobs_analyzed)} emplois")
            
            return self.sync_from_enhanced_data(jobs_analyzed)
            
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
def test_normalization():
    """Test de normalisation avec données exemple"""
    
    # Exemple de données Enhanced (structure réelle)
    test_job_enhanced = {
        'basic_info': {
            'title': 'SEO Specialist Test',
            'entityUrn': 'urn:li:fsd_jobPosting:1234567890',
            'companyName': 'Test Company'
        },
        'detailed_info': {
            'jobPostingId': 1234567890,
            'formattedLocation': 'Paris, Île-de-France, France',
            'description': {
                'text': 'Nous recherchons un SEO Specialist expérimenté...'
            },
            'workRemoteAllowed': True,
            'listedAt': 1724494849000,  # Timestamp Unix en millisecondes
            'applyMethod': {
                'com.linkedin.voyager.jobs.OffsiteApply': {
                    'companyApplyUrl': 'https://company.com/jobs/apply'
                }
            },
            'companyDetails': {
                'com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany': {
                    'companyResolutionResult': {
                        'name': 'Test Company Enhanced',
                        'url': 'https://linkedin.com/company/test-company'
                    }
                }
            }
        }
    }
    
    normalizer = LinkedInDataNormalizer()
    result = normalizer.normalize_job(test_job_enhanced)
    
    if result:
        print("✅ Test normalisation réussi:")
        print(f"   Platform: {result.source_platform}")
        print(f"   ID: {result.source_id}")
        print(f"   URL: {result.source_url}")
        print(f"   Titre: {result.title}")
        print(f"   Entreprise: {result.company_name}")
        print(f"   Mode travail: {result.work_mode}")
        print(f"   URL candidature: {result.application_url}")
        print(f"   Date publication: {result.posted_at}")
    else:
        print("❌ Test normalisation échoué")

if __name__ == "__main__":
    print("🧪 Test du système de normalisation LinkedIn")
    test_normalization()