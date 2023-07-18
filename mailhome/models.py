from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.

class MailSend(models.Model):
    content = FroalaField()
