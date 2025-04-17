from django.urls import path
from .views import ResumeUploadView, ResumeListView, JobPostingViewSet

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('my/', ResumeListView.as_view(), name='my-resumes'),
    path('jobs/', JobPostingViewSet.as_view(), name='my-jobs'),

]
