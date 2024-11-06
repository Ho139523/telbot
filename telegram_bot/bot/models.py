from django.db import models

from django.db import models

class UserRequest(models.Model):
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    service_category = models.CharField(max_length=50)
    product_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_name} - {self.service_category}"