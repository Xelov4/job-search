# 📚 Manuel Complet - Serveur MCP LinkedIn

## 🎯 Vue d'ensemble du projet

Ce projet implémente un serveur **Model Context Protocol (MCP)** pour LinkedIn, permettant d'automatiser la recherche d'emplois, la récupération de profils, et l'analyse du feed LinkedIn via des appels API programmatiques.

### 🚀 Fonctionnalités principales
- **Recherche d'emplois** avec critères personnalisables
- **Récupération de profils** utilisateur
- **Analyse du feed** LinkedIn
- **Extraction de détails** d'emplois spécifiques
- **Interface MCP** standardisée pour l'intégration

---

## 📁 Structure du projet

```
linkedin-mcp/
├── src/
│   ├── __init.py__
│   └── linkedin.py          # Serveur MCP principal
├── venv/                    # Environnement virtuel Python
├── .env                     # Variables d'environnement
├── pyproject.toml          # Configuration du projet
├── Dockerfile              # Configuration Docker
├── smithery.yaml           # Configuration Smithery
├── test_search.py          # Script de test basique
├── test_search_enhanced.py # Script de test amélioré
├── final_search.py         # Script de recherche final
├── search_results_raw.json # Résultats bruts de recherche
└── manual.md               # Ce manuel
```

---

## 🔧 Installation et configuration

### 1. Prérequis
- Python 3.12+
- Compte LinkedIn actif
- Accès Internet

### 2. Installation
```bash
# Cloner le projet
git clone https://github.com/hritik003/linkedin-mcp.git
cd linkedin-mcp

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -e .
```

### 3. Configuration des identifiants
Créer le fichier `.env` :
```env
LINKEDIN_EMAIL=votre_email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe
```

### 4. Configuration MCP
Créer `~/.config/mcp/servers/linkedin.json` :
```json
{
    "mcpServers": {
        "linkedin": {
            "command": "/chemin/vers/linkedin-mcp/venv/bin/python",
            "args": ["/chemin/vers/linkedin-mcp/src/linkedin.py"],
            "env": {
                "PYTHONPATH": "/chemin/vers/linkedin-mcp/src"
            }
        }
    }
}
```

---

## 🎯 Scripts de récupération des annonces

### 📋 `final_search.py` - Script principal de recherche

**Objectif** : Script complet et optimisé pour la recherche d'emplois avec récupération de tous les détails disponibles.

#### 🔍 Fonctionnalités
- Recherche d'emplois par mots-clés et localisation
- Récupération des détails complets de chaque emploi
- Formatage des résultats en français
- Sauvegarde automatique des résultats
- Gestion d'erreurs robuste

#### 📝 Utilisation
```bash
cd linkedin-mcp
source venv/bin/activate
python final_search.py
```

#### 🎛️ Paramètres de recherche
```python
# Recherche d'emplois SEO à Paris
search_results = linkedin.search_jobs(
    keywords="SEO",
    location="Paris, France",
    limit=10
)
```

#### 📊 Structure des résultats
Chaque emploi contient :
- **Titre** : Nom du poste
- **ID** : Identifiant unique LinkedIn
- **Source** : Type de publication (JOBS_PREMIUM, JOBS_CREATE, etc.)
- **Entreprise** : Nom de l'entreprise (si disponible)
- **Localisation** : Lieu du poste
- **Type** : Type de contrat
- **Expérience** : Niveau requis
- **Description** : Résumé du poste
- **Compétences** : Skills requis
- **Date** : Date de publication

#### 🔧 Fonctions internes

##### `format_timestamp(timestamp)`
Convertit les timestamps LinkedIn en dates lisibles.
```python
def format_timestamp(timestamp):
    if timestamp:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%d/%m/%Y %H:%M')
    return "Date inconnue"
```

##### `search_seo_jobs_paris()`
Fonction principale qui orchestre toute la recherche.
```python
def search_seo_jobs_paris():
    # 1. Initialisation de l'API
    # 2. Recherche d'emplois
    # 3. Récupération des détails
    # 4. Formatage des résultats
    # 5. Sauvegarde des données
```

---

### 📋 `test_search.py` - Script de test basique

**Objectif** : Test simple de l'API LinkedIn et affichage basique des résultats.

#### 🔍 Fonctionnalités
- Test de connexion à l'API
- Recherche simple d'emplois
- Affichage basique des résultats
- Gestion d'erreurs simple

#### 📝 Utilisation
```bash
python test_search.py
```

#### ⚠️ Limitations
- Affichage limité des détails
- Pas de récupération des détails complets
- Formatage basique des résultats

---

### 📋 `test_search_enhanced.py` - Script de test amélioré

**Objectif** : Version intermédiaire avec tentative de récupération de détails supplémentaires.

#### 🔍 Fonctionnalités
- Recherche d'emplois avec limite réduite
- Tentative de récupération des détails complets
- Sauvegarde des résultats bruts en JSON
- Gestion d'erreurs améliorée

#### 📝 Utilisation
```bash
python test_search_enhanced.py
```

#### 💾 Sortie
- Affichage des résultats dans le terminal
- Sauvegarde dans `search_results_raw.json`

---

## 🚀 Serveur MCP principal

### 📋 `src/linkedin.py` - Serveur MCP

**Objectif** : Implémentation du serveur MCP avec toutes les fonctionnalités exposées.

#### 🔧 Outils MCP disponibles

##### 1. `get_profile()`
Récupère le profil utilisateur connecté.
```python
@mcp.tool()
def get_profile():
    """Retrieves the User Profile"""
    linkedin = get_creds()
    profile = linkedin.get_profile()
    return profile
```

##### 2. `get_feed_posts(limit: int = 10, offset: int = 0)`
Récupère les posts du feed LinkedIn.
```python
@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """Retrieve LinkedIn feed posts"""
    # Implémentation...
```

##### 3. `search_jobs(keywords: str, location: str = None, limit: int = 10)`
Recherche d'emplois avec critères personnalisables.
```python
@mcp.tool()
def search_jobs(keywords: str, location: str = None, limit: int = 10) -> str:
    """Search for jobs on LinkedIn with specified criteria"""
    # Implémentation complète...
```

##### 4. `get_job_details(job_id: str)`
Récupère les détails complets d'un emploi spécifique.
```python
@mcp.tool()
def get_job_details(job_id: str) -> str:
    """Get detailed information about a specific job"""
    # Implémentation...
```

#### 🔑 Fonction d'authentification
```python
def get_creds():
    return Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=True
    )
```

---

## 📊 API LinkedIn sous-jacente

### 🔍 Méthodes disponibles
L'API LinkedIn fournit ces méthodes principales :
- `search_jobs()` - Recherche d'emplois
- `get_job()` - Détails d'un emploi
- `get_profile()` - Profil utilisateur
- `get_feed_posts()` - Posts du feed
- `search_companies()` - Recherche d'entreprises
- `search_people()` - Recherche de personnes

### 📋 Paramètres de recherche d'emplois
```python
linkedin.search_jobs(
    keywords="SEO",           # Mots-clés de recherche
    location="Paris, France", # Localisation
    limit=10,                 # Nombre de résultats
    # Paramètres optionnels :
    # experience_level="Entry level"
    # job_type="Full-time"
    # remote_work="Remote"
    # date_posted="r86400"  # 24h
)
```

---

## 🎯 Cas d'usage pratiques

### 1. Recherche d'emplois SEO à Paris
```bash
python final_search.py
```
**Résultat** : 10 emplois trouvés avec détails complets

### 2. Recherche via MCP
```python
# Utilisation du serveur MCP
from linkedin_mcp import search_jobs

jobs = search_jobs("SEO", "Paris, France", 15)
```

### 3. Surveillance continue
```bash
# Script automatisé
while true; do
    python final_search.py
    sleep 3600  # Attendre 1 heure
done
```

---

## 🔧 Personnalisation et extension

### 📝 Ajout de nouveaux critères de recherche
```python
# Dans final_search.py
search_results = linkedin.search_jobs(
    keywords="SEO",
    location="Paris, France",
    limit=20,
    experience_level="Senior",
    job_type="Full-time",
    remote_work="Hybrid"
)
```

### 🎨 Modification du format de sortie
```python
# Personnaliser l'affichage
print(f"🏢 {company}")
print(f"📍 {location}")
print(f"💰 {salary_range}")
```

### 💾 Sauvegarde personnalisée
```python
# Sauvegarder en CSV
import csv
with open('jobs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Titre', 'Entreprise', 'Localisation', 'Type'])
    # ... écriture des données
```

---

## ⚠️ Limitations et considérations

### 🔒 Sécurité
- **Ne jamais commiter** le fichier `.env`
- Utiliser des variables d'environnement sécurisées
- Limiter l'accès aux identifiants LinkedIn

### 📊 Limitations de l'API
- **Rate limiting** : Respecter les limites de l'API
- **Données partielles** : Certains champs peuvent être vides
- **Authentification** : Session LinkedIn peut expirer

### 🚫 Restrictions d'utilisation
- Respecter les conditions d'utilisation LinkedIn
- Ne pas surcharger l'API
- Utiliser à des fins personnelles/professionnelles légitimes

---

## 🐛 Dépannage

### ❌ Erreurs courantes

#### 1. "Impossible de récupérer les détails"
```python
# Solution : Vérifier l'ID de l'emploi
job_id = job['entityUrn'].split(':')[-1]
print(f"ID extrait : {job_id}")
```

#### 2. "Erreur d'authentification"
```bash
# Vérifier le fichier .env
cat .env
# Vérifier la connexion
python -c "from linkedin_api import Linkedin; print('OK')"
```

#### 3. "Aucun emploi trouvé"
```python
# Essayer avec des mots-clés plus larges
keywords="digital marketing"  # Au lieu de "SEO"
location="France"            # Au lieu de "Paris, France"
```

### 🔍 Debug
```python
# Activer le debug
linkedin = Linkedin(email, password, debug=True)

# Vérifier les variables d'environnement
print(f"Email: {os.getenv('LINKEDIN_EMAIL')}")
print(f"Password: {'*' * len(os.getenv('LINKEDIN_PASSWORD', ''))}")
```

---

## 📈 Améliorations futures

### 🚀 Fonctionnalités à ajouter
- [ ] **Filtres avancés** : Salaire, compétences, secteur
- [ ] **Alertes** : Notifications pour nouveaux emplois
- [ ] **Analyse** : Statistiques du marché
- [ ] **Export** : Formats CSV, Excel, PDF
- [ ] **Interface web** : Dashboard de recherche
- [ ] **Base de données** : Stockage des résultats
- [ ] **API REST** : Endpoints HTTP

### 🔧 Optimisations techniques
- [ ] **Cache** : Mise en cache des résultats
- [ ] **Parallélisation** : Recherches simultanées
- [ ] **Retry logic** : Gestion des échecs
- [ ] **Logging** : Traçabilité complète
- [ ] **Tests** : Suite de tests automatisés

---

## 📚 Ressources et références

### 🔗 Liens utiles
- [Repository GitHub](https://github.com/hritik003/linkedin-mcp)
- [Documentation MCP](https://modelcontextprotocol.io/)
- [API LinkedIn non-officielle](https://github.com/tomquirk/linkedin-api)

### 📖 Documentation technique
- [FastMCP Documentation](https://fastmcp.com/)
- [Python LinkedIn API](https://pypi.org/project/linkedin-api/)
- [Protocol MCP](https://github.com/modelcontextprotocol/spec)

---

## 🤝 Contribution

### 📝 Comment contribuer
1. Fork le projet
2. Créer une branche feature
3. Implémenter les améliorations
4. Tester avec `python final_search.py`
5. Soumettre une pull request

### 🐛 Signaler un bug
- Utiliser les Issues GitHub
- Inclure les logs d'erreur
- Décrire les étapes de reproduction

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

## 👨‍💻 Auteurs

- **Hritik Raj** - Développeur principal
- **Henry Mao** - Contributeur

---

*Dernière mise à jour : Août 2025*
*Version du manuel : 1.0*
