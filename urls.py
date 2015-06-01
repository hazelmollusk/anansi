from django.conf.urls import url, include
from api.urls import urlpatterns as api_patterns
import views


urlpatterns = (
    url(r'^api/', include(api_patterns)),
)