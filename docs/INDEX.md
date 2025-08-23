# 📚 Index complet de la documentation - LinkedIn Job Search MCP

## 🎯 Navigation rapide

| Section | Description | Lien |
|---------|-------------|------|
| 🏠 **Accueil** | Vue d'ensemble du projet | [README.md](README.md) |
| 🏗️ **Architecture** | Structure technique du projet | [architecture.md](architecture.md) |
| ⚙️ **Installation** | Guide d'installation complet | [setup/installation.md](setup/installation.md) |
| 🚀 **Utilisation** | Exemples et cas d'usage | [examples/basic_usage.md](examples/basic_usage.md) |
| 📊 **Extraction complète** | Script d'extraction avancé | [scripts/complete_extraction.md](scripts/complete_extraction.md) |
| 🧹 **Recherche optimisée** | Script de production | [scripts/final_search_clean.md](scripts/final_search_clean.md) |
| 🔌 **API LinkedIn** | Documentation technique API | [api/linkedin_api.md](api/linkedin_api.md) |
| 🔍 **Opérateurs LinkedIn** | Guide des opérateurs de recherche officiels | [linkedin_search_operators.md](linkedin_search_operators.md) |
| 🌐 **Portail HTML** | Interface web moderne | [portal_html.md](portal_html.md) |

---

## 📁 Structure complète de la documentation

```
docs/
├── 📋 INDEX.md                    # Ce fichier - Index général
├── 📖 README.md                   # Vue d'ensemble du projet
├── 🏗️ architecture.md             # Architecture technique
├── 🌐 portal_html.md              # Documentation portail HTML
├── 🔍 linkedin_search_operators.md # Opérateurs de recherche officiels
│
├── 📚 scripts/                    # Documentation des scripts
│   ├── complete_extraction.md     # Script d'extraction exhaustive
│   ├── final_search_clean.md      # Script de recherche optimisé
│   ├── final_search.md           # Script de recherche avec debug
│   └── explore_all_data.md       # Script d'exploration des données
│
├── 🔌 api/                       # Documentation API
│   ├── linkedin_api.md           # API LinkedIn sous-jacente
│   └── mcp_server.md             # Serveur MCP (architecture)
│
├── ⚙️ setup/                     # Guides d'installation
│   ├── installation.md           # Installation complète
│   └── configuration.md          # Configuration avancée
│
└── 🚀 examples/                  # Exemples d'utilisation
    ├── basic_usage.md            # Utilisation basique
    ├── advanced_usage.md         # Utilisation avancée
    └── data_analysis.md          # Analyse des données
```

---

## 🎯 Guides par objectif

### 👋 Débutant - Premier usage
1. [📖 Vue d'ensemble](README.md) - Comprendre le projet
2. [⚙️ Installation](setup/installation.md) - Installer le système
3. [🚀 Utilisation basique](examples/basic_usage.md) - Premiers tests
4. [🧹 Script optimisé](scripts/final_search_clean.md) - Usage quotidien

### 🔧 Développeur - Compréhension technique
1. [🏗️ Architecture](architecture.md) - Structure du projet
2. [🔌 API LinkedIn](api/linkedin_api.md) - Fonctionnement de l'API
3. [📊 Extraction complète](scripts/complete_extraction.md) - Script avancé
4. [🚀 Exemples avancés](examples/basic_usage.md) - Intégrations

### 📊 Analyste - Extraction de données
1. [📊 Script d'extraction complète](scripts/complete_extraction.md) - Données exhaustives
2. [🚀 Cas d'usage analytiques](examples/basic_usage.md) - Analyses avancées
3. [🏗️ Structure des données](architecture.md) - Format JSON
4. [🔌 API techniques](api/linkedin_api.md) - Limitations et optimisations

### 🏢 Production - Déploiement
1. [⚙️ Installation](setup/installation.md) - Environnement de production
2. [🧹 Script optimisé](scripts/final_search_clean.md) - Script de production
3. [🚀 Automatisation](examples/basic_usage.md) - Cron, Docker, CI/CD
4. [🏗️ Architecture](architecture.md) - Considérations de déploiement

---

## 🔍 Index des scripts

### Scripts principaux
| Script | Niveau | Usage | Documentation |
|--------|--------|-------|---------------|
| `final_search_clean.py` | ⭐⭐ Facile | Production quotidienne | [📋 Documentation](scripts/final_search_clean.md) |
| `complete_extraction.py` | ⭐⭐⭐ Avancé | Analyse exhaustive | [📊 Documentation](scripts/complete_extraction.md) |
| `final_search.py` | ⭐⭐ Moyen | Debug et développement | [🔧 Documentation](scripts/final_search.md) |
| `explore_all_data.py` | ⭐⭐⭐ Expert | Exploration structure | [🔍 Documentation](scripts/explore_all_data.md) |

### Scripts MCP
| Composant | Fonction | Documentation |
|-----------|----------|---------------|
| `src/linkedin.py` | Serveur MCP principal | [🔌 Architecture MCP](architecture.md#serveur-mcp) |
| Configuration MCP | Setup serveur MCP | [⚙️ Installation MCP](setup/installation.md#configuration-mcp-server) |

---

## 🔧 Index des fonctionnalités

### Extraction de données
| Fonctionnalité | Script | Documentation |
|----------------|--------|---------------|
| **Recherche basique** | `final_search_clean.py` | [🧹 Recherche optimisée](scripts/final_search_clean.md) |
| **Extraction complète** | `complete_extraction.py` | [📊 Extraction complète](scripts/complete_extraction.md) |
| **Exploration structure** | `explore_all_data.py` | [🔍 Exploration](scripts/explore_all_data.md) |
| **Serveur MCP** | `src/linkedin.py` | [🔌 API MCP](api/linkedin_api.md) |

### Types de données extraites
| Type de données | Description | Localisation documentation |
|-----------------|-------------|---------------------------|
| **Informations de base** | Titre, ID, état | [🏗️ Structure données](architecture.md#structure-des-données) |
| **Entreprise** | Nom, logo, URL | [📊 Extraction](scripts/complete_extraction.md#informations-dentreprise) |
| **Description** | Texte + formatage | [📊 Description](scripts/complete_extraction.md#description-complète) |
| **Lieu de travail** | Types, télétravail | [🔌 Types workplace](api/linkedin_api.md#types-et-urns-linkedin) |
| **Candidature** | URLs, méthodes | [📊 Apply methods](scripts/complete_extraction.md#méthodes-de-candidature) |

---

## 📊 Index des formats de données

### Formats de sortie
| Format | Usage | Exemple | Documentation |
|--------|-------|---------|---------------|
| **Console** | Debug, monitoring | Affichage temps réel | [🧹 Sortie console](scripts/final_search_clean.md#format-de-sortie) |
| **JSON basique** | Intégration simple | Données de recherche | [🧹 JSON basique](scripts/final_search_clean.md#fichier-json-sauvegardé) |
| **JSON complet** | Analyse approfondie | Toutes les données | [📊 JSON complet](scripts/complete_extraction.md#structure-des-données-de-sortie) |
| **Structuré MCP** | Protocole MCP | Format standardisé | [🔌 Format MCP](api/linkedin_api.md#structure-de-réponse) |

### Structures de données
| Structure | Contenu | Taille typique | Documentation |
|-----------|---------|----------------|---------------|
| **search_results** | Données de base | ~300 bytes/emploi | [🔌 Search response](api/linkedin_api.md#structure-de-réponse) |
| **job_details** | Données complètes | ~6 Ko/emploi | [🔌 Job details](api/linkedin_api.md#structure-de-réponse-complète) |
| **complete_extraction** | Tout + métadonnées | ~7 Ko/emploi | [📊 Extraction format](scripts/complete_extraction.md#format-json-complet) |

---

## 🚀 Index des cas d'usage

### Par secteur d'activité
| Secteur | Usage typique | Script recommandé | Exemple |
|---------|---------------|-------------------|---------|
| **Recrutement** | Veille marché emploi | `complete_extraction.py` | [🚀 Veille concurrentielle](examples/basic_usage.md#veille-concurrentielle) |
| **Marketing** | Analyse concurrence | `final_search_clean.py` | [🚀 Analyse marché](examples/basic_usage.md#analyse-de-marché-par-région) |
| **RH** | Sourcing candidats | `complete_extraction.py` | [🚀 Monitoring](examples/basic_usage.md#monitoring-automatique) |
| **Data Science** | Analyse de données | `complete_extraction.py` | [🚀 Dashboard](examples/basic_usage.md#dashboard-de-visualisation) |

### Par fréquence d'usage
| Fréquence | Usage | Script | Automation |
|-----------|-------|--------|-----------|
| **Ponctuel** | Test, exploration | `final_search_clean.py` | Manuel |
| **Quotidien** | Monitoring emplois | `final_search_clean.py` | Cron job |
| **Hebdomadaire** | Analyse approfondie | `complete_extraction.py` | Cron job |
| **Temps réel** | API continue | `src/linkedin.py` | Serveur MCP |

---

## 📖 Guides de lecture recommandés

### 🎯 Parcours "Démarrage rapide" (15 min)
1. [📖 README.md](README.md) - Vue d'ensemble (3 min)
2. [⚙️ Installation](setup/installation.md) - Setup de base (8 min)
3. [🧹 Premier test](scripts/final_search_clean.md#utilisation) - Exécution (4 min)

### 🎯 Parcours "Utilisation avancée" (45 min)
1. [🏗️ Architecture](architecture.md) - Compréhension technique (15 min)
2. [📊 Extraction complète](scripts/complete_extraction.md) - Script avancé (20 min)
3. [🚀 Cas d'usage](examples/basic_usage.md) - Intégrations (10 min)

### 🎯 Parcours "Développement" (90 min)
1. [🏗️ Architecture complète](architecture.md) - Structure détaillée (30 min)
2. [🔌 API LinkedIn](api/linkedin_api.md) - Fonctionnement API (25 min)
3. [📊 Scripts avancés](scripts/complete_extraction.md) - Code détaillé (20 min)
4. [🚀 Intégrations](examples/basic_usage.md) - Développements personnalisés (15 min)

---

## 🔗 Liens externes et ressources

### Dépendances principales
- [linkedin-api](https://github.com/tomquirk/linkedin-api) - API Python LinkedIn
- [FastMCP](https://fastmcp.com/) - Framework MCP
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Variables d'environnement

### Protocoles et standards
- [Model Context Protocol](https://modelcontextprotocol.io/) - Spécification MCP
- [LinkedIn Developer](https://developer.linkedin.com/) - API officielle (référence)

### Outils complémentaires
- [Docker](https://docs.docker.com/) - Containerisation
- [GitHub Actions](https://docs.github.com/en/actions) - CI/CD
- [Streamlit](https://docs.streamlit.io/) - Dashboard web

---

## 📝 Historique de la documentation

| Version | Date | Modifications | Auteur |
|---------|------|---------------|--------|
| **1.1** | Août 2025 | Ajout portail HTML + extraction enrichie | Claude Code |
| **1.0** | Août 2025 | Documentation complète initiale | Claude Code |
| **0.9** | Août 2025 | Scripts et architecture de base | Claude Code |
| **0.8** | Août 2025 | Correction bugs extraction | Claude Code |

---

## 🆘 Support et aide

### En cas de problème
1. **Consulter** la section [🔧 Dépannage](setup/installation.md#dépannage-de-linstallation)
2. **Vérifier** les [⚠️ Limitations](api/linkedin_api.md#limitations-et-contraintes)  
3. **Tester** avec les [🧪 Scripts de test](setup/installation.md#test-de-base)
4. **Consulter** les logs en mode debug

### Documentation manquante
Si vous ne trouvez pas d'information dans cette documentation :
- Consulter le [📖 README principal](../README.md)
- Regarder le [📋 Manuel original](../manual.md)
- Examiner le code source des scripts

---

*Index de documentation - Version 1.0 - Août 2025*
*Généré automatiquement avec Claude Code*