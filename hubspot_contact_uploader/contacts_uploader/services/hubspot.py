
import json
import logging
import requests
from django.conf import settings

#Ref: https://developers.hubspot.com/beta-docs/guides/api/crm/objects/contacts?uuid=1745ee94-820f-4590-9f97-4976d7418cb0

# Initialize logging
logger = logging.getLogger(__name__)

HUBSPOT_BASE_URL = "https://api.hubapi.com"

def get_headers():
    """Returns headers for HubSpot API requests."""
    return {
        "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }




def upload_hubspot_contacts(contacts):
    # url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/batch/upsert"
    url = "https://api.hubapi.com/crm/v3/objects/contacts/batch/upsert"
    print ("========================================================")
    print (contacts)
    response = requests.post(url, headers=get_headers(), json=json.loads(contacts))
    #response = requests.post(url, headers=get_headers() , json= contacts)
    response.raise_for_status()  # Raises an error for response codes 4xx/5xx
    return response.json()
                    