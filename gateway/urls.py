# # --- LIVE MODE ---
#
# from django.urls import path
# from gateway import views
#
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('callback/', views.callback, name='callback'),
#     path('callback-server/', views.callbackServer, name='callback-server')
#]
## -----------------------------------------------------------------------------------
## To initiate developer mode, comment out the ↑↑above↑↑ code and uncommet ↓↓below↓↓.
## -----------------------------------------------------------------------------------

# --- DEV MODE ---

from django.urls import path
from gateway import viewsdev

urlpatterns = [
    path('', viewsdev.index, name='index'),
    path('callback/', viewsdev.callback, name='callback'),
    path('callback-server/', viewsdev.callbackServer, name='callback-server')
]
