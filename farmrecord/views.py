# from django.contrib.auth.views import LoginView
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
from django.shortcuts import render

# class CustomLoginView(LoginView):
#     template_name = 'login.html'  # Your login template
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         # Log the user in
#         response = super().form_valid(form)
#         user = self.request.user

#         # Redirect based on roles
#         if hasattr(user, 'profile'):  # Check if User has a Userp profile
#             if user.profile.is_boss:
#                 return redirect('boss_dashboard')  # URL name for the boss dashboard
#             elif user.profile.is_supervisor:
#                 return redirect('supervisor_dashboard')  # URL name for the supervisor dashboard
#         return response  # Default redirection

#     def get_success_url(self):
#         return reverse_lazy('default_dashboard')  # Fallback redirect if no roles are matched


def dash_index(request):
    return render(request, 'index.html')
