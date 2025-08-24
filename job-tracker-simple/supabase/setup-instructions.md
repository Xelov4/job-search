# 🚀 Instructions Setup Supabase

## Étape 1: Créer le Projet Supabase

1. **Aller sur [supabase.com](https://supabase.com)**
2. **Créer un compte** ou se connecter
3. **"New Project"**
   - **Organization**: Créer ou utiliser existante
   - **Project Name**: `job-tracker-simple`
   - **Database Password**: Choisir un mot de passe fort (sauvegarder!)
   - **Region**: Europe (West) pour minimiser latence depuis France
   - **Pricing Plan**: Free tier (largement suffisant pour usage personnel)

## Étape 2: Exécuter le Schéma

1. **Aller dans l'onglet "SQL Editor"** dans le dashboard Supabase
2. **Copier-coller le contenu complet** du fichier `schema.sql`
3. **Cliquer "RUN"** pour exécuter
4. **Vérifier** que toutes les tables sont créées sans erreur

## Étape 3: Récupérer les Clés d'API

1. **Aller dans "Settings" > "API"**
2. **Noter ces informations** :
   - **URL**: `https://[your-project].supabase.co`
   - **API Key (public/anon)**: `eyJ...` (commence par eyJ)
   - **Service Role Key**: `eyJ...` (pour opérations admin côté serveur)

## Étape 4: Configuration Variables d'Environnement

Créer le fichier `.env` dans le répertoire `python/`:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# LinkedIn Configuration (réutilise celle existante)
LINKEDIN_EMAIL=ton.email@gmail.com
LINKEDIN_PASSWORD=ton_mot_de_passe
```

## Étape 5: Vérification Installation

Une fois le schéma exécuté, tu devrais voir dans l'onglet "Table Editor":

- ✅ **job_offers** (0 rows) - Table principale
- ✅ **job_actions** (0 rows) - Historique actions
- ✅ **app_settings** (6 rows) - Configuration
- ✅ **v_jobs_dashboard** (view) - Vue dashboard
- ✅ **v_stats_summary** (view) - Vue statistiques

## Étape 6: Test Rapide

Dans le SQL Editor, tester cette requête:

```sql
-- Vérifier que tout fonctionne
SELECT * FROM app_settings;

-- Devrais voir 6 lignes de configuration initiale
```

## 🔒 Sécurité

- **API Key publique**: OK pour le front-end (Next.js)
- **Service Role Key**: UNIQUEMENT côté serveur Python (plus de permissions)
- **Pas de RLS** pour l'instant (utilisateur unique, simplifié)
- **Fichier .env**: À ne JAMAIS committer dans Git

## 📊 Vérifications Post-Setup

- [ ] Projet Supabase créé
- [ ] Schéma SQL exécuté sans erreur
- [ ] 3 tables + 2 vues créées
- [ ] 6 lignes dans app_settings
- [ ] Variables d'environnement configurées
- [ ] Test requête SELECT réussie

## 🆘 Dépannage

**Erreur "relation already exists"**: Normal si tu exécutes le schéma plusieurs fois. Supprime les tables manuellement ou utilise `DROP TABLE IF EXISTS` avant de relancer.

**Erreur de permissions**: Utilise la Service Role Key pour les opérations Python côté serveur.

**Pas d'accès aux tables**: Vérifie que l'URL et les clés sont correctes dans le .env.

---

⚡ **Une fois terminé, passer à l'étape suivante: Développement client Python**