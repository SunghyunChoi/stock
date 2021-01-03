from django.db import models


class News(models.Model):
    subject = models.TextField()
    content = models.TextField()
    created_date = models.TextField()
    keyword = models.TextField()
    url = models.TextField()


    def __str__(self):
        return self.subject
