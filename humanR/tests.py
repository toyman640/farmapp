from django.test import TestCase

# Create your tests here.


def worker_check(request):
    qs = Employee.objects.all()
    if request.method == 'GET':
        search_form = EmployeeFilter(request.GET)
        if search_form.is_valid():
            surname = search_form.cleaned_data.get('employee_SN')
            name = search_form.cleaned_data.get('employee_FN')
            section = search_form.cleaned_data.get('section_id')
            title = search_form.cleaned_data.get('title_id')

            if surname != '' and surname is not None:
                qs = qs.filter(employee_SN__icontains=surname)
            if name != '' and name is not None:
                qs = qs.filter(employee_FN__icontains=name)
            
            if section != '' and section is not None:
                qs = qs.filter(section_id__section_name__contains=section)

            if title != '' and title is not None:
                qs = qs.filter(title_id__title_name__contains=title)
            return render(request, 'hr/search-page.html', {'result': qs})
        else:
            return render(request, 'hr/search-page.html')
