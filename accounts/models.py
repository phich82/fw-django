from django.db import models
from datetime import datetime
from django.conf import settings

from app.repositories.Repository import Repository

class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', unique=True, max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(verbose_name="Created At", auto_now=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-updated_at'] # -: Descending

# class Csv(models.Model, Repository):
#     id = models.BigAutoField(primary_key=True, null=False)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
#     name = models.ImageField("Csv", upload_to="uploads/%Y/%m/%d/", null=True, blank=True)
#     icon = models.CharField("Icon", max_length=255, null=True, blank=True)
#     url = models.TextField("Url", blank=True, null=True)
#     created_at = models.DateTimeField("Created At", auto_now=True)
#     updated_at = models.DateTimeField("Updated At", auto_now=True, null=True)

#     def formated_created_at(self):
#         # return self.created_at.strftime('%d/%m/%Y')
#         return datetime.strftime(self.created_at, '%d/%m/%Y')

#     def formated_updated_at(self):
#         # return self.updated_at.strftime('%d/%m/%Y')
#         return datetime.strftime(self.updated_at, '%d/%m/%Y')

#     def __str__(self):
#         return str(self.name)

#     class Meta:
#         # Ascending
#         # ordering = ['updated_at']
#         # Descending
#         ordering = ['-updated_at']
