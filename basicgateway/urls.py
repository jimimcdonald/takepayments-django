"""basicgateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
# ^^^ this is not ideal!

from gateway import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gateway/', include('gateway.urls')),
    path('', RedirectView.as_view(url='/gateway/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += patterns('',
#     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.STATIC_ROOT,
#     }),
# )

# urlpatterns += patterns('',
#     url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views', {
#         'document_root': settings.STATIC_ROOT,
#     }),
#  )
