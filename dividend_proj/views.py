from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Holding
from django.http import HttpResponse

# Create your views here.

#login_required only allows viewing if logged in
#otherwise, redirects to the login page

@login_required
def dashboard(request):
    user_holdings = Holding.objects.filter(user=request.user)

    #pack data into dict

    context = {
        'holdings': user_holdings,
    }

    return render(request, 'dividend_proj/dashboard.html', context)


def home(request):
    return HttpResponse("Hello World")