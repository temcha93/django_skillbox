from django.contrib import admin

from app_employment import models


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title']


class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(models.Vacancy, VacancyAdmin)
admin.site.register(models.Resume, VacancyAdmin)