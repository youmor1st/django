from rest_framework import serializers
from .models import Resume, JobPosting


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'parsed_data']
        read_only_fields = ['uploaded_at', 'parsed_data']


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'description', 'created_at']
