#!/usr/bin/env python3
"""
Script d'entrée pour lancer la recherche d'emplois optimisée
Usage: python run_search.py
"""
import sys
import os
sys.path.insert(0, 'src')

from linkedin_mcp.search_clean import search_seo_jobs_paris

if __name__ == "__main__":
    search_seo_jobs_paris()