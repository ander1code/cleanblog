from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import UniqueConstraint, CheckConstraint
from django.utils import timezone

# --------------------------------------------------------------------

class Author(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        error_messages={'null': 'A user is required to create an author.'}
    )

    name = models.CharField(
        'Name', 
        max_length=45, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(4, message="Name must be at least 4 characters long.")],
        error_messages={
            'blank': 'Please enter the author\'s name.',
            'null': 'Name cannot be null.',
            'max_length': 'Name cannot exceed 45 characters.',
        }
    )

    email = models.EmailField(
        'Email', 
        max_length=45, 
        blank=False, 
        null=False,
        validators=[EmailValidator(message='Please enter a valid email.')],
        error_messages={
            'blank': 'Please enter the author\'s email.',
            'null': 'Email cannot be null.',
            'invalid': 'Invalid email format.',
        }
    )

    occupation = models.CharField(
        'Occupation', 
        max_length=45, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(4, message="Occupation must be at least 4 characters long.")],
        error_messages={
            'blank': 'Please provide the author\'s occupation.',
            'null': 'Occupation cannot be null.',
            'max_length': 'Occupation cannot exceed 45 characters.',
        }
    )

    description = models.CharField(
        'Description', 
        max_length=300, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(10, message="Description must be at least 10 characters long.")],
        error_messages={
            'blank': 'Please provide a description for the author.',
            'null': 'Description cannot be null.',
            'max_length': 'Description cannot exceed 300 characters.',
        }
    )

    picture = models.ImageField(
        'Picture', 
        upload_to='authors', 
        blank=False, 
        null=False,
        error_messages={
            'blank': 'Please upload a picture for the author.',
            'null': 'Picture cannot be null.',
        }
    )

    class Meta:
        ordering = ['name']
        db_table = 'author'
        managed = True
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        constraints = [
            UniqueConstraint(
                fields=['email'], 
                name='unq_author_email', 
                violation_error_message='This email is already registered.'
            ),
        ]
    
    def __str__(self):
        return f"{self.pk}: {self.name}"

# --------------------------------------------------------------------

class Category(models.Model):
    title = models.CharField(
        max_length=45, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(5, message='Category title must be at least 5 characters long.')],
        error_messages={
            'blank': 'Please enter the category title.',
            'null': 'Category title cannot be null.',
            'max_length': 'Category title cannot exceed 45 characters.',
        }
    )

    class Meta:
        ordering = ['title']
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            UniqueConstraint(
                fields=['title'], 
                name='unq_category_title', 
                violation_error_message='This category is already registered.'
            )
        ]

    def __str__(self):
        return f"{self.title}"


# -----------------------

class Post(models.Model):
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        error_messages={'null': 'Author is required to create a post.'}
    )

    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        error_messages={'null': 'Category is required to create a post.'}
    )

    title = models.CharField(
        max_length=45, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(5, message="Title must be at least 5 characters long.")],
        error_messages={
            'blank': 'Please enter the post title.',
            'null': 'Title cannot be null.',
            'max_length': 'Title cannot exceed 45 characters.',
        }
    )

    briefing = models.CharField(
        max_length=100, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(10, message="Briefing must be at least 10 characters long.")],
        error_messages={
            'blank': 'Please enter the post briefing.',
            'null': 'Briefing cannot be null.',
            'max_length': 'Briefing cannot exceed 100 characters.',
        }
    )

    text = models.CharField(
        max_length=3000, 
        blank=False, 
        null=False,
        validators=[MinLengthValidator(100, message="Text must be at least 100 characters long.")],
        error_messages={
            'blank': 'Please enter the post text.',
            'null': 'Text cannot be null.',
            'max_length': 'Text cannot exceed 3000 characters.',
        }
    )

    picture = models.ImageField(
        upload_to='posts', 
        blank=False, 
        null=False,
        error_messages={
            'blank': 'Please upload an image for the post.',
            'null': 'Post image cannot be null.',
        }
    )

    created_at = models.DateTimeField(
        blank=False, 
        null=False, 
        default=timezone.now,
        error_messages={'null': 'Creation date cannot be null.'}
    )

    updated_at = models.DateTimeField(
        blank=True, 
        null=True, 
        error_messages={'null': 'Update date cannot be null.'}
    )

    class Meta:
        ordering = ['-created_at']
        db_table = 'post'
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        constraints = [
            CheckConstraint(
                check=Q(updated_at__isnull=True) | Q(updated_at__gte=F('created_at')),
                name='chk_post_updated_at',
                violation_error_message='Update date cannot be earlier than creation date.'
            )
        ]
    
    def __str__(self):
        return f"{self.title[0:15]}:{self.briefing[0:25]} | {self.text[0:50]}"