from django import forms

# --------------------------------------------------------------------

from .models import (
    Post, Category
)
from .utils.validators import Validator

# --------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter a username.', 
                'value': 'anderson',
                'class': 'form-control'
                }
        )
    )

    password = forms.CharField(max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter a password.', 
                'value': '121181',
                'class': 'form-control'
            }
        )                         
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False   

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return Validator().validate_username(username)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return Validator().validate_password(password)

# --------------------------------------------------------------------

class PostForm(forms.ModelForm):

    author_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    title = forms.CharField(
        max_length=45,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    briefing = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    text = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(attrs={  
            'class': 'form-control',
            'cols':'30',
            'rows':'10',
            'maxlength':'3000'
        })
    )

    picture = forms.FileField(
        widget=forms.ClearableFileInput(attrs={  
            'class': 'form-control',
            'style': 'cursor:pointer;'
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        return Validator().validate_string(title, 'title', 5, 45)

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return Validator().validate_category(category)
    
    def clean_briefing(self):
        briefing = self.cleaned_data.get('briefing')
        return Validator().validate_string(briefing, 'briefing', 10, 100)
   
    def clean_text(self):
        text = self.cleaned_data.get('text')
        return Validator().validate_string(text, 'text', 100, 3000)
    
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        return Validator().validate_picture(picture)
    
    class Meta:
        model = Post
        fields = ('title', 'category', 'briefing', 'text', 'picture')

# --------------------------------------------------------------------
        
class SearchPostForm(forms.Form):
    
    search = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Search for...',
            'maxlength':"50"
        })
    )
