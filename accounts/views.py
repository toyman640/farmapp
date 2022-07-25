from django.shortcuts import render
from django.views.generic import ListView, FormView, TemplateView
from farmrecord.forms import PurchaseFormSet
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.


def account(request):
    return render(request, 'accounts/index.html')

def purchase_list(request):
    return render(request, 'purchase-list.html')


class PurchaseListView(ListView):
    model = Purchases
    template_name = "accounts/purchase-list.html"


class PurchaseAddView(TemplateView):
    template_name = "accounts/purchase-rec.html"

    def get(self, *arg, **kwargs):
        formset = PurchaseFormSet(queryset=Purchases.objects.none())
        return self.render_to_response({'purchase_formset' : formset})

    def post(self, request, *args, **kwargs):
        
        formset = PurchaseFormSet(data=self.request.POST)

        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('accounts:purchase_list'))

        return self.render_to_response({'purchase_formset' : formset})
    
    