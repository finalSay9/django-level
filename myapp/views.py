from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from backend.myapp.forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_student:
            return reverse_lazy('student_dashboard')
        elif user.is_teacher:
            return reverse_lazy('teacher_dashboard')
        elif user.is_headteacher:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('home')