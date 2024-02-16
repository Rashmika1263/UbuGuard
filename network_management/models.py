# models.py

from django.db import models

class FirewallRule(models.Model):
    port = models.IntegerField()
    protocol = models.CharField(max_length=10, choices=[('tcp', 'TCP'), ('udp', 'UDP')])
    source_ip = models.GenericIPAddressField()
    action = models.CharField(max_length=5, choices=[('allow', 'Allow'), ('deny', 'Deny')])

    def __str__(self):
        return f"Rule {self.id}: {self.protocol} {self.port} {self.action}"
