from django.shortcuts import render

# Create your views here.


def account(request):
    return render(request, 'accounts/index.html')