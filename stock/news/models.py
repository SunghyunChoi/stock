from django.db import models


class News(models.Model):
    subject = models.TextField()
    content = models.TextField()
<<<<<<< HEAD
    url = models.CharField(max_length=500)
    created_at = models.CharField(max_length=300)
    create_date = models.DateTimeField()
=======
    created_date = models.TextField()
    keyword = models.TextField()
    url = models.TextField()

>>>>>>> c70b55f00cef9ffac6668465829f86ac924ea5a8

    def __str__(self):
        return self.subject
