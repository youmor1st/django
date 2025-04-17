from .models import ActionLog

def log_action(user, action_type, description):
    ActionLog.objects.using('dblog').create(
        user=user,
        action_type=action_type,
        description=description
    )
