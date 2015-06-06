from django.conf.urls import url, include


urlpatterns = (
    url(r'^web/', include('anansi.web.urls')),
    url(r'^api/', include('anansi.api.urls')),
)