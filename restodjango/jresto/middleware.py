from django.shortcuts import redirect
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.session.get_expiry_age)
        # Check if user is authenticated and session has expired
        if request.user.is_authenticated and request.session.get_expiry_age() <= 0:
            logout(request)  # Log out the user
            return redirect('user_login')  # Redirect to login page
        
        response = self.get_response(request)
        return response
