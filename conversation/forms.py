from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widegets = {
            'content': forms.Textarea(attrs={ 'class': 'w-full py-4 px-6 rounded-xl border', 'placeholder': 'Type your message here...', 'rows': 3 }),
        }