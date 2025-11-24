from functools import wraps

from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from .models import User

def admin_access():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)

            admin_id = request.session.get("admin_id") or None
            if admin_id:
                try:
                    admin = User.objects.get(pk=admin_id)
                except User.DoesNotExist:
                    return redirect('home') # HttpResponseNotAllowed('Нет доступа')
                else:
                    return response
            else:
                return redirect('home') # HttpResponseNotAllowed('Нет доступа')
            
        return wrapper
    return decorator
