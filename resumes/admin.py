from django.contrib import admin
from .models import Resume, JobPosting

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'uploaded_at']
    search_fields = ['user__username']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']
