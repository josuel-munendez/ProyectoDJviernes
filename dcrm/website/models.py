from django.db import models
from core.models import BaseModel


class Record(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_contact_info(self):
        return f"Email: {self.email}, Tel: {self.phone}"
