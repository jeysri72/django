from django import forms
from .models import ChatHistory

class ChatHistoryForm(forms.ModelForm):
    class Meta:
        model = ChatHistory
        fields = ['user_message']  # We only need to capture the user message
        widgets = {
            'user_message': forms.Textarea(attrs={'placeholder': 'Ask a question...'}),
        }
