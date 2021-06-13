from django.db import models

from django.conf import settings

class MailReceiverModel(models.Model):
    name = models.CharField(max_length=255) # receiver name
    email = models.EmailField(max_length = 255) # receiver email id
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None) # reference to user

    class Meta:
        unique_together = ('email', 'user')
