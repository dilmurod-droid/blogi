from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from blog.models import Blog
from myapp.forms import UserRegisterForm, Editpr
from myapp.models import CustomUser


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html')
        else:
            return render(request, 'registration/login.html')


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        return super().form_valid(form)
class Profile(LoginRequiredMixin,ListView):
    model = Blog
    template_name = 'profile.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        return Blog.objects.filter(author=user)

@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = CustomUser
    form_class = Editpr
    template_name = 'editprofile.html'

    def get_success_url(self):# Change this to your profile view URL
        obj = self.get_object()
        return reverse('profile', kwargs={'username': obj.username})

    def get_object(self):
        return self.request.user


class users_accs(ListView):
    model = CustomUser
    template_name = 'user_accs.html'
    context_object_name = 'user'
