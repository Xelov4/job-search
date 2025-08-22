# 🔌 LinkedIn API - Documentation technique

## 🎯 Vue d'ensemble

Le projet utilise la bibliothèque **`linkedin-api`** (version 2.3.1+), une API Python non-officielle qui permet d'interagir avec LinkedIn via des requêtes HTTP simulant un navigateur web.

## 📦 Installation et configuration

### Installation
```bash
pip install linkedin-api==2.3.1
pip install python-dotenv>=1.1.1
```

### Configuration
```python
from linkedin_api import Linkedin
import os
from dotenv import load_dotenv

load_dotenv()

linkedin = Linkedin(
    username=os.getenv("LINKEDIN_EMAIL"),
    password=os.getenv("LINKEDIN_PASSWORD"),
    debug=False  # True pour logs détaillés
)
```

## 🔑 Authentification

### Méthode utilisée
```python
def get_creds():
    return Linkedin(
        os.getenv("LINKEDIN_EMAIL"), 
        os.getenv("LINKEDIN_PASSWORD"), 
        debug=True
    )
```

### Variables d'environnement (.env)
```env
LINKEDIN_EMAIL=votre_email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe
```

### Gestion des sessions
- **Session persistante** : Réutilisée pendant toute la durée du script
- **Cookies automatiques** : Gestion transparente des cookies LinkedIn
- **Rate limiting** : Respect automatique des limites LinkedIn
- **Expiration** : Session peut expirer, nécessite ré-authentification

## 🔍 Méthodes principales

### 1. `search_jobs(keywords, location, limit)`

#### Description
Recherche d'emplois avec critères personnalisables.

#### Paramètres
```python
search_results = linkedin.search_jobs(
    keywords="SEO",                    # Mots-clés de recherche
    location="Paris, France",          # Localisation (optionnel)
    limit=10,                         # Nombre de résultats (1-1000)
    # Paramètres optionnels :
    experience_level="Entry level",    # Niveau d'expérience
    job_type="Full-time",             # Type de contrat
    remote_work="Remote",             # Travail à distance
    date_posted="r86400",             # Publié dans les 24h
    easy_apply=True                   # Candidature facile uniquement
)
```

#### Valeurs possibles

**experience_level** :
- `"Internship"`
- `"Entry level"`
- `"Associate"`
- `"Mid-Senior level"`
- `"Director"`
- `"Executive"`

**job_type** :
- `"Full-time"`
- `"Part-time"`
- `"Contract"`
- `"Temporary"`
- `"Volunteer"`
- `"Internship"`

**remote_work** :
- `"Remote"`
- `"On-site"`
- `"Hybrid"`

**date_posted** :
- `"r86400"` - 24 heures
- `"r604800"` - 7 jours
- `"r2592000"` - 30 jours

#### Structure de réponse
```python
[
    {
        "trackingUrn": "urn:li:jobPosting:4289767612",
        "repostedJob": false,
        "title": "Responsable marketing",
        "$recipeTypes": ["com.linkedin.deco.recipe.anonymous.Anon1578943416"],
        "posterId": "677395806",
        "$type": "com.linkedin.voyager.dash.jobs.JobPosting",
        "contentSource": "JOBS_PREMIUM",
        "entityUrn": "urn:li:fsd_jobPosting:4289767612"
    }
]
```

### 2. `get_job(job_id)`

#### Description
Récupère les détails complets d'un emploi spécifique.

#### Paramètre
```python
job_id = "4289767612"  # ID extrait de entityUrn
job_details = linkedin.get_job(job_id)
```

#### Extraction de l'ID
```python
job_id = job['entityUrn'].split(':')[-1]
# "urn:li:fsd_jobPosting:4289767612" → "4289767612"
```

#### Structure de réponse complète
```python
{
    "dashEntityUrn": "urn:li:fsd_jobPosting:4289767612",
    "companyDetails": {
        "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany": {
            "companyResolutionResult": {
                "entityUrn": "urn:li:fs_normalized_company:100669449",
                "name": "Keez",
                "logo": {
                    "image": {
                        "com.linkedin.common.VectorImage": {
                            "artifacts": [
                                {
                                    "width": 200,
                                    "height": 200,
                                    "fileIdentifyingUrlPathSegment": "...",
                                    "expiresAt": 1758758400000
                                }
                            ],
                            "rootUrl": "https://media.licdn.com/dms/image/v2/..."
                        }
                    }
                },
                "universalName": "keez-app",
                "url": "https://www.linkedin.com/company/keez-app"
            }
        }
    },
    "jobState": "LISTED",
    "description": {
        "attributes": [...],
        "text": "Description complète du poste..."
    },
    "title": "Responsable marketing",
    "entityUrn": "urn:li:fs_normalized_jobPosting:4289767612",
    "workRemoteAllowed": false,
    "applyMethod": {
        "com.linkedin.voyager.jobs.ComplexOnsiteApply": {
            "unifyApplyEnabled": true,
            "easyApplyUrl": "https://www.linkedin.com/job-apply/4289767612"
        }
    },
    "formattedLocation": "Paris, Île-de-France, France",
    "workplaceTypes": ["urn:li:fs_workplaceType:3"],
    "listedAt": 1755856353000,
    "jobPostingId": 4289767612,
    "workplaceTypesResolutionResults": {
        "urn:li:fs_workplaceType:3": {
            "localizedName": "Hybrid",
            "entityUrn": "urn:li:fs_workplaceType:3"
        }
    }
}
```

### 3. `get_profile()`

#### Description
Récupère le profil de l'utilisateur connecté.

#### Utilisation
```python
profile = linkedin.get_profile()
```

### 4. `get_feed_posts(limit, offset)`

#### Description
Récupère les posts du feed LinkedIn.

#### Paramètres
```python
posts = linkedin.get_feed_posts(
    limit=10,     # Nombre de posts
    offset=0      # Décalage pour pagination
)
```

## 🏷️ Types et URNs LinkedIn

### Types de lieux de travail
```python
workplace_mapping = {
    'urn:li:fs_workplaceType:1': 'Sur site',
    'urn:li:fs_workplaceType:2': 'Hybride', 
    'urn:li:fs_workplaceType:3': 'Distanciel'
}
```

### Types de sources de contenu
- `JOBS_PREMIUM` : Emplois premium
- `JOBS_PREMIUM_OFFLINE` : Emplois premium hors ligne
- `JOBS_CREATE` : Emplois créés manuellement

### Types de candidature
- `com.linkedin.voyager.jobs.SimpleOnsiteApply` : Candidature simple
- `com.linkedin.voyager.jobs.ComplexOnsiteApply` : Candidature complexe avec Easy Apply
- `com.linkedin.voyager.jobs.OffsiteApply` : Candidature externe

## ⚠️ Limitations et contraintes

### Rate Limiting
- **LinkedIn** applique des limites strictes
- **Recommandation** : Max 50-100 requêtes/heure
- **Gestion** : Pauses automatiques entre requêtes
- **Symptômes** : Erreurs 429, timeouts

### Restriction de données
- **Données partielles** selon le type de compte
- **Variations** entre comptes gratuits/premium
- **Champs manquants** pour certains emplois
- **Localisation** peut affecter la disponibilité

### Stabilité de l'API
- **API non-officielle** → peut changer
- **Structure** des données peut évoluer
- **Nouveaux champs** apparaissent régulièrement
- **Compatibilité** avec les versions LinkedIn

## 🛠️ Gestion d'erreurs

### Erreurs courantes

#### Authentification échouée
```python
try:
    linkedin = Linkedin(email, password)
except Exception as e:
    print(f"Erreur d'authentification: {e}")
    # Vérifier email/password
    # Compte peut être verrouillé
```

#### Rate limit dépassé
```python
try:
    results = linkedin.search_jobs(...)
except Exception as e:
    if "rate limit" in str(e).lower():
        print("Rate limit atteint, attendre...")
        time.sleep(3600)  # Attendre 1 heure
```

#### Données manquantes
```python
job_details = linkedin.get_job(job_id)
if not job_details:
    print(f"Aucun détail pour l'emploi {job_id}")
    # Emploi peut être supprimé/expiré
```

### Gestion robuste
```python
def safe_get_job(linkedin, job_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return linkedin.get_job(job_id)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Backoff exponentiel
                continue
            print(f"Échec définitif pour {job_id}: {e}")
            return None
```

## 📊 Performance et optimisation

### Bonnes pratiques
```python
# Réutiliser la session
linkedin = Linkedin(email, password)
# Utiliser pour toutes les requêtes

# Traitement par batch
for batch in chunks(job_ids, 10):
    for job_id in batch:
        job_details = linkedin.get_job(job_id)
        time.sleep(1)  # Pause entre requêtes
```

### Monitoring
```python
import time
start_time = time.time()

# Opérations...

end_time = time.time()
print(f"Durée: {end_time - start_time:.2f}s")
print(f"Requêtes/seconde: {num_requests / (end_time - start_time):.2f}")
```

## 🔒 Sécurité

### Protection des identifiants
```python
# ✅ Correct
linkedin = Linkedin(
    os.getenv("LINKEDIN_EMAIL"),
    os.getenv("LINKEDIN_PASSWORD")
)

# ❌ À éviter
linkedin = Linkedin("email@domain.com", "password123")
```

### Logs sécurisés
```python
if debug:
    # Ne jamais logger les identifiants
    print(f"Connexion pour: {os.getenv('LINKEDIN_EMAIL')}")
    print(f"Mot de passe: {'*' * len(os.getenv('LINKEDIN_PASSWORD'))}")
```

## 📈 Évolutions futures

### Nouvelles fonctionnalités possibles
- `search_companies()` - Recherche d'entreprises
- `search_people()` - Recherche de personnes
- `get_company_jobs()` - Emplois d'une entreprise spécifique
- `get_job_applicants()` - Candidats d'un emploi (si autorisé)

### Amélirations attendues
- **Cache** intégré pour les requêtes
- **Retry automatique** avec backoff
- **Pagination** améliorée
- **Filtres avancés** supplémentaires

---

*Documentation LinkedIn API - Version 1.0 - Août 2025*