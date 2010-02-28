from django.conf.urls.defaults import *


urlpatterns = patterns(
    '',
    url('^generate/$', 'yandexmarket.views.generate_yml',
        name='generate_yml'))
    
