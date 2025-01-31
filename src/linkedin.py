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

@mcp.tool
def get_profile():
    linkedin = get_creds()
    profile = linkedin.get_profile()
    return profile

if __name__ == "__main__":
    mcp.run()