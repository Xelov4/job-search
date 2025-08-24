"""
Welcome to the Jungle (WTJ) Scraper Module
==========================================

Module Python pour scraping et intégration Welcome to the Jungle
dans le système Job Tracker multi-sources.

Composants principaux:
- fast_scraper.py : Scraper optimisé sans timeout
- scraper.py : Scraper complet avec deep analysis (legacy)
- complete_test.py : Test workflow complet WTJ
- db_test.py : Test import base de données simplifié

Usage:
    from wtj.fast_scraper import scrape_wtj_fast
    
    jobs = await scrape_wtj_fast("SEO", "Île-de-France", max_pages=2)
"""

from .fast_scraper import scrape_wtj_fast, FastWTJScraper, WTJFastConfig

__version__ = "1.0.0"
__author__ = "Job Tracker Team"
__all__ = ["scrape_wtj_fast", "FastWTJScraper", "WTJFastConfig"]