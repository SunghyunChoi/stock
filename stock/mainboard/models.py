from django.db import models

class Article(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
    # 글쓴이 추가 예정
    
    def __str__(self):
        return self.subject

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    # 코멘트 단 이 추가 예정

    def __str__(self):
        return self.content