"""JNTUH Results API client."""

import requests
from typing import Dict
from ..config.settings import Settings


class JNTUHClient:
    """Client for fetching JNTUH academic results."""
    
    def __init__(self):
        self.api_url = Settings.JNTUH_API_URL
        self.timeout = Settings.API_TIMEOUT
    
    def fetch_results(self, hall_ticket: str) -> Dict:
        """
        Fetch academic results for a given hall ticket number.
        
        Args:
            hall_ticket: Student's hall ticket number
            
        Returns:
            Dictionary containing results or error information
        """
        try:
            url = f"{self.api_url}?rollNumber={hall_ticket}"
            response = requests.get(url, timeout=self.timeout, allow_redirects=True)
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("status") == "success" and 
                    data.get("message") == "Your roll number has been queued."):
                    return {
                        "queued": True,
                        "message": "Your roll number has been queued for processing. Please try again in a few seconds."
                    }
                return {"success": True, "data": data}
            else:
                return {"error": f"Unable to fetch results. Status: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
