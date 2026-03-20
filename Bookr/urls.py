"""
URL configuration for Bookr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

# Ajouter l'import de votre vue
import bookOnline.views
import backoffice.views
import bookOnline.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bookOnline.views.index), # => Ajout
    path('backoffice', backoffice.views.index),
    path('backoffice/getProduct', backoffice.views.getProduct),
    path('backoffice/getDetails', backoffice.views.getDetails),
    path('bookOnline', bookOnline.views.getBookOnline), 
    path('bookOnline/getLivres', bookOnline.views.getLivres), 
    path('bookOnline/getLivresFiltered', bookOnline.views.getLivresFiltered), 
    path('bookOnline/getLivresStatus', bookOnline.views.getLivresStatus)
]