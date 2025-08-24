"""
Types de données pour le système Job Tracker
Structures communes pour normalisation multi-sources
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class JobOfferData:
    """Structure normalisée pour une offre d'emploi - compatible Supabase"""
    
    # Identification source
    source_platform: str        # 'linkedin', 'welcometothejungle', 'indeed', etc.
    source_id: str             # ID unique sur la plateforme source
    source_url: str            # URL complète vers l'offre
    
    # Informations emploi
    title: str                 # Titre du poste
    company_name: str          # Nom de l'entreprise
    company_url: Optional[str] = None  # URL de l'entreprise
    location: Optional[str] = None     # Localisation du poste
    description: Optional[str] = None  # Description complète
    
    # Modalités travail
    work_mode: Optional[str] = None    # 'remote', 'on-site', 'hybrid'
    job_type: Optional[str] = None     # 'full-time', 'part-time', 'contract'
    
    # Candidature
    application_url: Optional[str] = None  # URL candidature directe
    salary_info: Optional[str] = None      # Informations salaire
    
    # Dates (format ISO string)
    posted_at: Optional[str] = None        # Date publication
    discovered_at: Optional[str] = None    # Date découverte par système
    
    def __post_init__(self):
        """Post-traitement après initialisation"""
        # Valeurs par défaut
        if self.discovered_at is None:
            self.discovered_at = datetime.now().isoformat()
        
        # Nettoyage des chaînes
        if self.title:
            self.title = self.title.strip()
        if self.company_name:
            self.company_name = self.company_name.strip()
        if self.location:
            self.location = self.location.strip()
        
        # Validation work_mode
        valid_work_modes = ['remote', 'on-site', 'hybrid']
        if self.work_mode and self.work_mode not in valid_work_modes:
            self.work_mode = 'on-site'  # Par défaut
        
        # Validation job_type  
        valid_job_types = ['full-time', 'part-time', 'contract', 'internship', 'freelance']
        if self.job_type and self.job_type not in valid_job_types:
            self.job_type = 'full-time'  # Par défaut
    
    def to_dict(self) -> dict:
        """Convertir en dictionnaire pour Supabase"""
        return {
            'source_platform': self.source_platform,
            'source_id': self.source_id,
            'source_url': self.source_url,
            'title': self.title,
            'company_name': self.company_name,
            'company_url': self.company_url,
            'location': self.location,
            'description': self.description,
            'work_mode': self.work_mode,
            'job_type': self.job_type,
            'application_url': self.application_url,
            'salary_info': self.salary_info,
            'posted_at': self.posted_at,
            'discovered_at': self.discovered_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'JobOfferData':
        """Créer depuis un dictionnaire"""
        return cls(
            source_platform=data.get('source_platform', ''),
            source_id=data.get('source_id', ''),
            source_url=data.get('source_url', ''),
            title=data.get('title', ''),
            company_name=data.get('company_name', ''),
            company_url=data.get('company_url'),
            location=data.get('location'),
            description=data.get('description'),
            work_mode=data.get('work_mode'),
            job_type=data.get('job_type'),
            application_url=data.get('application_url'),
            salary_info=data.get('salary_info'),
            posted_at=data.get('posted_at'),
            discovered_at=data.get('discovered_at')
        )


# Types d'énums pour validation
WORK_MODES = ['remote', 'on-site', 'hybrid']
JOB_TYPES = ['full-time', 'part-time', 'contract', 'internship', 'freelance']
JOB_STATUSES = ['discovered', 'interested', 'applied', 'interview', 'rejected', 'accepted']
PLATFORMS = ['linkedin', 'welcometothejungle', 'indeed', 'glassdoor']


def validate_job_offer(job: JobOfferData) -> tuple[bool, list[str]]:
    """Valider une offre d'emploi"""
    errors = []
    
    # Champs requis
    if not job.source_platform:
        errors.append("source_platform requis")
    if not job.source_id:
        errors.append("source_id requis")
    if not job.title:
        errors.append("title requis")
    if not job.company_name:
        errors.append("company_name requis")
    
    # Validation énums
    if job.work_mode and job.work_mode not in WORK_MODES:
        errors.append(f"work_mode invalide: {job.work_mode}")
    if job.job_type and job.job_type not in JOB_TYPES:
        errors.append(f"job_type invalide: {job.job_type}")
    if job.source_platform and job.source_platform not in PLATFORMS:
        errors.append(f"source_platform non supportée: {job.source_platform}")
    
    # Validation URLs
    if job.source_url and not (job.source_url.startswith('http://') or job.source_url.startswith('https://')):
        errors.append("source_url doit être une URL valide")
    
    return len(errors) == 0, errors