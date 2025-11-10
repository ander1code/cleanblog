from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# -----------------------

from .views import (
    PostListView, PostCreateView, PostDetailView, PostUpdateView
)

from . import views

# -----------------------

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post-update'),
    path('clear-data/', views.clear_data, name="clear-data")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)