# ⚙️ Guide d'installation - LinkedIn Job Search MCP

## 🎯 Prérequis système

### Environnement requis
- **Python** 3.12 ou supérieur
- **Git** pour le clonage du repository
- **Compte LinkedIn** actif et valide
- **Connexion Internet** stable

### Systèmes supportés
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10/11 avec WSL recommandé)
- ✅ **Docker** (toutes plateformes)

## 📥 Installation du projet

### 1. Clonage du repository

```bash
# Cloner depuis GitHub
git clone https://github.com/Xelov4/job-search.git
cd job-search

# Vérifier le contenu
ls -la
```

### 2. Création de l'environnement virtuel

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement (Linux/macOS)
source venv/bin/activate

# Activer l'environnement (Windows)
venv\\Scripts\\activate

# Vérifier l'activation
which python  # Doit pointer vers venv/bin/python
```

### 3. Installation des dépendances

```bash
# Mise à jour pip
pip install --upgrade pip

# Installation depuis pyproject.toml
pip install -e .

# Ou installation manuelle des packages
pip install linkedin-api>=2.3.1 python-dotenv>=1.1.1 fastmcp
```

### 4. Vérification de l'installation

```bash
# Tester l'importation
python -c "from linkedin_api import Linkedin; print('✅ LinkedIn API OK')"
python -c "from dotenv import load_dotenv; print('✅ Dotenv OK')"
python -c "import fastmcp; print('✅ FastMCP OK')"
```

## 🔐 Configuration des identifiants

### 1. Création du fichier .env

```bash
# Créer le fichier de configuration
touch .env

# Éditer avec votre éditeur préféré
nano .env
# ou
vim .env
```

### 2. Contenu du fichier .env

```env
# Identifiants LinkedIn
LINKEDIN_EMAIL=votre_email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe_linkedin

# Configuration optionnelle
DEBUG=false
MAX_RETRIES=3
TIMEOUT=30
```

### 3. Sécurisation du fichier

```bash
# Permissions restrictives
chmod 600 .env

# Vérifier que .env est dans .gitignore
echo ".env" >> .gitignore
```

⚠️ **IMPORTANT** : Ne jamais commiter le fichier `.env` dans Git !

## 🧪 Test de base

### 1. Test rapide d'authentification

```bash
# Test simple
python -c "
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os

load_dotenv()
try:
    linkedin = Linkedin(os.getenv('LINKEDIN_EMAIL'), os.getenv('LINKEDIN_PASSWORD'))
    print('✅ Authentification LinkedIn réussie')
except Exception as e:
    print(f'❌ Erreur d\'authentification: {e}')
"
```

### 2. Test des scripts principaux

```bash
# Test du script de recherche propre
python final_search_clean.py

# Test de l'extraction complète (optionnel)
python complete_extraction.py
```

### 3. Sortie attendue
```
🔍 Recherche d'emplois SEO à Paris, France...
======================================================================
✅ 10 emplois trouvés !

📋 **Emploi 1**
   Titre: [Titre du poste]
   Entreprise: [Nom entreprise]
   ...
```

## 🐳 Installation Docker (optionnel)

### 1. Construction de l'image

```bash
# Construire l'image Docker
docker build -t linkedin-mcp .

# Vérifier l'image
docker images | grep linkedin-mcp
```

### 2. Exécution du container

```bash
# Exécuter avec les variables d'environnement
docker run --env-file .env linkedin-mcp

# Ou avec montage de volume
docker run -v $(pwd):/app --env-file .env linkedin-mcp
```

### 3. Docker Compose (si disponible)

```yaml
# docker-compose.yml
version: '3.8'
services:
  linkedin-mcp:
    build: .
    env_file:
      - .env
    volumes:
      - ./data:/app/data
```

```bash
# Lancement
docker-compose up
```

## ⚙️ Configuration MCP Server

### 1. Configuration globale MCP

Créer le fichier de configuration MCP :

```bash
# Créer le répertoire de configuration
mkdir -p ~/.config/mcp/servers

# Créer le fichier de configuration
cat > ~/.config/mcp/servers/linkedin.json << 'EOF'
{
    "mcpServers": {
        "linkedin": {
            "command": "/path/to/linkedin-mcp/venv/bin/python",
            "args": ["/path/to/linkedin-mcp/src/linkedin.py"],
            "env": {
                "PYTHONPATH": "/path/to/linkedin-mcp/src"
            }
        }
    }
}
EOF
```

### 2. Adaptation des chemins

```bash
# Remplacer par vos chemins absolus
CURRENT_DIR=$(pwd)
sed -i "s|/path/to/linkedin-mcp|$CURRENT_DIR|g" ~/.config/mcp/servers/linkedin.json
```

### 3. Test du serveur MCP

```bash
# Test de démarrage du serveur
mcp run linkedin

# Ou test manuel
python src/linkedin.py
```

## 📁 Structure après installation

```
linkedin-mcp/
├── venv/                   # Environnement virtuel ✅
├── .env                    # Configuration sécurisée ✅
├── src/
│   └── linkedin.py         # Serveur MCP principal
├── final_search_clean.py   # Script de recherche optimisé
├── complete_extraction.py  # Script d'extraction complète
├── explore_all_data.py     # Script d'exploration
├── pyproject.toml         # Configuration Python
├── Dockerfile             # Configuration Docker
├── smithery.yaml          # Configuration Smithery
├── docs/                  # Documentation complète
└── README.md              # Instructions de base
```

## 🔧 Dépannage de l'installation

### Problèmes courants

#### 1. Erreur "ModuleNotFoundError"
```bash
# Vérifier l'environnement virtuel
which python
which pip

# Réinstaller les dépendances
pip install -e .
```

#### 2. Erreur d'authentification LinkedIn
```bash
# Vérifier les identifiants
cat .env

# Tester manuellement
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'Email: {os.getenv(\"LINKEDIN_EMAIL\")}')
print(f'Password: {\"*\" * len(os.getenv(\"LINKEDIN_PASSWORD\", \"\"))}')
"
```

#### 3. Permissions refusées
```bash
# Corriger les permissions
chmod 755 .
chmod 600 .env
chmod +x *.py
```

#### 4. Python version incompatible
```bash
# Vérifier la version Python
python --version
python3 --version

# Utiliser Python 3.12+
python3.12 -m venv venv
```

### Logs de debug

#### Activation du debug
```bash
# Mode debug dans .env
echo "DEBUG=true" >> .env

# Ou temporairement
DEBUG=true python final_search_clean.py
```

#### Vérification des logs
```bash
# Logs Python
python -v final_search_clean.py

# Logs réseau (si nécessaire)
export PYTHONPATH=. && python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# ... votre code
"
```

## 🚀 Post-installation

### 1. Premier test complet

```bash
# Test d'une recherche complète
python final_search_clean.py

# Vérifier la génération des fichiers
ls -la *.json
```

### 2. Configuration de production

```bash
# Script de lancement automatique
cat > run_search.sh << 'EOF'
#!/bin/bash
cd /path/to/linkedin-mcp
source venv/bin/activate
python final_search_clean.py "$@"
EOF

chmod +x run_search.sh
```

### 3. Automatisation (optionnel)

```bash
# Cron job quotidien
crontab -e

# Ajouter :
# 0 9 * * * /path/to/linkedin-mcp/run_search.sh > /tmp/linkedin_search.log 2>&1
```

### 4. Mise à jour

```bash
# Mise à jour du code
git pull origin main

# Mise à jour des dépendances
source venv/bin/activate
pip install -e . --upgrade
```

## ✅ Checklist finale

- [ ] Python 3.12+ installé
- [ ] Repository cloné
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées sans erreur
- [ ] Fichier `.env` créé avec identifiants LinkedIn
- [ ] Test d'authentification réussi
- [ ] Script de base exécuté avec succès
- [ ] Configuration MCP (si applicable)
- [ ] Documentation lue

**🎉 Installation terminée ! Votre environnement LinkedIn Job Search MCP est prêt.**

---

*Guide d'installation - Version 1.0 - Août 2025*