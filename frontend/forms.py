from django import forms
from django_ace import AceWidget

class EditorForm(forms.Form):
    code = forms.CharField(widget=AceWidget(mode='python', theme='twilight'))