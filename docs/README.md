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
- Date de publication

### Informations d'entreprise
- Nom complet de l'entreprise
- Logo (3 tailles disponibles)
- Page LinkedIn
- URN d'entreprise

### Détails du poste
- Description complète avec formatage
- Localisation précise
- Type de travail (Sur site/Hybride/Distanciel)
- Télétravail autorisé
- Méthodes de candidature

## 🛠️ Technologies utilisées

- **Python 3.12+**
- **linkedin-api** - API non-officielle LinkedIn
- **FastMCP** - Framework MCP
- **python-dotenv** - Gestion variables d'environnement
- **Docker** - Containerisation
- **JSON** - Format de données

## 📈 Cas d'usage

1. **Recherche d'emploi automatisée**
2. **Veille du marché de l'emploi**
3. **Analyse de la concurrence**
4. **Extraction de données en masse**
5. **Intégration avec d'autres systèmes**

## 🔗 Liens rapides

- [Guide d'installation](setup/installation.md)
- [Architecture du projet](architecture.md)
- [API LinkedIn](api/linkedin_api.md)
- [Exemples d'utilisation](examples/basic_usage.md)
- [Script d'extraction complète](scripts/complete_extraction.md)

## 📝 Notes

- ⚠️ **Respecter les conditions d'utilisation LinkedIn**
- 🔒 **Ne jamais commiter les identifiants** (fichier `.env`)
- ⏱️ **Respecter les limites de taux** de l'API
- 🛡️ **Utilisation responsable** des données

---

*Documentation générée automatiquement - Version 1.0 - Août 2025*