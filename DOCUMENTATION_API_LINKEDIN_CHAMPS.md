# 📋 DOCUMENTATION COMPLÈTE - CHAMPS API LINKEDIN

**Version :** 1.0  
**Date :** 23 août 2025  
**Analysé sur :** linkedin-api Python  
**Méthodes testées :** `search_jobs()`, `get_job()`

---

## 🎯 **MÉTHODES PRINCIPALES DISPONIBLES**

### **📊 MÉTHODES DE RECHERCHE**
- **`search_jobs(keywords, location, limit)`** - Recherche d'emplois avec critères
- **`search_companies(keywords)`** - Recherche d'entreprises
- **`search_people(keywords)`** - Recherche de profils
- **`search(keywords)`** - Recherche générale

### **🔍 MÉTHODES D'EXTRACTION DÉTAILLÉE**
- **`get_job(job_id)`** - Détails complets d'un emploi spécifique
- **`get_job_skills(job_id)`** - Compétences associées à un emploi
- **`get_company(company_id)`** - Informations complètes entreprise
- **`get_profile(profile_id)`** - Profil complet utilisateur

### **📞 AUTRES MÉTHODES UTILES**
- **`get_company_updates(company_id)`** - Actualités entreprise
- **`get_profile_experiences(profile_id)`** - Expériences professionnelles
- **`get_profile_skills(profile_id)`** - Compétences d'un profil

---

## 📊 **STRUCTURE COMPLÈTE DES DONNÉES D'EMPLOI**

### **🔍 BASIC_INFO (Résultats de `search_jobs()`)**

#### **Champs Principaux**
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `title` | str | Titre de l'emploi | "Lead Marketing Developer - Growth" |
| `entityUrn` | str | Identifiant unique LinkedIn | "urn:li:fsd_jobPosting:4232920689" |
| `trackingUrn` | str | URN de tracking | "urn:li:jobPosting:4232920689" |
| `posterId` | str | ID de la personne qui a posté | "331296772" |
| `repostedJob` | bool | Emploi reposté ou non | true/false |
| `contentSource` | str | Source du contenu | "JOBS_PREMIUM_OFFLINE" |

#### **Champs Techniques**
| Champ | Type | Description | Valeur |
|-------|------|-------------|-------|
| `$recipeTypes` | list | Types de recette LinkedIn | ["com.linkedin.deco.recipe.anonymous.Anon1578943416"] |
| `$type` | str | Type d'objet LinkedIn | "com.linkedin.voyager.dash.jobs.JobPosting" |

---

### **🔬 DETAILED_INFO (Résultats de `get_job(job_id)`)**

#### **Champs de Base Étendus**
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `dashEntityUrn` | str | URN dashboard | "urn:li:fsd_jobPosting:4232920689" |
| `title` | str | Titre (répété) | "Lead Marketing Developer - Growth" |
| `entityUrn` | str | URN normalisé | "urn:li:fs_normalized_jobPosting:4232920689" |
| `jobPostingId` | int | ID numérique | 4232920689 |
| `jobState` | str | État de l'emploi | "LISTED" |
| `talentHubJob` | bool | Emploi Talent Hub | true/false |

#### **🏢 INFORMATIONS ENTREPRISE (companyDetails)**
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `name` | str | Nom de l'entreprise | "Voodoo" |
| `entityUrn` | str | URN entreprise | "urn:li:fs_normalized_company:5353630" |
| `universalName` | str | Nom universel LinkedIn | "voodoo.io" |
| `url` | str | URL profil LinkedIn entreprise | "https://www.linkedin.com/company/voodoo.io" |

#### **🖼️ LOGO ENTREPRISE (logo)**
| Champ | Type | Description | Valeurs |
|-------|------|-------------|---------|
| `type` | str | Type de logo | "SQUARE_LOGO" |
| `rootUrl` | str | URL racine images | "https://media.licdn.com/dms/image/..." |
| `artifacts` | list | Versions du logo | [100x100, 200x200, 400x400] |

#### **📝 DESCRIPTION COMPLÈTE (description)**
| Champ | Type | Description | Utilisation |
|-------|------|-------------|-------------|
| `text` | str | **TEXTE PRINCIPAL** | Analyse de pertinence, scoring |
| `attributes` | list | Formatage (gras, saut ligne) | Parsing HTML-like |

#### **📍 LOCALISATION ET MODE DE TRAVAIL**
| Champ | Type | Description | Valeurs Possibles |
|-------|------|-------------|-------------------|
| `formattedLocation` | str | Localisation formatée | "Paris, Île-de-France, France" |
| `workRemoteAllowed` | bool | Télétravail autorisé | true/false |
| `workplaceTypes` | list | Types de lieu de travail | ["urn:li:fs_workplaceType:1"] |

#### **🌍 TYPES DE LIEU DE TRAVAIL (workplaceTypesResolutionResults)**
| Code | Type | Description |
|------|------|-------------|
| `workplaceType:1` | On-site | Sur site |
| `workplaceType:2` | Remote | Télétravail |
| `workplaceType:3` | Hybrid | Hybride |

#### **🔗 CANDIDATURE (applyMethod)**
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `companyApplyUrl` | str | URL de candidature externe | "https://jobs.ashbyhq.com/..." |
| `applyStartersPreferenceVoid` | bool | Préférence annulée | true/false |
| `inPageOffsiteApply` | bool | Candidature externe dans la page | true/false |

#### **⏰ MÉTADONNÉES TEMPORELLES**
| Champ | Type | Description | Format |
|-------|------|-------------|-------|
| `listedAt` | int | Timestamp de publication | 1755946649000 (Unix timestamp) |

---

## 🛠️ **EXTRACTION PRATIQUE DES CHAMPS**

### **🔍 Code d'Extraction Standard**
```python
from linkedin_api import Linkedin

# Initialisation
linkedin = Linkedin(email, password)

# Recherche de base
jobs = linkedin.search_jobs(
    keywords="Product Manager",
    location="Paris, France", 
    limit=10
)

# Pour chaque emploi
for job in jobs:
    # Champs de base
    title = job.get('title', 'N/A')
    entity_urn = job.get('entityUrn', '')
    
    # Extraction détails complets
    if entity_urn:
        job_id = entity_urn.split(':')[-1]
        details = linkedin.get_job(job_id)
        
        if details:
            # Description complète
            description = ""
            if 'description' in details and 'text' in details['description']:
                description = details['description']['text']
            
            # Nom entreprise
            company_name = "N/A"
            if 'companyDetails' in details:
                comp_details = details['companyDetails']
                for key in comp_details:
                    if 'companyResolutionResult' in comp_details[key]:
                        comp_result = comp_details[key]['companyResolutionResult']
                        if 'name' in comp_result:
                            company_name = comp_result['name']
            
            # Localisation
            location = details.get('formattedLocation', 'N/A')
            
            # Télétravail
            remote = details.get('workRemoteAllowed', False)
            
            # URL candidature
            apply_url = ""
            if 'applyMethod' in details:
                apply_method = details['applyMethod']
                for key in apply_method:
                    if 'companyApplyUrl' in apply_method[key]:
                        apply_url = apply_method[key]['companyApplyUrl']
            
            # Date publication
            listed_at = details.get('listedAt', 0)
            if listed_at:
                from datetime import datetime
                posted_date = datetime.fromtimestamp(listed_at / 1000)
```

---

## 🎯 **CHAMPS LES PLUS UTILES POUR L'ANALYSE**

### **🏆 PRIORITÉ MAXIMALE (Obligatoires)**
1. **`title`** (basic_info) - Titre pour première analyse
2. **`description.text`** (detailed_info) - **ESSENTIEL pour scoring avancé**
3. **`companyDetails.*.companyResolutionResult.name`** - Nom entreprise
4. **`entityUrn`** - Identifiant pour extraction détaillée

### **⭐ PRIORITÉ HAUTE (Très utiles)**
5. **`formattedLocation`** - Géolocalisation précise
6. **`workRemoteAllowed`** - Information télétravail
7. **`listedAt`** - Date de publication (fraîcheur)
8. **`applyMethod.*.companyApplyUrl`** - URL candidature directe

### **📊 PRIORITÉ MOYENNE (Utiles)**
9. **`workplaceTypesResolutionResults`** - Type de travail (hybride, etc.)
10. **`companyDetails.*.companyResolutionResult.url`** - Profil LinkedIn entreprise
11. **`companyDetails.*.companyResolutionResult.logo`** - Logo pour présentation
12. **`jobState`** - État de l'offre (LISTED/CLOSED)

### **⚙️ PRIORITÉ BASSE (Techniques)**
13. **`posterId`** - Identification du recruteur
14. **`repostedJob`** - Détection republication
15. **`talentHubJob`** - Type d'offre LinkedIn
16. **`description.attributes`** - Formatage texte (gras, sauts ligne)

---

## 🔬 **CHAMPS AVANCÉS POUR ANALYSES SPÉCIFIQUES**

### **📈 ANALYSE DE PERTINENCE MÉTIER**
```python
# Champs essentiels pour scoring intelligent
essential_fields = {
    'content_analysis': [
        'title',                    # Analyse titre
        'description.text',         # Analyse description complète  
    ],
    'context_analysis': [
        'companyDetails.*.name',           # Secteur d'activité
        'formattedLocation',        # Géolocalisation
        'workRemoteAllowed',        # Flexibilité travail
    ],
    'freshness_analysis': [
        'listedAt',                 # Date publication
        'repostedJob',             # Republication
    ]
}
```

### **🎯 FILTRAGE ET SEGMENTATION**
```python
# Champs pour filtres avancés
filtering_fields = {
    'geo_filtering': [
        'formattedLocation',        # Ville/région
        'workplaceTypes',          # Type lieu travail
    ],
    'company_filtering': [
        'companyDetails.*.name',           # Nom entreprise
        'companyDetails.*.universalName',  # Handle LinkedIn
        'companyDetails.*.url',            # Profil LinkedIn
    ],
    'temporal_filtering': [
        'listedAt',                # Date publication
        'jobState',               # État offre
    ]
}
```

### **🚀 AUTOMATISATION CANDIDATURES**
```python
# Champs pour candidature automatique
application_fields = {
    'direct_apply': [
        'applyMethod.*.companyApplyUrl',   # URL candidature
        'applyMethod.*.inPageOffsiteApply', # Type candidature
    ],
    'tracking': [
        'entityUrn',               # ID unique
        'jobPostingId',           # ID numérique
        'trackingUrn',            # URN tracking
    ]
}
```

---

## ⚡ **OPTIMISATIONS DE PERFORMANCE**

### **🔄 RATE LIMITING**
- **Recherche** : `search_jobs()` - 1 requête pour N emplois
- **Détails** : `get_job()` - 1 requête par emploi
- **Recommandation** : Pause de 1-2 secondes entre requêtes `get_job()`

### **📊 STRATÉGIE D'EXTRACTION**
```python
# Extraction optimisée
def optimized_extraction():
    # 1. Recherche groupée (efficace)
    jobs = linkedin.search_jobs(keywords="Python", limit=50)  # 1 requête
    
    # 2. Extraction détails (coûteux)
    for job in jobs:
        time.sleep(1)  # Rate limiting
        details = linkedin.get_job(job_id)  # 1 requête par emploi
        
        # 3. Extraction ciblée des champs essentiels seulement
        extract_essential_fields(details)
```

---

## 📚 **EXEMPLES D'UTILISATION PAR CAS D'USAGE**

### **🎯 CAS 1: Analyse de Pertinence Métier**
```python
def analyze_job_relevance(job_basic, job_details):
    """Analyse optimisée pour pertinence métier"""
    
    # Champs essentiels
    title = job_basic.get('title', '')
    description = job_details.get('description', {}).get('text', '')
    company = extract_company_name(job_details)
    location = job_details.get('formattedLocation', '')
    
    # Analyse avec ces 4 champs principaux
    return score_relevance(title, description, company, location)
```

### **🌍 CAS 2: Filtrage Géographique et Télétravail**
```python
def filter_by_location_and_remote(job_details):
    """Filtrage par localisation et télétravail"""
    
    location = job_details.get('formattedLocation', '')
    remote_allowed = job_details.get('workRemoteAllowed', False)
    
    # Extraire type de travail (hybride/présentiel/remote)
    workplace_types = extract_workplace_types(job_details)
    
    return {
        'location': location,
        'remote': remote_allowed,
        'workplace_type': workplace_types
    }
```

### **🚀 CAS 3: Candidature Automatisée**
```python
def prepare_auto_application(job_details):
    """Préparation candidature automatique"""
    
    # URL candidature directe
    apply_url = extract_apply_url(job_details)
    
    # Métadonnées pour suivi
    job_id = job_details.get('jobPostingId')
    entity_urn = job_details.get('entityUrn')
    posted_date = job_details.get('listedAt')
    
    return {
        'apply_url': apply_url,
        'tracking': {
            'job_id': job_id,
            'urn': entity_urn,
            'posted': datetime.fromtimestamp(posted_date/1000)
        }
    }
```

---

## 🎯 **RÉSUMÉ EXÉCUTIF**

### **🏆 CHAMPS INCONTOURNABLES (4 essentiels)**
1. **`title`** - Titre emploi
2. **`description.text`** - Description complète 
3. **`companyDetails.*.name`** - Nom entreprise
4. **`formattedLocation`** - Localisation

### **⭐ CHAMPS AVANCÉS (8 très utiles)**
5. **`entityUrn`** - ID unique
6. **`workRemoteAllowed`** - Télétravail
7. **`listedAt`** - Date publication
8. **`applyMethod.*.companyApplyUrl`** - URL candidature
9. **`workplaceTypes`** - Mode de travail
10. **`jobState`** - État offre
11. **`companyDetails.*.url`** - Profil LinkedIn entreprise
12. **`repostedJob`** - Détection republication

### **🎯 MÉTHODES CLÉS À MAÎTRISER**
- **`search_jobs(keywords, location, limit)`** → Recherche de base
- **`get_job(job_id)`** → Détails complets
- **`get_job_skills(job_id)`** → Compétences associées (bonus)

**Total de champs utiles identifiés : 20+ champs principaux avec 50+ sous-champs disponibles**

---

*Documentation créée le 23/08/2025 - Basée sur tests réels avec linkedin-api*  
*Testée sur des emplois réels extraits de LinkedIn*  
*Méthodes validées : search_jobs() + get_job()*