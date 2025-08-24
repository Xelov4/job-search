#!/usr/bin/env python3
"""
Welcome to the Jungle Fast Scraper
Version optimisée sans deep scraping pour éviter les timeouts
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urljoin
import logging

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("❌ Playwright non installé")
    exit(1)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from job_data_types import JobOfferData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WTJFastConfig:
    """Configuration pour scraper rapide WTJ"""
    keywords: str
    location: str = "Île-de-France"
    max_pages: int = 2
    headless: bool = True

class FastWTJScraper:
    """Scraper rapide WTJ - surface scraping seulement"""
    
    BASE_URL = "https://www.welcometothejungle.com"
    
    def __init__(self, config: WTJFastConfig):
        self.config = config
        self.browser = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        await self.playwright.stop()
    
    def build_search_url(self, page_num: int = 1) -> str:
        """Construire URL de recherche"""
        base = f"{self.BASE_URL}/fr/jobs"
        params = [
            f"query={self.config.keywords}",
            "refinementList%5Boffices.country_code%5D%5B%5D=FR",
            f"refinementList%5Boffices.state%5D%5B%5D={self.config.location}",
            f"page={page_num}"
        ]
        return f"{base}?{'&'.join(params)}"
    
    async def scrape_page_fast(self, page: Page, page_num: int) -> List[Dict[str, Any]]:
        """Scraping rapide d'une page - surface seulement"""
        logger.info(f"🔍 Scraping rapide page {page_num}")
        
        search_url = self.build_search_url(page_num)
        await page.goto(search_url, wait_until='networkidle', timeout=30000)
        
        # Attendre que les jobs se chargent dynamiquement
        await page.wait_for_timeout(5000)
        
        # Scroll pour déclencher le chargement lazy
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        
        # Sélecteurs pour les cartes job (plus génériques)
        job_selectors = [
            'article',  # Plus générique
            'div[class*="job"]',
            'div[class*="card"]',
            '[data-testid="job-card"]',
            '.kghzAS', 
            'div[class*="JobCard"]',
            '[class*="job-item"]',
            'div[role="listitem"]',  # Souvent utilisé
            'li'  # Très générique
        ]
        
        job_cards = []
        for selector in job_selectors:
            cards = await page.query_selector_all(selector)
            if cards:
                job_cards = cards
                logger.info(f"📋 Trouvé {len(cards)} jobs avec sélecteur: {selector}")
                break
        
        if not job_cards:
            logger.warning("⚠️ Aucune carte job trouvée")
            return []
        
        jobs_data = []
        
        for i, card in enumerate(job_cards):
            try:
                # Extraire seulement les données visibles sur la carte
                job_data = await self.extract_card_data_fast(card, i)
                if job_data:
                    jobs_data.append(job_data)
                    
            except Exception as e:
                logger.warning(f"⚠️ Erreur extraction carte {i}: {str(e)}")
                continue
        
        return jobs_data
    
    async def extract_card_data_fast(self, card, index: int) -> Optional[Dict[str, Any]]:
        """Extraction rapide des données de carte - pas de navigation"""
        try:
            # Titre
            title = await self.get_text_safe(card, [
                '[data-testid="job-title"]',
                'h3', 'h2', 'h4',
                '.job-title',
                'a[class*="title"]'
            ])
            
            # Entreprise
            company = await self.get_text_safe(card, [
                '[data-testid="company-name"]',
                '.company-name',
                'span[class*="company"]',
                'div[class*="company"]'
            ])
            
            # Localisation
            location = await self.get_text_safe(card, [
                '[data-testid="job-location"]',
                '.location',
                'span[class*="location"]',
                'div[class*="location"]'
            ])
            
            # URL du job
            job_url = await self.get_link_safe(card)
            
            # Détection work_mode basique
            work_mode = self.detect_work_mode_fast(title, location)
            
            # Générer source_id
            source_id = self.generate_source_id(job_url, index)
            
            return {
                'source_platform': 'welcometothejungle',
                'source_id': source_id,
                'source_url': job_url or '',
                'title': title or f"Job #{index+1}",
                'company_name': company or 'Entreprise inconnue',
                'location': self.clean_location(location or ''),
                'description': f"Job {title} chez {company}" if title and company else '',
                'work_mode': work_mode,
                'job_type': 'full-time',
                'application_url': job_url or '',
                'salary_info': '',
                'posted_at': None,
                'discovered_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur extraction données carte {index}: {str(e)}")
            return None
    
    async def get_text_safe(self, element, selectors: List[str]) -> Optional[str]:
        """Récupérer texte de manière sûre"""
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
    
    async def get_link_safe(self, element) -> Optional[str]:
        """Récupérer lien de manière sûre"""
        try:
            # Essayer plusieurs sélecteurs pour les liens
            link_selectors = ['a', '[href]', 'a[href*="/jobs/"]']
            
            for selector in link_selectors:
                link_elem = await element.query_selector(selector)
                if link_elem:
                    href = await link_elem.get_attribute('href')
                    if href:
                        if href.startswith('/'):
                            return urljoin(self.BASE_URL, href)
                        elif href.startswith('http'):
                            return href
            return None
        except:
            return None
    
    def detect_work_mode_fast(self, title: str, location: str) -> str:
        """Détection rapide work_mode"""
        text = f"{title or ''} {location or ''}".lower()
        
        if any(word in text for word in ['remote', 'télétravail', 'distance']):
            return 'remote'
        elif any(word in text for word in ['hybride', 'hybrid']):
            return 'hybrid'
        else:
            return 'on-site'
    
    def clean_location(self, location: str) -> str:
        """Nettoyer localisation"""
        if not location:
            return "France"
        return location.strip()
    
    def generate_source_id(self, url: str, index: int) -> str:
        """Générer source_id unique"""
        if url:
            # Extraire ID de l'URL si possible
            match = re.search(r'/jobs/([a-zA-Z0-9_-]+)', url)
            if match:
                return f"wtj_{match.group(1)}"
        
        # Fallback avec timestamp
        return f"wtj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}"
    
    async def scrape_all_fast(self) -> List[JobOfferData]:
        """Scraping rapide de toutes les pages"""
        logger.info(f"🚀 Scraping rapide WTJ: '{self.config.keywords}' - {self.config.location}")
        
        all_jobs = []
        page = await self.browser.new_page()
        
        try:
            for page_num in range(1, self.config.max_pages + 1):
                jobs_data = await self.scrape_page_fast(page, page_num)
                
                if not jobs_data:
                    logger.info(f"📄 Page {page_num}: Aucun job trouvé, arrêt")
                    break
                
                # Convertir en JobOfferData
                for job_dict in jobs_data:
                    job_offer = JobOfferData(**job_dict)
                    all_jobs.append(job_offer)
                
                logger.info(f"✅ Page {page_num}: {len(jobs_data)} jobs extraits")
                
                # Délai entre pages
                await page.wait_for_timeout(1000)
        
        finally:
            await page.close()
        
        logger.info(f"🎉 Scraping terminé: {len(all_jobs)} jobs au total")
        return all_jobs

# Fonction utilitaire
async def scrape_wtj_fast(keywords: str, location: str = "Île-de-France", max_pages: int = 2) -> List[JobOfferData]:
    """Fonction utilitaire pour scraping rapide"""
    config = WTJFastConfig(
        keywords=keywords,
        location=location,
        max_pages=max_pages,
        headless=True
    )
    
    async with FastWTJScraper(config) as scraper:
        return await scraper.scrape_all_fast()

if __name__ == "__main__":
    async def test_fast():
        jobs = await scrape_wtj_fast("SEO", "Île-de-France", 1)
        print(f"✅ {len(jobs)} jobs trouvés")
        
        for i, job in enumerate(jobs[:5]):
            print(f"{i+1}. {job.title} chez {job.company_name}")
    
    asyncio.run(test_fast())