from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services.hubspot import create_contact, get_contact_by_email, update_contact, delete_contact, get_contact_by_id

def create_contact_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")

        try:
            contact = create_contact(email, first_name, last_name, phone)
            return JsonResponse({"success": True, "contact": contact})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return render(request, "contacts/create_contact.html")


def get_contact_view(request, email):
    try:
        contact = get_contact_by_email(email)
        return JsonResponse({"success": True, "contact": contact})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


def update_contact_view(request, contact_id):
#def update_contact_view(request):
    # contact_id = request.GET.get('contact_id')
    # if not contact_id:
    #     # Handle the missing contact_id case
    #     return JsonResponse({"error": "Contact ID is required"}, status=400)
    
    if request.method == 'POST':
        properties = {
            "firstname": request.POST.get("first_name"),
            "lastname": request.POST.get("last_name"),
            "phone": request.POST.get("phone"),
        }

        try:
            contact = update_contact(contact_id, properties)
            return JsonResponse({"success": True, "contact": contact})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    else: 
        contact_data = get_contact_by_id(contact_id)
        # print (contact_data)
        # Extract properties or set default to empty string if not present
        if contact_data:
            properties = contact_data.get("properties", {})
            context = {
                "contact_id": contact_id,
                "firstname": properties.get("firstname", ""),
                "lastname": properties.get("lastname", ""),
                "phone": properties.get("phone", ""),
            }
        else:
            context = {"contact_id": contact_id, "firstname": "", "lastname": "", "phone": ""}

        return render(request, "contacts/update_contact.html", context )


def delete_contact_view(request, contact_id):
    try:
        status_code = delete_contact(contact_id)
        return JsonResponse({"success": True, "status_code": status_code})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

