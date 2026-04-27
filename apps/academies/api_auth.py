from functools import wraps
from django.http import JsonResponse
from django.utils import timezone
from .models import APIKey


def require_api_key(view_func):
    """
    Decorator to require a valid API key for API endpoints.
    
    Usage:
        @require_api_key
        def my_api_view(request):
            return JsonResponse({'data': 'success'})
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Get API key from header
        api_key = request.headers.get('X-API-Key') or request.headers.get('x-api-key')
        
        # Also check query parameter
        if not api_key:
            api_key = request.GET.get('api_key')
        
        if not api_key:
            return JsonResponse({
                'error': 'API key required',
                'message': 'Please provide API key in X-API-Key header or api_key query parameter'
            }, status=401)
        
        # Validate the API key
        key_obj = APIKey.validate_key(api_key)
        
        if not key_obj:
            return JsonResponse({
                'error': 'Invalid API key',
                'message': 'The provided API key is invalid or inactive'
            }, status=403)
        
        # Update last used timestamp
        key_obj.last_used_at = timezone.now()
        key_obj.save(update_fields=['last_used_at'])
        
        # Store the API key object in request for use in view
        request.api_key = key_obj
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def get_api_key_from_request(request):
    """
    Extract API key from request headers or query parameters.
    Returns None if not found.
    """
    # Check header (case-insensitive)
    api_key = request.headers.get('X-API-Key') or request.headers.get('x-api-key')
    
    # Check query parameter
    if not api_key:
        api_key = request.GET.get('api_key')
    
    return api_key


class APIKeyAuthentication:
    """
    Class-based API key authentication for use in views.
    """
    
    @staticmethod
    def authenticate(request):
        api_key = get_api_key_from_request(request)
        
        if not api_key:
            return None, {'error': 'API key required', 'code': 401}
        
        key_obj = APIKey.validate_key(api_key)
        
        if not key_obj:
            return None, {'error': 'Invalid API key', 'code': 403}
        
        # Update last used
        key_obj.last_used_at = timezone.now()
        key_obj.save(update_fields=['last_used_at'])
        
        return key_obj, None
