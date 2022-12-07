from django.shortcuts import render

# Create your views here.

def transport_home(request):

    return render(request, 'logistics/index.html')

def feed_rec(request):

    return render(request, 'logistics/feed-rec.html')