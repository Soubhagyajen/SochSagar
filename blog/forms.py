from django import forms
from .models import BlogPost,Poll
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BlogPostForm(forms.ModelForm):
    # image = forms.ImageField(required=False)
    class Meta:
        model = BlogPost
        fields = ['title','content',]
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        #     'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded h-40'}),
        # }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded dark:bg-gray-700 dark:text-white'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded dark:bg-gray-700 dark:text-white'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border rounded dark:bg-gray-700 dark:text-white'
            }),
        }



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required= True)
    
    class Meta:
        model = User
        fields =("username","email","password1","password2")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "w-full p-2 border rounded dark:bg-gray-700 dark:text-white"})    


from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded dark:bg-gray-700 dark:text-white'
            }),
        }


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option1', 'option2']

