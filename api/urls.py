from django.conf.urls import url, include
from rest_framework import routers
import views


api_v1 = routers.DefaultRouter()
api_v1.register(r'hosts', views.HostViewSet)
api_v1.register(r'groups', views.GroupViewSet)

urlpatterns = (
    url(r'^api/', include(router.urls)),
)