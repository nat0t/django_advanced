from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('category/<int:pk>/ajax', cache_page(3600)(mainapp.products_ajax), name='ajax'),
    path('', mainapp.products, name='index'),
    path('<int:category_id>', mainapp.products, name='product'),
    path('page/<int:page>/', mainapp.products, name='page'),
]