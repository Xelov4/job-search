-- =====================================================
-- JOB TRACKER SIMPLE - SCHÉMA SUPABASE V1.0
-- Utilisateur unique, focus suivi candidatures
-- =====================================================

-- Table principale des offres d'emploi
CREATE TABLE job_offers (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  
  -- === IDENTIFICATION SOURCE (Anti-doublons) ===
  source_platform VARCHAR(50) NOT NULL, -- 'linkedin', 'indeed', etc.
  source_id VARCHAR(255) NOT NULL, -- ID original plateforme (jobPostingId LinkedIn)
  source_url TEXT, -- URL LinkedIn directe: https://linkedin.com/jobs/view/{id}
  
  -- === INFORMATIONS ESSENTIELLES ===
  title VARCHAR(500) NOT NULL,
  company_name VARCHAR(200),
  company_url TEXT, -- URL profil LinkedIn entreprise
  location VARCHAR(200), -- "Paris, Île-de-France, France"
  description TEXT, -- Description complète de l'offre
  
  -- === MÉTADONNÉES EMPLOI (du workflow Enhanced) ===
  work_mode VARCHAR(50), -- 'remote', 'hybrid', 'on-site' (workRemoteAllowed)
  job_type VARCHAR(50), -- 'full-time', 'part-time', 'contract', 'internship'
  application_url TEXT, -- URL candidature directe (applyMethod.companyApplyUrl)
  salary_info VARCHAR(200), -- Information salaire (texte libre)
  
  -- === SUIVI CANDIDATURES PERSONNEL ===
  status VARCHAR(50) DEFAULT 'discovered', 
  -- Workflow: 'discovered' → 'interested' → 'applied' → 'interview' → 'rejected'/'accepted'/'archived'
  priority INTEGER DEFAULT 0, -- 0-5 étoiles pour priorité personnelle
  notes TEXT, -- Notes personnelles libres
  
  -- === DATES IMPORTANTES ===
  posted_at TIMESTAMP, -- Date publication originale (listedAt LinkedIn)
  discovered_at TIMESTAMP DEFAULT NOW(), -- Première fois vu dans le système
  applied_at TIMESTAMP, -- Date candidature envoyée (auto-rempli si status='applied')
  last_contact TIMESTAMP, -- Dernier contact/nouvelle de l'entreprise
  interview_date TIMESTAMP, -- Date entretien programmé
  
  -- === TIMESTAMPS SYSTÈME ===
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- === CONTRAINTES ===
  UNIQUE(source_platform, source_id) -- Anti-doublons: une offre par source/id
);

-- Fonction pour auto-update du timestamp updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_job_offers_updated_at 
    BEFORE UPDATE ON job_offers 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- === HISTORIQUE DES ACTIONS (optionnel mais utile pour debug) ===
CREATE TABLE job_actions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  job_offer_id UUID REFERENCES job_offers(id) ON DELETE CASCADE,
  
  action_type VARCHAR(50) NOT NULL, -- 'status_change', 'note_added', 'priority_change'
  old_value TEXT, -- Ancienne valeur (pour status_change par exemple)
  new_value TEXT, -- Nouvelle valeur
  details TEXT, -- Détails supplémentaires si nécessaire
  
  created_at TIMESTAMP DEFAULT NOW()
);

-- === CONFIGURATION APPLICATION ===
CREATE TABLE app_settings (
  key VARCHAR(100) PRIMARY KEY,
  value TEXT,
  description TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- === INDEX DE PERFORMANCE ===
-- Index pour les vues principales de l'interface
CREATE INDEX idx_job_offers_status_updated ON job_offers(status, updated_at DESC);
CREATE INDEX idx_job_offers_discovered ON job_offers(discovered_at DESC);
CREATE INDEX idx_job_offers_priority_discovered ON job_offers(priority DESC, discovered_at DESC);
CREATE INDEX idx_job_offers_source_lookup ON job_offers(source_platform, source_id);

-- Index pour recherche textuelle (titre et entreprise)
CREATE INDEX idx_job_offers_title_search ON job_offers USING gin(to_tsvector('english', title));
CREATE INDEX idx_job_offers_company_search ON job_offers USING gin(to_tsvector('english', company_name));

-- === DONNÉES INITIALES ===
INSERT INTO app_settings (key, value, description) VALUES 
('default_search_keywords', 'SEO', 'Mots-clés par défaut pour les recherches'),
('default_search_location', 'Paris, Île-de-France, France', 'Localisation par défaut'),
('last_linkedin_sync', NOW()::text, 'Dernière synchronisation LinkedIn'),
('app_version', '1.0', 'Version actuelle de l\'application'),
('total_jobs_processed', '0', 'Nombre total d\'emplois traités'),
('linkedin_api_rate_limit', '100', 'Limite de requêtes LinkedIn par session');

-- === VUES UTILES POUR L'INTERFACE ===

-- Vue des emplois avec statut enrichi
CREATE VIEW v_jobs_dashboard AS 
SELECT 
  id,
  title,
  company_name,
  location,
  work_mode,
  status,
  priority,
  source_url,
  application_url,
  discovered_at,
  applied_at,
  CASE 
    WHEN posted_at > NOW() - INTERVAL '1 day' THEN 'today'
    WHEN posted_at > NOW() - INTERVAL '3 days' THEN 'recent' 
    WHEN posted_at > NOW() - INTERVAL '7 days' THEN 'week'
    ELSE 'old'
  END as freshness,
  CASE 
    WHEN status = 'discovered' THEN 0
    WHEN status = 'interested' THEN 1  
    WHEN status = 'applied' THEN 2
    WHEN status = 'interview' THEN 3
    ELSE 4
  END as status_order
FROM job_offers
ORDER BY priority DESC, status_order ASC, discovered_at DESC;

-- Vue statistiques pour dashboard
CREATE VIEW v_stats_summary AS
SELECT 
  COUNT(*) as total_jobs,
  COUNT(CASE WHEN status = 'discovered' THEN 1 END) as discovered_count,
  COUNT(CASE WHEN status = 'interested' THEN 1 END) as interested_count,
  COUNT(CASE WHEN status = 'applied' THEN 1 END) as applied_count,
  COUNT(CASE WHEN status = 'interview' THEN 1 END) as interview_count,
  COUNT(CASE WHEN work_mode = 'remote' THEN 1 END) as remote_count,
  COUNT(CASE WHEN application_url IS NOT NULL THEN 1 END) as direct_apply_count,
  AVG(priority) as avg_priority
FROM job_offers;

-- === COMMENTAIRES ET DOCUMENTATION ===
COMMENT ON TABLE job_offers IS 'Table principale des offres d\'emploi avec suivi candidatures personnel';
COMMENT ON COLUMN job_offers.source_id IS 'ID unique de la source (jobPostingId pour LinkedIn)';
COMMENT ON COLUMN job_offers.source_url IS 'URL directe vers l\'offre (https://linkedin.com/jobs/view/{id})';
COMMENT ON COLUMN job_offers.application_url IS 'URL candidature directe entreprise (Enhanced: applyMethod.companyApplyUrl)';
COMMENT ON COLUMN job_offers.work_mode IS 'Mode de travail extrait du workflow Enhanced (workRemoteAllowed)';
COMMENT ON COLUMN job_offers.status IS 'Workflow personnel: discovered→interested→applied→interview→rejected/accepted';

-- === EXEMPLES DE REQUÊTES UTILES ===
/*
-- Tous les emplois intéressants avec télétravail
SELECT * FROM job_offers WHERE status = 'interested' AND work_mode = 'remote';

-- Candidatures en attente de réponse
SELECT * FROM job_offers WHERE status = 'applied' ORDER BY applied_at DESC;

-- Emplois haute priorité découverts récemment  
SELECT * FROM job_offers WHERE priority >= 4 AND discovered_at > NOW() - INTERVAL '3 days';

-- Statistiques rapides
SELECT status, COUNT(*) FROM job_offers GROUP BY status;
*/