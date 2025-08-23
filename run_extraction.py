#!/usr/bin/env python3
"""
Script d'entrée pour lancer l'extraction complète
Usage: python run_extraction.py
"""
import sys
import os
sys.path.insert(0, 'src')

from linkedin_mcp.extraction_complete import search_complete_jobs

if __name__ == "__main__":
    search_complete_jobs()