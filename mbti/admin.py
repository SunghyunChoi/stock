from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Question)
@admin.register(models.Choice)
@admin.register(models.Case)
@admin.register(models.Response)
@admin.register(models.Result)
class QuestionAdmin(admin.ModelAdmin):
    pass