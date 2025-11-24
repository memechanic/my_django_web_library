from functools import wraps
from .models import Log

def action_logger(action_text:str | None = None):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)

            username = request.session.get("admin_name") or "Пользователь"
            action = action_text or f"{view.__module__}.{view.__name__}"
            Log.objects.create(
                username=username,
                status=response.status_code,
                action=action,
                method=request.method,
                path=request.path,
            )
            return response
        return wrapper
    return decorator