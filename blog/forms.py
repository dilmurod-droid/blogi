from django import forms
from django.forms import ModelForm

from blog.models import Blog, Tag, Category, Comment


class BlogForm(forms.ModelForm):
    tags = forms.CharField(max_length=100)
    class Meta:
        model = Blog
        fields = ['title', 'body', 'photo', 'video', 'tags']

    def save(self, commit=True):
        blog = super().save(commit=False)

        # Handle tags
        tags_str = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]


        if tags_list:
            # Take the first tag as category
            category_name = tags_list[0]
            category, created = Category.objects.get_or_create(name=category_name)
            blog.category = category
        if commit:
            blog.save()
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        return blog

class Blog_search(forms.Form):
    query = forms.CharField(label='Search')

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']