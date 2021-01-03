from django.db import models


class News(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    url = models.CharField(max_length=500)
    created_at = models.CharField(max_length=300)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject
