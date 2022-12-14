from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, TemplateView
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *

# Create your views here.

def transport_home(request):

    return render(request, 'logistics/index.html')

def feed_rec(request):
    feed_rec = FeedForm(request.POST)
    if feed_rec.is_valid():
            feed_rec.save()
            messages.success(request, 'Entry Saved')
            feed_rec = FeedForm()
    else:
        feed_rec = FeedForm()

    return render(request, 'logistics/feed-rec.html', {'feed_rec' : feed_rec})

def feed_post(request):
    feed_post = Feed.objects.order_by('-date')
    return render(request, 'logistics/feed-post.html', {'feed_post' : feed_post})

class DieselAddView(TemplateView):
    template_name = "logistics/diesel-rec.html"

    def get(self, *arg, **kwargs):
        d_formset = DieselFormSet(queryset=Diesel.objects.none())
        return self.render_to_response({'diesel_formset' : d_formset})

    def post(self, request, *args, **kwargs):
        
        d_formset = DieselFormSet(data=self.request.POST)

        if d_formset.is_valid():
            d_formset.save()
            return redirect(reverse_lazy('logistics:diesel_post'))

        return self.render_to_response({'diesel_formset' : d_formset})


def add_truck(request):
    if request.method == 'POST':
        new_truck = VehicleForm(request.POST, request.FILES)
        if new_truck.is_valid():
            new_truck.save()
            messages.success(request, 'Entry Saved')
            new_truck = VehicleForm()
    else:
        new_truck = VehicleForm()

    return render(request, 'logistics/new-truck.html', {'new_truck' : new_truck})


def view_truck(request):

    return render(request, 'logistics/truck-list.html')


    

def maintenance_rec(request):

    return render(request, 'logistics/maintenance-rec.html')

def diesel_post(request):
    diesel_rec = Diesel.objects.order_by('-date')
    return render(request, 'logistics/diesel-post.html', {'diesel_rec' : diesel_rec})