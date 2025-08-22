# 🚀 Exemples d'utilisation - LinkedIn Job Search MCP

## 🎯 Introduction

Ce guide présente des exemples concrets d'utilisation du système LinkedIn Job Search MCP, depuis les cas les plus simples jusqu'aux utilisations avancées.

## 📋 Cas d'usage de base

### 1. Recherche simple d'emplois SEO

```bash
# Recherche basique avec le script optimisé
cd linkedin-mcp
source venv/bin/activate
python final_search_clean.py
```

**Résultat attendu :**
```
🔍 Recherche d'emplois SEO à Paris, France...
✅ 10 emplois trouvés !

📋 **Emploi 1**
   Titre: Search Engine Optimization Team Lead
   Entreprise: Six Values
   Localisation: EMEA
   Type: Distanciel
   ...
```

### 2. Extraction complète avec analyse

```bash
# Extraction exhaustive de toutes les données
python complete_extraction.py
```

**Fichiers générés :**
- `complete_extraction_YYYYMMDD_HHMMSS.json` (65+ Ko)
- Données structurées prêtes pour l'analyse

## 🔧 Personnalisation des recherches

### 1. Modification des critères de recherche

#### A. Recherche par mots-clés spécifiques
```python
# Dans final_search_clean.py, modifier :
search_results = linkedin.search_jobs(
    keywords="Marketing Digital OR SEO OR SEM",  # ← Recherche élargie
    location="Paris, France",
    limit=10
)
```

#### B. Recherche géographique étendue
```python
search_results = linkedin.search_jobs(
    keywords="SEO",
    location="France",  # ← Plus large que "Paris"
    limit=20           # ← Plus de résultats
)
```

#### C. Recherche par secteur d'activité
```python
search_results = linkedin.search_jobs(
    keywords="SEO manager fintech startup",  # ← Secteur ciblé
    location="Paris, Île-de-France, France",
    limit=15
)
```

### 2. Filtres avancés dans complete_extraction.py

```python
# Modifier dans search_complete_jobs() :
def search_complete_jobs():
    # ... code existant ...
    
    # Filtrage post-recherche
    filtered_jobs = []
    for job_data in all_jobs_complete:
        if job_data['detailed_data']:
            company = job_data['detailed_data']['company']['name']
            workplace = job_data['detailed_data']['workplace']
            
            # Filtrer par type de travail
            if any('Remote' in wt['localized_name'] for wt in workplace['detailed_types']):
                filtered_jobs.append(job_data)
    
    return filtered_jobs
```

## 📊 Cas d'usage analytiques

### 1. Veille concurrentielle

```bash
#!/bin/bash
# Script : competitive_watch.sh

cd /path/to/linkedin-mcp
source venv/bin/activate

# Rechercher les emplois de concurrents spécifiques
python -c "
from complete_extraction import *
import json

# Recherche ciblée concurrents
linkedin = Linkedin(os.getenv('LINKEDIN_EMAIL'), os.getenv('LINKEDIN_PASSWORD'))

competitors = ['Google', 'Meta', 'Amazon']
all_competitor_jobs = []

for competitor in competitors:
    print(f'🔍 Analyse {competitor}...')
    jobs = linkedin.search_jobs(
        keywords=f'company:{competitor} AND (SEO OR Marketing)',
        limit=20
    )
    all_competitor_jobs.extend(jobs)

print(f'📊 Total: {len(all_competitor_jobs)} emplois analysés')
"
```

### 2. Analyse de marché par région

```python
# Script personnalisé : market_analysis.py
from complete_extraction import search_complete_jobs
import json

def analyze_market_by_region():
    regions = [
        "Paris, Île-de-France, France",
        "Lyon, France", 
        "Marseille, France",
        "Toulouse, France",
        "Bordeaux, France"
    ]
    
    market_data = {}
    
    for region in regions:
        print(f"🔍 Analyse marché : {region}")
        
        # Modifier temporairement la recherche
        # ... logique de recherche par région ...
        
        market_data[region] = {
            'total_jobs': len(jobs),
            'remote_jobs': count_remote_jobs(jobs),
            'companies': extract_companies(jobs),
            'average_requirements': analyze_requirements(jobs)
        }
    
    return market_data
```

### 3. Monitoring automatique

```bash
#!/bin/bash
# Script : daily_monitoring.sh

SCRIPT_DIR="/path/to/linkedin-mcp"
LOG_DIR="$SCRIPT_DIR/logs"
DATA_DIR="$SCRIPT_DIR/data"

mkdir -p $LOG_DIR $DATA_DIR

cd $SCRIPT_DIR
source venv/bin/activate

# Recherche quotidienne
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/monitoring_$TIMESTAMP.log"

{
    echo "🚀 Début monitoring - $(date)"
    
    # Recherche SEO
    python complete_extraction.py
    
    # Archiver les résultats
    mv complete_extraction_*.json $DATA_DIR/
    
    echo "✅ Monitoring terminé - $(date)"
} >> $LOG_FILE 2>&1

# Notification (optionnel)
echo "Monitoring LinkedIn terminé. Voir $LOG_FILE" | mail -s "LinkedIn Job Monitoring" admin@domain.com
```

## 🔌 Utilisation du serveur MCP

### 1. Démarrage du serveur

```bash
# Méthode 1 : Direct
python src/linkedin.py

# Méthode 2 : Via MCP CLI (si installé)
mcp run linkedin

# Méthode 3 : Via configuration
mcp start --config ~/.config/mcp/servers/linkedin.json
```

### 2. Interaction avec le serveur MCP

```python
# Client MCP exemple
import json
from mcp_client import MCPClient

async def test_mcp_server():
    client = MCPClient("linkedin")
    
    # Recherche d'emplois via MCP
    result = await client.call_tool("search_jobs", {
        "keywords": "SEO Manager",
        "location": "Paris, France", 
        "limit": 5
    })
    
    jobs = json.loads(result)
    print(f"Trouvé {len(jobs)} emplois via MCP")
    
    # Détails d'un emploi spécifique
    if jobs:
        job_id = jobs[0]['entityUrn'].split(':')[-1]
        details = await client.call_tool("get_job_details", {
            "job_id": job_id
        })
        print(f"Détails emploi: {details[:100]}...")
```

## 🔄 Intégrations avancées

### 1. Intégration avec base de données

```python
# db_integration.py
import sqlite3
import json
from complete_extraction import search_complete_jobs

def setup_database():
    conn = sqlite3.connect('linkedin_jobs.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job_id TEXT UNIQUE,
            title TEXT,
            company TEXT,
            location TEXT,
            workplace_type TEXT,
            description TEXT,
            posted_date TEXT,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_data TEXT
        )
    ''')
    
    conn.commit()
    return conn

def store_jobs_in_db():
    jobs_data = search_complete_jobs()
    conn = setup_database()
    cursor = conn.cursor()
    
    for job in jobs_data:
        if job['detailed_data']:
            data = job['detailed_data']
            cursor.execute('''
                INSERT OR REPLACE INTO jobs 
                (job_id, title, company, location, workplace_type, description, posted_date, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['basic_info']['job_id'],
                data['basic_info']['title'],
                data['company']['name'],
                data['workplace']['formatted_location'],
                ', '.join([wt['localized_name'] for wt in data['workplace']['detailed_types']]),
                data['description']['text'],
                data['dates']['listed_at_formatted'],
                json.dumps(job)
            ))
    
    conn.commit()
    print(f"✅ {len(jobs_data)} emplois stockés en base")
```

### 2. API REST personnalisée

```python
# api_server.py
from flask import Flask, jsonify, request
from complete_extraction import search_complete_jobs
import json

app = Flask(__name__)

@app.route('/api/jobs/search', methods=['GET'])
def search_jobs_api():
    keywords = request.args.get('keywords', 'SEO')
    location = request.args.get('location', 'Paris, France')
    limit = int(request.args.get('limit', 10))
    
    # Adapter la recherche avec les paramètres
    jobs = search_complete_jobs()  # À adapter
    
    return jsonify({
        'status': 'success',
        'total': len(jobs),
        'jobs': jobs
    })

@app.route('/api/jobs/analyze', methods=['GET'])
def analyze_jobs():
    jobs = search_complete_jobs()
    
    analysis = {
        'total_jobs': len(jobs),
        'remote_percentage': calculate_remote_percentage(jobs),
        'top_companies': get_top_companies(jobs),
        'location_distribution': get_location_distribution(jobs)
    }
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. Dashboard de visualisation

```python
# dashboard.py avec Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
from complete_extraction import search_complete_jobs

def create_dashboard():
    st.title("📊 LinkedIn Job Search Dashboard")
    
    # Sidebar pour les paramètres
    st.sidebar.header("Paramètres de recherche")
    keywords = st.sidebar.text_input("Mots-clés", "SEO")
    location = st.sidebar.text_input("Localisation", "Paris, France")
    limit = st.sidebar.slider("Nombre d'emplois", 5, 50, 10)
    
    if st.sidebar.button("🔍 Rechercher"):
        with st.spinner("Recherche en cours..."):
            jobs_data = search_complete_jobs()  # À adapter avec les paramètres
            
            # Conversion en DataFrame
            df = convert_jobs_to_dataframe(jobs_data)
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total emplois", len(df))
            with col2:
                st.metric("Emplois remote", len(df[df['remote'] == True]))
            with col3:
                st.metric("Entreprises uniques", df['company'].nunique())
            with col4:
                st.metric("Postes dernières 24h", count_recent_jobs(df))
            
            # Graphiques
            fig_companies = px.bar(df['company'].value_counts().head(10), 
                                 title="Top 10 des entreprises")
            st.plotly_chart(fig_companies)
            
            fig_locations = px.pie(df, names='location', 
                                  title="Répartition géographique")
            st.plotly_chart(fig_locations)
            
            # Tableau détaillé
            st.subheader("📋 Détail des emplois")
            st.dataframe(df[['title', 'company', 'location', 'workplace_type', 'posted_date']])

if __name__ == "__main__":
    create_dashboard()
```

## 🔁 Automatisation et déploiement

### 1. Docker Compose pour production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  linkedin-scraper:
    build: .
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    command: ["python", "complete_extraction.py"]
    
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: linkedin_jobs
      POSTGRES_USER: linkedin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  api:
    build: .
    env_file:
      - .env
    ports:
      - "5000:5000"
    depends_on:
      - postgres
    command: ["python", "api_server.py"]

volumes:
  postgres_data:
```

### 2. GitHub Actions pour CI/CD

```yaml
# .github/workflows/linkedin-jobs.yml
name: LinkedIn Jobs Pipeline

on:
  schedule:
    - cron: '0 9 * * *'  # Tous les jours à 9h
  workflow_dispatch:

jobs:
  extract-jobs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        pip install -e .
        
    - name: Extract jobs
      env:
        LINKEDIN_EMAIL: ${{ secrets.LINKEDIN_EMAIL }}
        LINKEDIN_PASSWORD: ${{ secrets.LINKEDIN_PASSWORD }}
      run: |
        python complete_extraction.py
        
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: job-results
        path: complete_extraction_*.json
```

---

*Documentation des exemples d'utilisation - Version 1.0 - Août 2025*