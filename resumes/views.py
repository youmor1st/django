from pydantic import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

from logs.utils import log_action
from .parsers.matcher import match_resume_to_job
from .serializers import ResumeUploadSerializer, JobPostingSerializer
from .models import Resume, JobPosting

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, parse_resume_task=None, serializer=None, *args, **kwargs):
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            resume_file = request.FILES['file']
            resume = serializer.save(user=request.user)
            parse_resume_task.delay(resume.id)

            # Логирование
            log_action(
                user=request.user,
                action_type="upload_resume",
                description=f"User uploaded resume: {resume_file.name}"
            )

            return Response(ResumeUploadSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ResumeListView(generics.ListAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'recruiter' or user.is_staff:
            return Resume.objects.all().order_by('-uploaded_at')
        return Resume.objects.filter(user=user).order_by('-uploaded_at')

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='match-resume/(?P<resume_id>[^/.]+)')
    def match_resume(self, request, pk=None, resume_id=None):
        job = self.get_object()
        try:
            resume = Resume.objects.get(pk=resume_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        score, keywords = match_resume_to_job(resume.parsed_data.get("text", ""), job.description)
        return Response({
            "match_score": score,
            "common_keywords": keywords
        })