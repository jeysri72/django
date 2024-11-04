import requests
from django.conf import settings

#Ref: https://developers.hubspot.com/beta-docs/guides/api/crm/objects/contacts?uuid=1745ee94-820f-4590-9f97-4976d7418cb0

HUBSPOT_BASE_URL = "https://api.hubapi.com"

def get_headers():
    """Returns headers for HubSpot API requests."""
    return {
        "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

def create_contact(email, first_name, last_name, phone):
    """Creates a contact in HubSpot."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
    contact_data = {
        "properties": {
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
            "phone": phone
        }
    }
    
    response = requests.post(url, headers=get_headers(), json=contact_data)
    response.raise_for_status()  # Raises an error for response codes 4xx/5xx
    return response.json()

def get_contact_by_email(email):
    """Retrieves a contact by email from HubSpot."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search"
    data = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=get_headers(), json=data)
    response.raise_for_status()
    return response.json()


def get_contact_by_id(contact_id):
    """Retrieves a contact by email from HubSpot."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"

    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def update_contact(contact_id, properties):
    """Updates a contact in HubSpot."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
    contact_data = {"properties": properties}
    
    response = requests.patch(url, headers=get_headers(), json=contact_data)
    response.raise_for_status()
    return response.json()

def delete_contact(contact_id):
    """Deletes a contact from HubSpot."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
    
    response = requests.delete(url, headers=get_headers())
    response.raise_for_status()
    return response.status_code  # Should return 204 for successful deletion
