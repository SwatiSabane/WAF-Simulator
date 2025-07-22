from django.db import models

class WAFRule(models.Model):
    name = models.CharField(max_length=100)
    pattern = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
