"""
Multi-Source Job Collector
Collecte de jobs depuis multiple sources : LinkedIn Enhanced + Welcome to the Jungle
Intégration complète avec le système Job Tracker existant
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
import os
import sys

# Imports du système existant
from job_data_types import JobOfferData
from linkedin_integration import LinkedInJobNormalizer
from wtj import scrape_wtj_fast
from supabase_client import SupabaseJobClient

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MultiSourceConfig:
    """Configuration pour collecte multi-sources"""
    keywords: str
    location: str = "Paris, Île-de-France, France"
    
    # LinkedIn Enhanced
    enable_linkedin: bool = True
    linkedin_limit: int = 50
    
    # Welcome to the Jungle
    enable_wtj: bool = True
    wtj_max_pages: int = 3
    wtj_location: str = "Île-de-France"
    
    # Autres sources futures
    enable_indeed: bool = False
    enable_glassdoor: bool = False
    
    # Paramètres généraux
    remove_duplicates: bool = True
    save_raw_results: bool = True
    auto_sync_supabase: bool = True


class MultiSourceJobCollector:
    """Collecteur unifié pour toutes les sources d'emploi"""
    
    def __init__(self, config: MultiSourceConfig):
        self.config = config
        self.collected_jobs: Dict[str, List[JobOfferData]] = {}
        self.all_jobs: List[JobOfferData] = []
        self.stats = {
            'total_collected': 0,
            'by_source': {},
            'duplicates_removed': 0,
            'sync_success': 0,
            'sync_errors': 0
        }
    
    async def collect_from_linkedin_enhanced(self) -> List[JobOfferData]:
        """Collecter jobs depuis LinkedIn Enhanced (workflow existant)"""
        if not self.config.enable_linkedin:
            logger.info("📴 LinkedIn désactivé dans la config")
            return []
        
        logger.info(f"🔍 Recherche LinkedIn Enhanced: '{self.config.keywords}'")
        
        try:
            # Chercher le dernier export LinkedIn Enhanced
            export_dir = "/root/Job/linkedin-mcp/data/exports"
            linkedin_files = []
            
            if os.path.exists(export_dir):
                for filename in os.listdir(export_dir):
                    if filename.startswith("enhanced_results_") and filename.endswith(".json"):
                        file_path = os.path.join(export_dir, filename)
                        linkedin_files.append((file_path, os.path.getmtime(file_path)))
            
            if not linkedin_files:
                logger.warning("⚠️ Aucun export LinkedIn Enhanced trouvé")
                logger.info("💡 Lancez d'abord: python analyse_pertinence_complete_enhanced.py")
                return []
            
            # Prendre le fichier le plus récent
            latest_file = max(linkedin_files, key=lambda x: x[1])[0]
            logger.info(f"📁 Utilisation export LinkedIn: {os.path.basename(latest_file)}")
            
            # Charger et normaliser les jobs LinkedIn
            with open(latest_file, 'r', encoding='utf-8') as f:
                linkedin_data = json.load(f)
            
            jobs = linkedin_data.get('jobs', [])
            normalized_jobs = []
            
            for job in jobs[:self.config.linkedin_limit]:
                normalized = LinkedInJobNormalizer.normalize_job(job)
                if normalized:
                    normalized_jobs.append(normalized)
            
            logger.info(f"✅ LinkedIn Enhanced: {len(normalized_jobs)} jobs collectés")
            self.stats['by_source']['linkedin'] = len(normalized_jobs)
            return normalized_jobs
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte LinkedIn: {str(e)}")
            self.stats['by_source']['linkedin'] = 0
            return []
    
    async def collect_from_welcome_to_jungle(self) -> List[JobOfferData]:
        """Collecter jobs depuis Welcome to the Jungle"""
        if not self.config.enable_wtj:
            logger.info("📴 Welcome to the Jungle désactivé dans la config")
            return []
        
        logger.info(f"🌟 Recherche Welcome to the Jungle: '{self.config.keywords}'")
        
        try:
            jobs = await scrape_wtj_fast(
                keywords=self.config.keywords,
                location=self.config.wtj_location,
                max_pages=self.config.wtj_max_pages
            )
            
            logger.info(f"✅ Welcome to the Jungle: {len(jobs)} jobs collectés")
            self.stats['by_source']['welcometothejungle'] = len(jobs)
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte Welcome to the Jungle: {str(e)}")
            self.stats['by_source']['welcometothejungle'] = 0
            return []
    
    async def collect_from_indeed(self) -> List[JobOfferData]:
        """Collecter jobs depuis Indeed (à implémenter)"""
        if not self.config.enable_indeed:
            return []
        
        logger.info("🚧 Indeed - À implémenter")
        # TODO: Implémenter Indeed scraper
        self.stats['by_source']['indeed'] = 0
        return []
    
    async def collect_from_glassdoor(self) -> List[JobOfferData]:
        """Collecter jobs depuis Glassdoor (à implémenter)"""
        if not self.config.enable_glassdoor:
            return []
        
        logger.info("🚧 Glassdoor - À implémenter")
        # TODO: Implémenter Glassdoor scraper
        self.stats['by_source']['glassdoor'] = 0
        return []
    
    async def collect_from_all_sources(self) -> List[JobOfferData]:
        """Collecter jobs depuis toutes les sources activées"""
        logger.info("🚀 Début collecte multi-sources")
        logger.info(f"🎯 Recherche: '{self.config.keywords}' - {self.config.location}")
        
        # Collecte parallèle de toutes les sources
        tasks = []
        
        if self.config.enable_linkedin:
            tasks.append(('linkedin', self.collect_from_linkedin_enhanced()))
        
        if self.config.enable_wtj:
            tasks.append(('welcometothejungle', self.collect_from_welcome_to_jungle()))
        
        if self.config.enable_indeed:
            tasks.append(('indeed', self.collect_from_indeed()))
        
        if self.config.enable_glassdoor:
            tasks.append(('glassdoor', self.collect_from_glassdoor()))
        
        # Exécuter toutes les tâches en parallèle
        results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        # Traiter les résultats
        all_jobs = []
        for i, (source_name, _) in enumerate(tasks):
            result = results[i]
            if isinstance(result, Exception):
                logger.error(f"❌ Erreur {source_name}: {str(result)}")
                self.collected_jobs[source_name] = []
            else:
                self.collected_jobs[source_name] = result
                all_jobs.extend(result)
                logger.info(f"✅ {source_name}: {len(result)} jobs")
        
        # Supprimer les doublons si activé
        if self.config.remove_duplicates:
            all_jobs = self.remove_duplicates(all_jobs)
        
        self.all_jobs = all_jobs
        self.stats['total_collected'] = len(all_jobs)
        
        logger.info(f"🎯 Collecte terminée: {len(all_jobs)} jobs au total")
        return all_jobs
    
    def remove_duplicates(self, jobs: List[JobOfferData]) -> List[JobOfferData]:
        """Supprimer les doublons basés sur titre + entreprise"""
        seen = set()
        unique_jobs = []
        duplicates_count = 0
        
        for job in jobs:
            # Créer une clé unique basée sur titre et entreprise (normalisés)
            title_clean = job.title.lower().strip()
            company_clean = job.company_name.lower().strip()
            unique_key = f"{title_clean}|{company_clean}"
            
            if unique_key not in seen:
                seen.add(unique_key)
                unique_jobs.append(job)
            else:
                duplicates_count += 1
        
        self.stats['duplicates_removed'] = duplicates_count
        logger.info(f"🧹 Doublons supprimés: {duplicates_count}")
        
        return unique_jobs
    
    async def sync_to_supabase(self) -> Dict[str, int]:
        """Synchroniser tous les jobs vers Supabase"""
        if not self.config.auto_sync_supabase:
            logger.info("📴 Sync Supabase désactivé dans la config")
            return {'synced': 0, 'errors': 0}
        
        if not self.all_jobs:
            logger.warning("⚠️ Aucun job à synchroniser")
            return {'synced': 0, 'errors': 0}
        
        logger.info(f"🗄️ Synchronisation Supabase: {len(self.all_jobs)} jobs")
        
        try:
            supabase_client = SupabaseJobClient()
            sync_stats = supabase_client.save_jobs_batch(self.all_jobs)
            
            self.stats['sync_success'] = sync_stats.get('new', 0) + sync_stats.get('updated', 0)
            self.stats['sync_errors'] = sync_stats.get('errors', 0)
            
            logger.info(f"✅ Sync terminée: {sync_stats}")
            return sync_stats
            
        except Exception as e:
            logger.error(f"❌ Erreur sync Supabase: {str(e)}")
            self.stats['sync_errors'] = len(self.all_jobs)
            return {'synced': 0, 'errors': len(self.all_jobs)}
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """Sauvegarder tous les résultats en JSON"""
        if not self.config.save_raw_results:
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/root/Job/linkedin-mcp/data/exports/multi_source_collection_{timestamp}.json"
        
        # Préparer les données d'export
        export_data = {
            'collection_metadata': {
                'timestamp': datetime.now().isoformat(),
                'config': asdict(self.config),
                'stats': self.stats
            },
            'jobs_by_source': {},
            'all_jobs_normalized': []
        }
        
        # Jobs par source (format brut)
        for source, jobs in self.collected_jobs.items():
            export_data['jobs_by_source'][source] = [asdict(job) for job in jobs]
        
        # Tous les jobs normalisés
        export_data['all_jobs_normalized'] = [asdict(job) for job in self.all_jobs]
        
        # Sauvegarder
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Résultats sauvegardés: {filename}")
        return filename
    
    def print_summary(self):
        """Afficher un résumé de la collecte"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ COLLECTE MULTI-SOURCES")
        print("="*60)
        print(f"🎯 Mots-clés: {self.config.keywords}")
        print(f"📍 Localisation: {self.config.location}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📈 STATISTIQUES GLOBALES:")
        print(f"  Total collecté: {self.stats['total_collected']} jobs")
        print(f"  Doublons supprimés: {self.stats['duplicates_removed']}")
        print(f"  Sync Supabase: {self.stats['sync_success']} succès, {self.stats['sync_errors']} erreurs")
        
        print(f"\n🗂️ PAR SOURCE:")
        for source, count in self.stats['by_source'].items():
            status = "✅" if count > 0 else "❌"
            print(f"  {status} {source.upper()}: {count} jobs")
        
        if self.all_jobs:
            print(f"\n🏆 TOP 5 ENTREPRISES:")
            companies = {}
            for job in self.all_jobs:
                companies[job.company_name] = companies.get(job.company_name, 0) + 1
            
            for i, (company, count) in enumerate(sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]):
                print(f"  {i+1}. {company}: {count} jobs")
        
        print("\n" + "="*60)


# Fonctions principales pour utilisation
async def collect_jobs_multi_source(
    keywords: str,
    location: str = "Paris, Île-de-France, France",
    enable_linkedin: bool = True,
    enable_wtj: bool = True,
    linkedin_limit: int = 50,
    wtj_max_pages: int = 3
) -> List[JobOfferData]:
    """
    Fonction principale pour collecte multi-sources
    """
    config = MultiSourceConfig(
        keywords=keywords,
        location=location,
        enable_linkedin=enable_linkedin,
        enable_wtj=enable_wtj,
        linkedin_limit=linkedin_limit,
        wtj_max_pages=wtj_max_pages,
        remove_duplicates=True,
        auto_sync_supabase=True,
        save_raw_results=True
    )
    
    collector = MultiSourceJobCollector(config)
    
    # Collecter de toutes les sources
    jobs = await collector.collect_from_all_sources()
    
    # Synchroniser vers Supabase
    await collector.sync_to_supabase()
    
    # Sauvegarder les résultats
    collector.save_results()
    
    # Afficher le résumé
    collector.print_summary()
    
    return jobs


# Script principal
async def main():
    """Script principal de collecte multi-sources"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collecte multi-sources de jobs")
    parser.add_argument("keywords", help="Mots-clés de recherche")
    parser.add_argument("--location", default="Paris, Île-de-France, France", help="Localisation")
    parser.add_argument("--no-linkedin", action="store_true", help="Désactiver LinkedIn")
    parser.add_argument("--no-wtj", action="store_true", help="Désactiver Welcome to the Jungle")
    parser.add_argument("--linkedin-limit", type=int, default=50, help="Limite jobs LinkedIn")
    parser.add_argument("--wtj-pages", type=int, default=3, help="Pages WTJ à scraper")
    
    args = parser.parse_args()
    
    try:
        jobs = await collect_jobs_multi_source(
            keywords=args.keywords,
            location=args.location,
            enable_linkedin=not args.no_linkedin,
            enable_wtj=not args.no_wtj,
            linkedin_limit=args.linkedin_limit,
            wtj_max_pages=args.wtj_pages
        )
        
        print(f"\n🎉 Collecte terminée: {len(jobs)} jobs collectés et synchronisés!")
        
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())