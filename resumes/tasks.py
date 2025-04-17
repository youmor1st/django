from celery import shared_task
from .models import Resume
from .parsers import parser
from logs.utils import log_action

@shared_task
def parse_resume_task(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        file = resume.file.open()
        parsed = parser.parse_resume(file, resume.file.name)
        resume.parsed_data = parsed
        resume.save()

        log_action(
            user=resume.user,
            action_type="parsed_resume",
            description=f"Resume parsed asynchronously: {resume.file.name}"
        )
    except Exception as e:
        # Можно логировать ошибки отдельно
        print(f"Error parsing resume: {e}")
