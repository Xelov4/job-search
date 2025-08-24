#!/usr/bin/env python3
"""
Client Supabase Simple - Job Tracker
Gestion centralisée des interactions avec la base de données Supabase
"""

import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

@dataclass
class JobOfferData:
    """Structure de données normalisée pour un emploi"""
    source_platform: str
    source_id: str
    source_url: Optional[str]
    title: str
    company_name: Optional[str]
    company_url: Optional[str]
    location: Optional[str]
    description: Optional[str]
    work_mode: Optional[str]
    job_type: Optional[str]
    application_url: Optional[str]
    salary_info: Optional[str]
    posted_at: Optional[datetime]
    priority: int = 0
    notes: Optional[str] = None

class SimpleJobManager:
    """Client simplifié pour gérer les emplois dans Supabase"""
    
    def __init__(self):
        """Initialise la connexion Supabase"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")  # Service key pour plus de permissions
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Variables d'environnement manquantes: SUPABASE_URL et SUPABASE_SERVICE_KEY requis"
            )
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        print(f"✅ Connexion Supabase établie: {self.supabase_url}")
    
    def save_job(self, job_data: JobOfferData) -> Tuple[bool, str]:
        """
        Sauvegarde un emploi avec gestion intelligente des doublons
        
        Returns:
            Tuple[bool, str]: (succès, message)
        """
        try:
            # Préparation des données pour insertion
            job_dict = {
                "source_platform": job_data.source_platform,
                "source_id": job_data.source_id,
                "source_url": job_data.source_url,
                "title": job_data.title,
                "company_name": job_data.company_name,
                "company_url": job_data.company_url,
                "location": job_data.location,
                "description": job_data.description,
                "work_mode": job_data.work_mode,
                "job_type": job_data.job_type,
                "application_url": job_data.application_url,
                "salary_info": job_data.salary_info,
                "posted_at": job_data.posted_at.isoformat() if job_data.posted_at else None,
                "priority": job_data.priority,
                "notes": job_data.notes,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Vérifier si l'emploi existe déjà
            existing = self.client.table("job_offers").select("id, status, priority, notes").eq(
                "source_platform", job_data.source_platform
            ).eq("source_id", job_data.source_id).execute()
            
            if existing.data:
                # Emploi existant - mise à jour intelligente
                existing_job = existing.data[0]
                
                # Préserver les données utilisateur importantes
                job_dict.update({
                    "status": existing_job["status"],  # Garder le statut utilisateur
                    "priority": existing_job["priority"],  # Garder la priorité utilisateur
                    "notes": existing_job["notes"] or job_data.notes  # Garder les notes utilisateur
                })
                
                # Mise à jour
                result = self.client.table("job_offers").update(job_dict).eq(
                    "id", existing_job["id"]
                ).execute()
                
                return True, f"✅ Emploi mis à jour: {job_data.title}"
            
            else:
                # Nouvel emploi - insertion
                result = self.client.table("job_offers").insert(job_dict).execute()
                return True, f"🆕 Nouvel emploi ajouté: {job_data.title}"
                
        except Exception as e:
            error_msg = f"❌ Erreur sauvegarde {job_data.title}: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def save_jobs_batch(self, jobs_list: List[JobOfferData]) -> Dict[str, int]:
        """
        Sauvegarde une liste d'emplois avec statistiques
        
        Returns:
            Dict avec compteurs: new, updated, errors
        """
        stats = {"new": 0, "updated": 0, "errors": 0, "total": len(jobs_list)}
        
        print(f"🔄 Début synchronisation: {stats['total']} emplois à traiter")
        
        for i, job in enumerate(jobs_list, 1):
            print(f"   📋 [{i}/{stats['total']}] {job.title[:50]}...")
            
            success, message = self.save_job(job)
            
            if success:
                if "ajouté" in message:
                    stats["new"] += 1
                else:
                    stats["updated"] += 1
            else:
                stats["errors"] += 1
            
            # Affichage conditionnel pour éviter spam
            if i % 10 == 0 or not success:
                print(f"      {message}")
        
        # Mise à jour des statistiques globales
        self._update_app_stats(stats)
        
        print(f"\n📊 SYNCHRONISATION TERMINÉE:")
        print(f"   🆕 Nouveaux emplois: {stats['new']}")
        print(f"   🔄 Emplois mis à jour: {stats['updated']}")
        print(f"   ❌ Erreurs: {stats['errors']}")
        print(f"   ✅ Taux de succès: {((stats['new'] + stats['updated']) / stats['total'] * 100):.1f}%")
        
        return stats
    
    def update_job_status(self, job_id: str, status: str, notes: str = None) -> bool:
        """
        Met à jour le statut d'un emploi avec logging automatique
        
        Args:
            job_id: ID de l'emploi
            status: Nouveau statut
            notes: Notes optionnelles
        """
        try:
            # Récupérer l'état actuel
            current = self.client.table("job_offers").select("status, title").eq("id", job_id).execute()
            
            if not current.data:
                print(f"❌ Emploi non trouvé: {job_id}")
                return False
            
            old_status = current.data[0]["status"]
            job_title = current.data[0]["title"]
            
            # Préparer la mise à jour
            update_data = {
                "status": status,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Gestion automatique des timestamps selon le statut
            if status == "applied" and old_status != "applied":
                update_data["applied_at"] = datetime.now(timezone.utc).isoformat()
            
            if notes:
                update_data["notes"] = notes
            
            # Mise à jour
            result = self.client.table("job_offers").update(update_data).eq("id", job_id).execute()
            
            # Log de l'action dans l'historique
            self._log_action(job_id, "status_change", old_status, status)
            
            print(f"✅ Statut mis à jour: {job_title} ({old_status} → {status})")
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour statut: {e}")
            return False
    
    def get_jobs_by_status(self, status: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Récupère les emplois filtrés par statut
        
        Args:
            status: Statut à filtrer (None = tous)
            limit: Nombre maximum d'emplois
        """
        try:
            query = self.client.table("job_offers").select("*").order("discovered_at", desc=True).limit(limit)
            
            if status and status != "all":
                query = query.eq("status", status)
            
            result = query.execute()
            return result.data
            
        except Exception as e:
            print(f"❌ Erreur récupération emplois: {e}")
            return []
    
    def get_dashboard_stats(self) -> Dict:
        """Récupère les statistiques pour le dashboard"""
        try:
            result = self.client.table("v_stats_summary").select("*").execute()
            
            if result.data:
                return result.data[0]
            else:
                return {"total_jobs": 0}
                
        except Exception as e:
            print(f"❌ Erreur récupération stats: {e}")
            return {"total_jobs": 0}
    
    def search_jobs(self, query: str, limit: int = 50) -> List[Dict]:
        """Recherche textuelle dans les emplois"""
        try:
            # Recherche dans titre et nom entreprise
            result = self.client.table("job_offers").select("*").or_(
                f"title.ilike.%{query}%,company_name.ilike.%{query}%"
            ).order("discovered_at", desc=True).limit(limit).execute()
            
            return result.data
            
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return []
    
    def _log_action(self, job_id: str, action_type: str, old_value: str = None, new_value: str = None):
        """Log une action dans l'historique"""
        try:
            log_data = {
                "job_offer_id": job_id,
                "action_type": action_type,
                "old_value": old_value,
                "new_value": new_value
            }
            
            self.client.table("job_actions").insert(log_data).execute()
            
        except Exception as e:
            print(f"⚠️ Erreur logging action: {e}")
    
    def _update_app_stats(self, sync_stats: Dict):
        """Met à jour les statistiques globales de l'application"""
        try:
            # Mise à jour dernière sync
            self.client.table("app_settings").update({
                "value": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }).eq("key", "last_linkedin_sync").execute()
            
            # Mise à jour compteur total (approximatif)
            current_total = self.client.table("app_settings").select("value").eq("key", "total_jobs_processed").execute()
            
            if current_total.data:
                new_total = int(current_total.data[0]["value"]) + sync_stats.get("new", 0)
                self.client.table("app_settings").update({
                    "value": str(new_total),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }).eq("key", "total_jobs_processed").execute()
            
        except Exception as e:
            print(f"⚠️ Erreur mise à jour stats globales: {e}")
    
    def test_connection(self) -> bool:
        """Test la connexion Supabase"""
        try:
            result = self.client.table("app_settings").select("count", count="exact").execute()
            print(f"✅ Test connexion réussi: {result.count} paramètres trouvés")
            return True
        except Exception as e:
            print(f"❌ Test connexion échoué: {e}")
            return False

# Fonction utilitaire pour tests rapides
if __name__ == "__main__":
    # Test de base
    manager = SimpleJobManager()
    
    if manager.test_connection():
        print("🎉 Client Supabase opérationnel!")
        
        # Test insertion emploi fictif
        test_job = JobOfferData(
            source_platform="linkedin",
            source_id="test-123",
            source_url="https://linkedin.com/jobs/view/test-123",
            title="Test SEO Specialist",
            company_name="Test Company",
            location="Paris, France",
            description="Test description",
            work_mode="remote"
        )
        
        success, message = manager.save_job(test_job)
        print(message)
        
    else:
        print("❌ Problème configuration Supabase")