from django import forms
from mainboard.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'content']


        labels = {
            'subject': '제목',
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
