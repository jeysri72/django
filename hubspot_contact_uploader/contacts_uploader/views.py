
import csv
import json
from django.http import HttpResponse, JsonResponse
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactUploadForm, CSVUploadForm
from .services.hubspot import upload_hubspot_contacts





def upload_csv(request):
    data = []  # To store CSV rows

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Decode file if necessary (for UTF-8 or similar encodings)
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Skip the header if needed
            header = next(reader, None)
            for row in reader:
                 # Prepare contact data from CSV columns
                print (row)

                contact_data = {
                    "properties": {
                        "firstname": row[0],
                        "lastname": row[1],
                        "email": row[2],
                        "phone": row[3],
                    },
                    "id": row[2],
                    "idProperty": "email"
                }

                print (contact_data)
                data.append(contact_data)
                print(data)

                contacts =json.dumps({"inputs": data})
            try:
                        
                print (contacts)
                response = upload_hubspot_contacts(contacts)

                return JsonResponse({"success": True, "response": response})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e), "json": contacts}, status=400)
    