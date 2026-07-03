from django.db import models

class NetworkDevice(models.Model):
    DEVICE_CHOICES = [
        ('Router', 'Core Router'),
        ('Switch', 'L2/L3 Switch'),
        ('Access Point', 'Wireless AP / Bridge'),
        ('Server', 'Bare Metal Server'),
        ('Firewall', 'Network Firewall'),
        ('Load Balancer', 'Load Balancer'),
        ('Other', 'Other Network Device'),
    ]

    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    device_type = models.CharField(max_length=50, choices=DEVICE_CHOICES, default='Switch')
    status = models.CharField(max_length=10, default='Unknown')
    latency_ms = models.FloatField(default=0.0)
    last_checked = models.DateTimeField(auto_now=True)
    
    # 📊 Telemetry Data Fields
    health_score = models.IntegerField(default=100, null=True, blank=True)  # Health score out of 100
    temperature_c = models.FloatField(default=40.0, null=True, blank=True)       
    update_required = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    def save(self, *args, **kwargs):
        """ Runs an immediate ping assessment when a new asset is added """
        if not self.pk:
            from .utils import ping_device
            resolved_status, calculated_latency = ping_device(self.ip_address)
            self.status = resolved_status
            self.latency_ms = calculated_latency
            
            if resolved_status == 'Online':
                pass
             
            else:
                 self.health_score = 0
                 self.temperature_c = 0.0
                 self.update_required = False
                
        super().save(*args, **kwargs)