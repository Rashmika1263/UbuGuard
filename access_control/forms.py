# your_project/ssh_config/forms.py

from django import forms

class SSHSettingsForm(forms.Form):
    ssh_status = forms.ChoiceField(choices=[("enable", "Enable"), ("disable", "Disable")], required=False)
    password_authentication = forms.BooleanField(required=False)
    allow_users = forms.CharField(required=False)
    change_default_port = forms.IntegerField(required=False)
    permit_root_login = forms.BooleanField(required=False)
    use_dns = forms.BooleanField(required=False)
    permit_empty_passwords = forms.BooleanField(required=False)
    client_alive_interval = forms.IntegerField(required=False)
    client_alive_count_max = forms.IntegerField(required=False)
    login_grace_time = forms.IntegerField(required=False)
