# 📚 Documentation - LinkedIn Job Search MCP Server

## 🎯 Vue d'ensemble

Ce projet implémente un serveur **Model Context Protocol (MCP)** pour LinkedIn permettant l'automatisation de la recherche d'emplois, l'extraction de données complètes et l'analyse du marché de l'emploi via des appels API programmatiques.

## 📁 Structure de la documentation

```
docs/
├── README.md              # Ce fichier - Index de la documentation
├── architecture.md        # Architecture générale du projet
├── scripts/               # Documentation des scripts
│   ├── final_search.md    # Script de recherche basique
│   ├── final_search_clean.md  # Script de recherche optimisé
│   ├── complete_extraction.md # Script d'extraction complète
│   └── explore_all_data.md    # Script d'exploration
├── api/                  # Documentation API
│   ├── linkedin_api.md   # API LinkedIn sous-jacente
│   └── mcp_server.md     # Serveur MCP
├── setup/               # Guide d'installation
│   ├── installation.md  # Installation et configuration
│   └── configuration.md # Configuration avancée
└── examples/           # Exemples et cas d'usage
    ├── basic_usage.md  # Utilisation basique
    ├── advanced_usage.md # Utilisation avancée
    └── data_analysis.md  # Analyse des données
```

## 🚀 Démarrage rapide

1. **Installation** : Voir [setup/installation.md](setup/installation.md)
2. **Configuration** : Voir [setup/configuration.md](setup/configuration.md)  
3. **Premier test** : Voir [examples/basic_usage.md](examples/basic_usage.md)
4. **Architecture** : Voir [architecture.md](architecture.md)

## 📋 Scripts disponibles

| Script | Description | Documentation |
|--------|-------------|---------------|
| `final_search.py` | Recherche basique avec debug | [scripts/final_search.md](scripts/final_search.md) |
| `final_search_clean.py` | Recherche optimisée et propre | [scripts/final_search_clean.md](scripts/final_search_clean.md) |
| `complete_extraction.py` | Extraction complète de toutes les données | [scripts/complete_extraction.md](scripts/complete_extraction.md) |
| `explore_all_data.py` | Exploration de la structure des données | [scripts/explore_all_data.md](scripts/explore_all_data.md) |

## 🌐 Fonctionnalités nouvelles

### 📊 Extraction enrichie (Août 2025)
- **Extraction complète** de 20 emplois SEO avec toutes les données LinkedIn
- **Formats multiples** : JSON complet (143KB), Markdown lisible, HTML interactif
- **Logos d'entreprises** intégrés (3 tailles : 100x100, 200x200, 400x400px)
- **Données exhaustives** : descriptions formatées, liens de candidature, types de travail

### 🌐 Portail HTML/CSS
- **Page lobby interactive** pour naviguer entre les offres d'emploi
- **Design moderne** avec animations CSS, dégradés et effets hover
- **Interface responsive** compatible mobile/tablet/desktop
- **Intégration des logos** et ressources enrichies LinkedIn

## 🔧 Composants principaux

- **Serveur MCP** (`src/linkedin.py`) - Serveur principal avec outils MCP
- **Scripts d'extraction** - Collection de scripts spécialisés  
- **Configuration** (`.env`, `pyproject.toml`) - Configuration du projet
- **Docker** (`Dockerfile`, `smithery.yaml`) - Déploiement

## 📊 Données extraites

Le système peut extraire une grande variété de données LinkedIn :

### Informations de base
- Titre du poste
- ID unique LinkedIn
- État de publication
- Date de publication formatée
- URN d'entité et tracking URN

### Informations d'entreprise enrichies
- Nom complet de l'entreprise
- **Logos haute résolution** (3 tailles : 100x100, 200x200, 400x400px)
- Page LinkedIn officielle
- URN d'entreprise
- Nom universel de l'entreprise

### Détails du poste complets
- **Description complète** avec formatage LinkedIn préservé
- **Attributs de formatage** (gras, italique, listes, paragraphes)
- Localisation précise et formatée
- **Types de travail décodés** (Sur site/Hybride/Distanciel)
- Télétravail autorisé (booléen)
- **Méthodes de candidature** avec URLs directes
- **Liens de candidature** (Easy Apply, Company Apply, Complex Apply)

### Métadonnées avancées
- **Timestamp d'extraction** pour traçabilité
- **Données de recherche brutes** pour analyse
- **Champs additionnels** non traités
- **Structure de formatage** détaillée

## 🛠️ Technologies utilisées

- **Python 3.12+**
- **linkedin-api** - API non-officielle LinkedIn
- **FastMCP** - Framework MCP
- **python-dotenv** - Gestion variables d'environnement
- **Docker** - Containerisation
- **JSON** - Format de données

## 📈 Cas d'usage

### Cas d'usage traditionnels
1. **Recherche d'emploi automatisée**
2. **Veille du marché de l'emploi**
3. **Analyse de la concurrence**
4. **Extraction de données en masse**
5. **Intégration avec d'autres systèmes**

### Nouveaux cas d'usage (2025)
6. **Génération de portails HTML** pour présentation des offres
7. **Création de rapports visuels** avec logos et formatage
8. **Analyse comparative** avec données enrichies
9. **Tableaux de bord interactifs** avec navigation
10. **Export multi-format** (JSON, Markdown, HTML)

## 🔗 Liens rapides

- [Guide d'installation](setup/installation.md)
- [Architecture du projet](architecture.md)
- [API LinkedIn](api/linkedin_api.md)
- [**Opérateurs de recherche LinkedIn**](linkedin_search_operators.md) ⭐
- [Exemples d'utilisation](examples/basic_usage.md)
- [Script d'extraction complète](scripts/complete_extraction.md)

## 🆕 Nouveautés - Août 2025

### 📊 Fichiers générés
- **`complete_extraction_20250823_025546.json`** - Extraction complète 20 emplois (143KB)
- **`index.html`** - Page lobby interactive avec navigation
- **`job_*.html`** - Pages individuelles avec design moderne
- **`job_*.md`** - Fichiers markdown lisibles

### 🌐 Interface Web
- **Lobby interactif** : Naviguez entre les offres avec une interface moderne
- **Pages d'emploi enrichies** : Design responsive avec logos d'entreprises
- **CSS avancé** : Animations, dégradés, effets hover, backdrop filters
- **Mobile-friendly** : Interface adaptive pour tous les écrans

### 📈 Données enrichies
- **Logos en 3 tailles** : 100x100, 200x200, 400x400px
- **Descriptions formatées** : Conservation du formatage LinkedIn original
- **Liens de candidature** : URLs directes vers les plateformes de recrutement
- **Types de travail** : Décodage des URNs en texte lisible

### 🔍 Optimisation de recherche avancée
- **Opérateurs LinkedIn officiels** : Documentation complète des Boolean operators
- **Recherche avec exclusions** : `SEO NOT (casino OR gaming OR stage)`
- **Phrases exactes** : `"SEO Specialist"` pour des résultats précis
- **Recherche multilingue** : `(SEO OR référenceur) AND paris`
- **Tests comparatifs** : Analyse d'efficacité des différents opérateurs

## 📝 Notes

- ⚠️ **Respecter les conditions d'utilisation LinkedIn**
- 🔒 **Ne jamais commiter les identifiants** (fichier `.env`)
- ⏱️ **Respecter les limites de taux** de l'API
- 🛡️ **Utilisation responsable** des données

---

*Documentation générée automatiquement - Version 1.0 - Août 2025*