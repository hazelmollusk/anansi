from django.conf.urls import url, include


urlpatterns = (
    url(r'^web/', include('anansi.web.urls', namespace='anansi-web', app_name='anansi')),
    url(r'^api/', include('anansi.api.urls', namespace='anansi-api', app_name='anansi')),
)