from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .local_settings import ADMIN_URL
from .views import home

urlpatterns = [
    path(f'{ADMIN_URL}', admin.site.urls),
    path('', home, name='home'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('profile/', include(('user_profile.urls', 'user_profile'), namespace='profile')),
    path('content/', include(('content.urls', 'content'), namespace='content')),
    path('direct/', include(('direct.urls', 'direct'), namespace='direct')),
    path('log/', include(('log.urls', 'log'), namespace='log')),
    # path('tag/', include('tag.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)