from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from .models import LogEntry

User = get_user_model()

class ActionLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.path == '/login/' and request.method == 'POST':
                self.log_action(request.user, 'LOGIN')
            elif request.path == '/logout/' and request.method == 'POST':
                self.log_action(request.user, 'LOGOUT')

    def log_action(self, user, action, details=''):
        LogEntry.objects.create(user=user, action=action, details=details)