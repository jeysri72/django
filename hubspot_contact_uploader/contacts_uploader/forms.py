
from django import forms

class ContactUploadForm(forms.Form):
    csv_file = forms.FileField()


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()