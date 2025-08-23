#!/usr/bin/env python3
"""
Script d'entrée pour lancer le serveur MCP
Usage: python run_server.py
"""
import sys
import os
sys.path.insert(0, 'src')

from linkedin_mcp.server import mcp

if __name__ == "__main__":
    mcp.run()