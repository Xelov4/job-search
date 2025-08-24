"""
Welcome to the Jungle Job Scraper
Scraper avancé pour Welcome to the Jungle avec Playwright
Intégré au système Job Tracker existant
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse, parse_qs
import logging

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("❌ Playwright non installé. Installation requise:")
    print("pip install playwright")
    print("playwright install chromium")
    exit(1)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from job_data_types import JobOfferData

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WTJSearchConfig:
    """Configuration pour recherche Welcome to the Jungle"""
    keywords: str
    location: str = "Île-de-France"
    country: str = "FR" 
    max_pages: int = 5
    max_jobs_per_page: int = 20
    delay_between_requests: float = 2.0
    headless: bool = True


class WelcomeToTheJungleScraper:
    """Scraper pour Welcome to the Jungle avec normalisation JobOfferData"""
    
    BASE_URL = "https://www.welcometothejungle.com"
    SEARCH_URL = f"{BASE_URL}/fr/jobs"
    
    def __init__(self, config: WTJSearchConfig):
        self.config = config
        self.browser: Optional[Browser] = None
        self.jobs_found: List[Dict[str, Any]] = []
        
    async def __aenter__(self):
        """Context manager entry"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.config.headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage'
            ]
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            await self.browser.close()
    
    def build_search_url(self, page: int = 1) -> str:
        """Construire URL de recherche WTJ"""
        params = {
            'query': self.config.keywords,
            'refinementList[offices.country_code][]': self.config.country,
            'refinementList[offices.state][]': self.config.location,
            'page': str(page)
        }
        
        # Construction manuelle pour éviter les problèmes d'encodage
        url = f"{self.SEARCH_URL}?query={self.config.keywords.replace(' ', '%20')}"
        url += f"&refinementList%5Boffices.country_code%5D%5B%5D={self.config.country}"
        url += f"&refinementList%5Boffices.state%5D%5B%5D={self.config.location.replace(' ', '%20')}"
        url += f"&page={page}"
        
        return url
    
    async def scrape_search_page(self, page: Page, page_num: int = 1) -> List[Dict[str, Any]]:
        """Scraper une page de résultats de recherche"""
        search_url = self.build_search_url(page_num)
        logger.info(f"🔍 Scraping page {page_num}: {search_url}")
        
        try:
            # Aller à la page de recherche
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            
            # Attendre que les résultats se chargent
            await page.wait_for_timeout(3000)
            
            # Vérifier s'il y a des résultats
            no_results = await page.query_selector('.sc-AxjAm')  # Message "pas de jobs"
            if no_results:
                logger.warning(f"❌ Aucun résultat trouvé sur la page {page_num}")
                return []
            
            # Extraire les cartes d'emploi
            job_cards = await page.query_selector_all('[data-testid="job-card"], .kghzAS, [class*="job-card"], article')
            
            if not job_cards:
                # Essayer avec des sélecteurs plus génériques
                job_cards = await page.query_selector_all('a[href*="/jobs/"]')
            
            logger.info(f"📋 Trouvé {len(job_cards)} cartes d'emploi sur la page {page_num}")
            
            jobs = []
            for i, card in enumerate(job_cards):
                try:
                    job_data = await self.extract_job_from_card(page, card, i)
                    if job_data:
                        jobs.append(job_data)
                        logger.debug(f"✅ Job {i+1}: {job_data.get('title', 'N/A')}")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erreur extraction job {i+1}: {str(e)}")
                    continue
            
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Erreur scraping page {page_num}: {str(e)}")
            return []
    
    async def extract_job_from_card(self, page: Page, card, index: int) -> Optional[Dict[str, Any]]:
        """Extraire données d'une carte emploi"""
        try:
            # Extraire le lien vers l'annonce détaillée
            job_link = None
            link_elem = await card.query_selector('a[href*="/jobs/"]')
            if link_elem:
                job_link = await link_elem.get_attribute('href')
                if job_link and not job_link.startswith('http'):
                    job_link = urljoin(self.BASE_URL, job_link)
            
            if not job_link:
                # Si pas de lien direct, chercher dans les parents
                job_link = await card.get_attribute('href')
                if job_link and not job_link.startswith('http'):
                    job_link = urljoin(self.BASE_URL, job_link)
            
            # Extraire les données basiques de la carte
            title = await self.extract_text_from_selectors(card, [
                '[data-testid="job-title"]',
                '.kqhpUv',
                'h3',
                'h2',
                '.job-title'
            ])
            
            company = await self.extract_text_from_selectors(card, [
                '[data-testid="company-name"]',
                '.heHnPH',
                '.jkTLoh',
                '.company-name'
            ])
            
            location = await self.extract_text_from_selectors(card, [
                '[data-testid="job-location"]',
                '.iVnwxA',
                '.location'
            ])
            
            # Description courte si disponible
            description = await self.extract_text_from_selectors(card, [
                '.ZhdPr',
                '.job-description',
                'p'
            ]) or ""
            
            # Construire job data basique
            job_data = {
                'source_platform': 'welcometothejungle',
                'source_url': job_link or '',
                'title': title or f"Job #{index+1}",
                'company_name': company or 'Entreprise inconnue',
                'location': self.clean_location(location or ''),
                'description': description.strip()[:500] if description else '',  # Limiter à 500 chars
                'posted_at': None,
                'work_mode': self.detect_work_mode(title, description, location),
                'job_type': 'full-time',  # Par défaut
                'application_url': '',
                'salary_info': ''
            }
            
            # Si on a un lien, essayer d'extraire plus de détails
            if job_link and len(job_data.get('description', '')) < 100:
                detailed_data = await self.scrape_job_details(page, job_link)
                if detailed_data:
                    job_data.update(detailed_data)
            
            # Générer source_id à partir de l'URL
            if job_link:
                job_data['source_id'] = self.extract_job_id_from_url(job_link)
            else:
                job_data['source_id'] = f"wtj_{datetime.now().timestamp()}_{index}"
            
            return job_data
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur extraction carte {index}: {str(e)}")
            return None
    
    async def extract_text_from_selectors(self, element, selectors: List[str]) -> Optional[str]:
        """Extraire texte en essayant plusieurs sélecteurs"""
        for selector in selectors:
            try:
                elem = await element.query_selector(selector)
                if elem:
                    text = await elem.inner_text()
                    if text and text.strip():
                        return text.strip()
            except:
                continue
        return None
    
    async def scrape_job_details(self, page: Page, job_url: str) -> Optional[Dict[str, Any]]:
        """Scraper les détails d'une annonce individuelle"""
        try:
            logger.debug(f"🔍 Détails job: {job_url}")
            
            # Créer une nouvelle page pour éviter les conflits
            detail_page = await self.browser.new_page()
            
            try:
                await detail_page.goto(job_url, wait_until='networkidle', timeout=20000)
                await detail_page.wait_for_timeout(2000)
                
                # Extraire description complète
                description_selectors = [
                    '[data-testid="job-description"]',
                    '.sc-AxjAm.dDaKon',
                    '.job-description',
                    'section[class*="description"]',
                    'div[class*="description"]'
                ]
                
                description = ""
                for selector in description_selectors:
                    try:
                        elem = await detail_page.query_selector(selector)
                        if elem:
                            description = await elem.inner_text()
                            if description and len(description) > 100:
                                break
                    except:
                        continue
                
                # Extraire informations additionnelles
                salary = await self.extract_text_from_selectors(detail_page, [
                    '[data-testid="salary"]',
                    '.salary',
                    '[class*="salary"]'
                ])
                
                work_mode = await self.extract_text_from_selectors(detail_page, [
                    '[data-testid="remote"]',
                    '.remote',
                    '[class*="remote"]',
                    '[class*="location"]'
                ])
                
                # URL de candidature
                apply_button = await detail_page.query_selector('a[href*="apply"], button[class*="apply"], [data-testid="apply"]')
                application_url = ""
                if apply_button:
                    application_url = await apply_button.get_attribute('href') or ""
                    if application_url and not application_url.startswith('http'):
                        application_url = urljoin(self.BASE_URL, application_url)
                
                return {
                    'description': description.strip()[:2000] if description else '',
                    'salary_info': salary or '',
                    'work_mode': self.detect_work_mode_from_details(work_mode, description),
                    'application_url': application_url
                }
                
            finally:
                await detail_page.close()
                
        except Exception as e:
            logger.warning(f"⚠️ Erreur détails job {job_url}: {str(e)}")
            return None
    
    def extract_job_id_from_url(self, url: str) -> str:
        """Extraire ID unique de l'URL Welcome to the Jungle"""
        try:
            # Format typique: /fr/jobs/[slug]-[id] ou /jobs/[id]
            path = urlparse(url).path
            
            # Chercher un ID à la fin de l'URL
            id_match = re.search(r'/jobs/([^/]+)(?:/[^/]*)?/?$', path)
            if id_match:
                job_slug = id_match.group(1)
                
                # Si le slug contient un ID numérique, l'extraire
                numeric_id = re.search(r'-(\d+)$', job_slug)
                if numeric_id:
                    return f"wtj_{numeric_id.group(1)}"
                else:
                    return f"wtj_{job_slug}"
            
            # Fallback: utiliser le path complet comme ID
            return f"wtj_{hash(path)}"
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur extraction ID de {url}: {str(e)}")
            return f"wtj_{hash(url)}_{datetime.now().timestamp()}"
    
    def clean_location(self, location: str) -> str:
        """Nettoyer et normaliser la localisation"""
        if not location:
            return ""
        
        # Nettoyer les espaces et caractères spéciaux
        location = re.sub(r'\s+', ' ', location.strip())
        
        # Normaliser les localisations communes
        location_mapping = {
            'paris': 'Paris, France',
            'île-de-france': 'Île-de-France, France',
            'remote': 'Remote',
            'télétravail': 'Remote',
            'france': 'France'
        }
        
        location_lower = location.lower()
        for key, value in location_mapping.items():
            if key in location_lower:
                return value
        
        return location
    
    def detect_work_mode(self, title: str = "", description: str = "", location: str = "") -> str:
        """Détecter le mode de travail (remote/on-site/hybrid)"""
        text_to_check = f"{title} {description} {location}".lower()
        
        remote_keywords = [
            'remote', 'télétravail', 'full remote', 'home office',
            'travail à distance', 'distanciel', 'nomade'
        ]
        
        hybrid_keywords = [
            'hybride', 'flexible', 'partiel', 'mixte',
            'télétravail partiel', 'hybrid'
        ]
        
        if any(keyword in text_to_check for keyword in remote_keywords):
            return 'remote'
        elif any(keyword in text_to_check for keyword in hybrid_keywords):
            return 'hybrid'
        else:
            return 'on-site'
    
    def detect_work_mode_from_details(self, work_mode_text: str, description: str) -> str:
        """Détecter mode de travail à partir des détails de l'annonce"""
        if work_mode_text:
            return self.detect_work_mode(description=f"{work_mode_text} {description}")
        return self.detect_work_mode(description=description)
    
    async def scrape_all_pages(self) -> List[Dict[str, Any]]:
        """Scraper toutes les pages de résultats"""
        if not self.browser:
            raise ValueError("Browser not initialized. Use async with context manager.")
        
        logger.info(f"🚀 Début scraping Welcome to the Jungle: '{self.config.keywords}' - {self.config.location}")
        
        # Créer une page principale
        page = await self.browser.new_page()
        
        # Headers pour éviter la détection
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        all_jobs = []
        
        try:
            for page_num in range(1, self.config.max_pages + 1):
                jobs_on_page = await self.scrape_search_page(page, page_num)
                
                if not jobs_on_page:
                    logger.info(f"❌ Pas de jobs sur la page {page_num}, arrêt du scraping")
                    break
                
                all_jobs.extend(jobs_on_page)
                logger.info(f"✅ Page {page_num}: {len(jobs_on_page)} jobs extraits")
                
                # Attendre entre les pages
                if page_num < self.config.max_pages:
                    await page.wait_for_timeout(int(self.config.delay_between_requests * 1000))
            
            logger.info(f"🎯 Scraping terminé: {len(all_jobs)} jobs au total")
            self.jobs_found = all_jobs
            return all_jobs
            
        finally:
            await page.close()
    
    def normalize_to_job_offer_data(self, wtj_job: Dict[str, Any]) -> Optional[JobOfferData]:
        """Normaliser un job WTJ vers JobOfferData"""
        try:
            return JobOfferData(
                source_platform='welcometothejungle',
                source_id=wtj_job.get('source_id', ''),
                source_url=wtj_job.get('source_url', ''),
                title=wtj_job.get('title', ''),
                company_name=wtj_job.get('company_name', ''),
                company_url='',  # À implémenter si nécessaire
                location=wtj_job.get('location', ''),
                description=wtj_job.get('description', ''),
                work_mode=wtj_job.get('work_mode', 'on-site'),
                job_type=wtj_job.get('job_type', 'full-time'),
                application_url=wtj_job.get('application_url', ''),
                salary_info=wtj_job.get('salary_info', ''),
                posted_at=wtj_job.get('posted_at'),  # ISO string ou None
                discovered_at=datetime.now().isoformat(),
            )
        except Exception as e:
            logger.error(f"❌ Erreur normalisation job: {str(e)}")
            return None
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """Sauvegarder les résultats en JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/root/Job/linkedin-mcp/data/exports/wtj_scraping_{timestamp}.json"
        
        export_data = {
            'search_config': {
                'keywords': self.config.keywords,
                'location': self.config.location,
                'max_pages': self.config.max_pages
            },
            'scraping_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_jobs': len(self.jobs_found),
                'source': 'welcometothejungle'
            },
            'jobs': self.jobs_found
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Résultats sauvegardés: {filename}")
        return filename


# Fonction principale pour intégration
async def scrape_welcome_to_jungle(keywords: str, location: str = "Île-de-France", max_pages: int = 3) -> List[JobOfferData]:
    """
    Fonction principale pour scraper Welcome to the Jungle
    Retourne des JobOfferData normalisées pour intégration Supabase
    """
    config = WTJSearchConfig(
        keywords=keywords,
        location=location,
        max_pages=max_pages,
        headless=True,
        delay_between_requests=2.0
    )
    
    normalized_jobs = []
    
    async with WelcomeToTheJungleScraper(config) as scraper:
        # Scraper tous les jobs
        raw_jobs = await scraper.scrape_all_pages()
        
        # Sauvegarder les résultats bruts
        scraper.save_results()
        
        # Normaliser pour le système existant
        for raw_job in raw_jobs:
            normalized = scraper.normalize_to_job_offer_data(raw_job)
            if normalized:
                normalized_jobs.append(normalized)
    
    logger.info(f"🎯 Normalisés: {len(normalized_jobs)} jobs Welcome to the Jungle")
    return normalized_jobs


# Script de test/démonstration
async def main():
    """Test du scraper Welcome to the Jungle"""
    print("🧪 Test Welcome to the Jungle Scraper")
    print("=" * 50)
    
    # Configuration de test
    keywords = "SEO"
    location = "Île-de-France"
    
    try:
        jobs = await scrape_welcome_to_jungle(
            keywords=keywords,
            location=location,
            max_pages=2  # Limité pour le test
        )
        
        print(f"\n✅ Scraping terminé: {len(jobs)} jobs trouvés")
        
        # Afficher quelques exemples
        for i, job in enumerate(jobs[:3]):
            print(f"\n📋 Job {i+1}:")
            print(f"  Titre: {job.title}")
            print(f"  Entreprise: {job.company_name}")
            print(f"  Lieu: {job.location}")
            print(f"  Mode: {job.work_mode}")
            print(f"  URL: {job.source_url[:80]}...")
        
        return jobs
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []


if __name__ == "__main__":
    asyncio.run(main())