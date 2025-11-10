from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
# -----------------------
from ..models import Author, Category
# -----------------------

class Validator:
    def validate_username(self, data):
        if not data or not data.strip():
            raise ValidationError('Username is empty.')
        validator = RegexValidator(regex=r'^\S+$', message='Username cannot contain space.')
        validator(data)
        return data

    def validate_password(self, data):
        if not data or not data.strip():
            raise ValidationError("Password is empty.")
        return data

    def validate_string(self, string, label, min_length, max_length):
        if not string or not string.strip():
            raise ValidationError(f'{label.capitalize()} is empty.')
        if len(string) < min_length:
            raise ValidationError(f'{label.capitalize()} must be at least {min_length} characters long.')
        if len(string) > max_length:
            raise ValidationError(f'{label.capitalize()} must not exceed {max_length} characters.')
        return string
    
    def validate_category(self, category):
        if not category:
            raise ValidationError('Category is empty')
        exists = Category.objects.filter(pk=category.pk).exists()
        if not exists:
            raise ValidationError("Category does not exist.")
        return category

    def validate_picture(self, picture):
        if picture is None:
            raise ValidationError('Picture is empty.')
        return picture
    
    def validate_author_for_edition(self, post, _user):
        author =  get_object_or_404(Author, user=_user)
        return post.author != author
        
