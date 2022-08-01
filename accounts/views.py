from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.html import format_html
from django.views.generic import ListView, FormView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from farmrecord.forms import PurchaseFormSet, PurchaseFilter, EditPurchase
from .models import *
import csv
from django.urls import reverse_lazy
from django.shortcuts import redirect
from datetime import timedelta
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='/admin-page/login')
def account(request):
    return render(request, 'accounts/index.html')



@login_required(login_url='/admin-page/login')
def purchase_list(request):
    purch = Purchases.objects.order_by('-date')
    query_form = PurchaseFilter() 
    paginated_filterpi = Paginator(purch, 10)
    page_number = request.GET.get('page')
    pi_page_obj = paginated_filterpi.get_page(page_number)
    context = {
        'pi_page_obj' : purch,
        'q' : query_form

    }
    context['pi_page_obj'] = pi_page_obj
    return render(request, 'accounts/purchase-list.html', context)

@method_decorator(login_required, name='dispatch')
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

@login_required(login_url='/admin-page/login')
def delete_purchase(request, purch_id):
    post_record = get_object_or_404(Purchases, id=purch_id)
    post_record.delete()
    return redirect('accounts:purchase_list')


@login_required(login_url='/admin-page/login')
def purchase_filter(request):
    if request.method == 'GET':
        purchse_query = PurchaseFilter(request.GET)
        if purchse_query.is_valid():
            start_date = purchse_query.cleaned_data.get('start_date')
            end_date = purchse_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = Purchases.objects.filter(date__range=[start_date, new_end])
            if purchse_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Purchase-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Purchse For', 'Item', 'Quantity', 'Price per quantity', 'Total Price'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.section, row.item, row.quantity, row.i_price, row.price])
                return response
            return render(request, 'accounts/filter-purchases.html', {'queryset': result, 'q': purchse_query})
            
        else:
            messages.error(request, 'Out of range')
    else:
        purchse_query = PurchaseFilter()
    return render(request, 'accounts/filter-purchases.html', {'q': purchse_query})

@login_required(login_url='/admin-page/login')
def edit_purchase(request, item_id):
    single_log = get_object_or_404(Purchases, id=item_id)
    if request.method == 'POST':
        edit_purch = EditPurchase(request.POST, request.FILES, instance=single_log)
        if edit_purch.is_valid():
            edit_purch.save()
            messages.success(request, format_html('Edited Successfully,<a href="/accounts/purchses">click here to go back</a>'))
    else:
        edit_purch = EditPurchase(instance=single_log)
    return render(request, 'accounts/purchase-edit.html', {'purchase_edit': edit_purch})


    
    