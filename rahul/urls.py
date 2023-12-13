from django.conf.urls import url
from rahul.views import introduce

urlpatterns_error_pages = [
    url(regex=r'^rahul/$', name='error_403', view=introduce)
]