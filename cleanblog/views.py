from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import(
    ListView, CreateView, DetailView, UpdateView
)

# -----------------------
from .models import Post, Author
from .form import LoginForm, PostForm, SearchPostForm
from .utils.validators import Validator
from .utils.modal import Modal
# -----------------------

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def clear_data(request):
    request.session.pop("open_modal", False)
    request.session.pop("message", None)
    return JsonResponse({})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '').strip()
        context['form'] = SearchPostForm(initial={'search': search})
        context['search'] = search
        return context

# -----------------------

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/form.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['edition'] = False
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        modal = Modal(request)
        form = self.get_form()
        if form.is_valid():
            try:
                form.instance.author = get_object_or_404(Author, user=self.request.user)
                form.save()
                modal.create_message(request, 'Successfully created.')
            except Exception as error:
                print(error)
                modal.create_message(request, 'Error creating.')
        else:
            return render(request, self.template_name, {'form':form})
        return redirect(reverse_lazy('post-list'))

# -----------------------

class PostDetailView(DetailView):
    model = Post
    template_name='post/detail.html'

# -----------------------

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/form.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Validator().validate_author_for_edition(self.object, self.request.user):
            Modal(request).create_message(request, 'You cannot edit or delete posts from this author.')
            return redirect('post-list')  
        self.request.session['edition'] = True
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_name"] = self.object.author.name
        context["picture_url"] = f"/media/{self.object.picture}"
        return context
    
    def post(self, request, *args, **kwargs):
        modal = Modal(request)
        if Validator().validate_author_for_edition(self.object, self.request.user):
            modal.create_message(request, 'You cannot edit or delete posts from this author.')
            return redirect(reverse_lazy('post-list'))    
        
        obj = self.object
        if 'delete' in request.POST:
            try:
                obj.delete()
                modal.create_message(request, 'Successfully deleted.')
            except:
                modal.create_message(request, 'Error deleting.')
        else:
            form = self.form_class(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                try:
                    form.instance.updated_at = timezone.now()
                    form.save()
                    modal.create_message(request, 'Successfully edited.')
                except:
                    modal.create_message(request, 'Error editing.')
            else:
                return render(request, self.template_name, {'form':form, 'author_name': self.object.author.name, 'picture_url': f"/media/{self.object.picture}"})
        return redirect(reverse_lazy('post-list'))    

# -----------------------

def login_auth(request):
    modal = Modal(request)
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if not user is None:
                    login(request, user)
                    modal.create_message(request, 'Sucessfully logged in.')
                    return redirect(reverse_lazy('post-list'))
                else:
                    modal.create_message(request, 'Invalid username and password.')
            else:
                return render(request, 'login/form.html', {'form':form})
        else:
            form = LoginForm()
        return render(request, 'login/form.html', {'form':form})
    else:
        modal.create_message(request, 'User is already logged in.')
        return redirect(reverse_lazy('post-list'))
    
# -----------------------
    
@login_required(login_url='login')
def logout_auth(request):
    modal = Modal(request)
    if request.user.is_authenticated:
        logout(request)
        modal.create_message(request, 'Successfully logged off.')    
    else:
        modal.create_message(request, 'User is already logged off.')    
    return redirect(reverse_lazy('post-list'))

# -----------------------

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)