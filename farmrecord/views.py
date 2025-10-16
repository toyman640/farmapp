# from django.shortcuts import render, redirect
# from .forms import EventForm

# def create_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES, user=request.user)
#         if form.is_valid():
#             event = form.save()
#             # If an image was uploaded, create EventImage record
#             image = form.cleaned_data.get('image')
#             if image:
#                 EventImage.objects.create(event=event, image=image)
#             return redirect('event_list')  # change to your event list view
#     else:
#         form = EventForm(user=request.user)
#     return render(request, 'event_form.html', {'form': form})
