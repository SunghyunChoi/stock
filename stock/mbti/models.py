from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length = 1000, null=True)
    image_url = models.URLField(max_length= 2000, null = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table='questions'