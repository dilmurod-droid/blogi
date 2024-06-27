from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import request, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView,DeleteView,UpdateView,CreateView

from blog.forms import BlogForm, Blog_search, CommentCreateForm
from blog.models import Blog, Contact, Likes, Notification, Comment
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from myapp.models import CustomUser

class Home(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 10





class About(ListView):
    model = Blog
    template_name = 'about.html'
    context_object_name = 'about'


def contact_view(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    elif request.method == 'POST':
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        try:
            msg = Contact.objects.create(name=name, email=email, subject=subject, message=message)
            msg.save()
            messages.success(request, "Xabaringiz yuborildi!")
            messages.add_message(request, messages.INFO, "Hushyor bo'lavering")
        except Exception as err:
            messages.error(request, err)
        return render(request, 'contact.html')






# class Blogdetail(DetailView):
#     model = Blog
#     template_name = 'detail.html'
#     context_object_name = 'object'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         blog = self.get_object()
#         context['comments'] = blog.comments.all()
#         context['comment_form'] = CommentCreateForm()
#         if self.request.user.is_authenticated:
#             context['is_liked'] = Likes.objects.filter(author=self.request.user, blog=blog).exists()
#             context['notifications'] = self.request.user.notifications.filter(read=False)
#         else:
#             context['is_liked'] = False
#             context['notifications'] = None  # Notifications are only for authenticated users
#         context['like_count'] = blog.likes.count()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         blog = self.get_object()
#         comment_form = CommentCreateForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.blog = blog
#             new_comment.save()
#             if request.user != blog.author:
#                 Notification.objects.create(
#                     recipient=blog.author,
#                     message=f'{request.user.username} coment your blog "{blog.title}".'
#                 )
#         return redirect('detail', slug=blog.slug)
# @method_decorator(login_required, name='dispatch')
# class BlogLikeView(View):
#     def post(self, request, *args, **kwargs):
#         blog = get_object_or_404(Blog, slug=kwargs['slug'])
#         like, created = Likes.objects.get_or_create(author=request.user, blog=blog)
#         if not created:
#             like.delete()
#             if request.user != blog.author:
#                 Notification.objects.create(
#                     recipient=blog.author,
#                     message=f'{request.user.username} unliked your blog "{blog.title}".'
#                 )
#         else:
#             if request.user != blog.author:
#                 Notification.objects.create(
#                     recipient=blog.author,
#                     message=f'{request.user.username} liked your blog "{blog.title}".'
#                 )
#         return redirect('detail', slug=blog.slug)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['comments'] = blog.comments.all()
        context['comment_form'] = CommentCreateForm()
        if self.request.user.is_authenticated:
            context['is_liked'] = Likes.objects.filter(author=self.request.user, blog=blog).exists()
            context['notifications'] = self.request.user.notifications.filter(read=False)
        else:
            context['is_liked'] = False
        context['like_count'] = blog.likes.count()
        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.blog = blog
            new_comment.save()
        return redirect('detail', slug=blog.slug)

@login_required
@csrf_exempt
def like_post(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    like, created = Likes.objects.get_or_create(author=request.user, blog=blog)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    like_count = blog.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})
@login_required
@csrf_exempt
def comment_post(request, slug):
    if request.method == "POST":
        blog = get_object_or_404(Blog, slug=slug)
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.blog = blog
            new_comment.save()
            comment_data = {
                'author': new_comment.author.username,
                'body': new_comment.body,
                'img':new_comment.author.photo.url,
                'created_time': new_comment.created_time,
            }
            return JsonResponse({'success': True, 'comment': comment_data})
    return JsonResponse({'success': False})
@login_required
@require_POST
def comment_delete(request, slug):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        comment.delete()
        return JsonResponse({'deleted': True})
    else:
        return JsonResponse({'deleted': False})
class Delete(DeleteView):
    model = Blog
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

class Update(UpdateView):
    model = Blog
    fields = ['title','photo','video','tags','category','slug']
    template_name = 'update.html'
    success_url = reverse_lazy('home')


def generate_slug(title):
    return slugify(title)

class Create(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'create.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.author = self.request.user  # Blog muallifini avtomatik qo'shish
        form.instance.slug = generate_slug(form.instance.title[:50])
        return super().form_valid(form)

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')

@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.filter(read=False)


@login_required
def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'user_profile.html', {'user': user})

class UserProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'other_profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')  # URL dan username ni olish
        return get_object_or_404(CustomUser, username=username)