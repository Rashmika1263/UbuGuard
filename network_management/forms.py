# forms.py

from django import forms
from .models import FirewallRule

class FirewallRuleForm(forms.ModelForm):
    class Meta:
        model = FirewallRule
        fields = ['port', 'protocol', 'source_ip', 'action']