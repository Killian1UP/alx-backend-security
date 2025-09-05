from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django_ratelimit.decorators import ratelimit

# Create your views here.
def get_rate_limit_key(request):
    """Use user ID for authenticated users, IP for anonymous."""
    return str(request.user.id) if request.user.is_authenticated else request.META.get('REMOTE_ADDR')

def get_rate(request):
    """Dynamic rate: 10/min for authenticated, 5/min for anonymous."""
    return '10/m' if request.user.is_authenticated else '5/m'

@ratelimit(key=get_rate_limit_key, rate=get_rate, method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Login successful")
        return HttpResponse("Invalid credentials", status=401)

    return HttpResponse("Send a POST request with username and password")