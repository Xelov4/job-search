from linkedin_api import Linkedin
from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging

load_dotenv()

mcp = FastMCP("LinkedIn-MCP")
logger = logging.getLogger(__name__)

def get_creds():
    return Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), debug=True)

@mcp.tool()
def get_profile():
    """
    Retrieves the User Profile
    """
    linkedin = get_creds()
    profile = linkedin.get_profile()
    return profile

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieve LinkedIn feed posts.

    :return: List of feed post details
    """
    linkedin = get_creds()
    try:
        post_urns = linkedin.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"
    
    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn["author_name"]}: {urn["content"]}\n"

    return posts

@mcp.tool()
def search_jobs(keywords: str, location: str = None, limit: int = 10) -> str:
    """
    Search for jobs on LinkedIn with specified criteria.
    
    :param keywords: Job search keywords (e.g., "SEO", "developer")
    :param location: Job location (e.g., "Paris, France")
    :param limit: Maximum number of jobs to return
    :return: List of job search results
    """
    linkedin = get_creds()
    try:
        # Perform job search
        search_results = linkedin.search_jobs(
            keywords=keywords,
            location=location,
            limit=limit
        )
        
        if not search_results:
            return "Aucun emploi trouvé avec ces critères."
        
        # Format results
        jobs_info = f"🔍 Recherche d'emplois pour '{keywords}'"
        if location:
            jobs_info += f" à {location}"
        jobs_info += f"\n\n"
        
        for i, job in enumerate(search_results[:limit], 1):
            jobs_info += f"📋 **Emploi {i}**\n"
            jobs_info += f"   Titre: {job.get('title', 'N/A')}\n"
            jobs_info += f"   Entreprise: {job.get('company', 'N/A')}\n"
            jobs_info += f"   Localisation: {job.get('location', 'N/A')}\n"
            jobs_info += f"   Type: {job.get('job_type', 'N/A')}\n"
            jobs_info += f"   Expérience: {job.get('experience_level', 'N/A')}\n"
            jobs_info += f"   Date: {job.get('date_posted', 'N/A')}\n"
            jobs_info += f"   Lien: {job.get('job_url', 'N/A')}\n\n"
        
        return jobs_info
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return f"Erreur lors de la recherche d'emplois: {e}"

@mcp.tool()
def get_job_details(job_id: str) -> str:
    """
    Get detailed information about a specific job.
    
    :param job_id: LinkedIn job ID
    :return: Detailed job information
    """
    linkedin = get_creds()
    try:
        job_details = linkedin.get_job(job_id)
        return f"📋 **Détails de l'emploi**\n{job_details}"
    except Exception as e:
        logger.error(f"Error getting job details: {e}")
        return f"Erreur lors de la récupération des détails: {e}"

if __name__ == "__main__":
    mcp.run(transport='stdio')