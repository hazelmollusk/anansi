from django.conf.urls import url
from django.shortcuts import redirect
import views

urlpatterns = (
    url(r'dash/$', views.DashView.as_view(), name='dash'),
    
    url(r'hosts/$', views.HostListView.as_view(), name='host-list'),
    url(r'hosts/create$', views.HostCreateView.as_view(), name='host-create'),
    url(r'host/(?P<pk>[0-9]*)/update$', views.HostUpdateView.as_view(), name='host-update'),
    url(r'host/(?P<pk>[0-9]*)/delete$', views.HostDeleteView.as_view(), name='host-delete'),
    url(r'host/(?P<pk>[0-9]*)/$', views.HostDetailView.as_view(), name='host-detail'),
    
    url(r'groups/$', views.GroupListView.as_view(), name='group-list'),
    url(r'groups/create$', views.GroupCreateView.as_view(), name='group-create'),
    url(r'group/(?P<pk>[0-9]*)/update$', views.GroupUpdateView.as_view(), name='group-update'),
    url(r'group/(?P<pk>[0-9]*)/delete$', views.GroupDeleteView.as_view(), name='group-delete'),
    url(r'group/(?P<pk>[0-9]*)/$', views.GroupDetailView.as_view(), name='group-detail'),
        
    url(r'collectors/$', views.CollectorListView.as_view(), name='collector-list'),
    url(r'collectors/create$', views.CollectorCreateView.as_view(), name='collector-create'),
    url(r'collector/(?P<pk>[0-9]*)/update$', views.CollectorUpdateView.as_view(), name='collector-update'),
    url(r'collector/(?P<pk>[0-9]*)/delete$', views.CollectorDeleteView.as_view(), name='collector-delete'),
    url(r'collector/(?P<pk>[0-9]*)/$', views.CollectorDetailView.as_view(), name='collector-detail'),
    url(r'collector/(?P<slug>[-\w]+)/update$', views.CollectorUpdateView.as_view(), name='collector-update'),
    url(r'collector/(?P<slug>[-\w]+)/delete$', views.CollectorDeleteView.as_view(), name='collector-delete'),
    url(r'collector/(?P<slug>[-\w]+)/$', views.CollectorDetailView.as_view(), name='collector-detail'),

    url(r'libraries/$', views.LibraryListView.as_view(), name='library-list'),
    url(r'libraries/create$', views.LibraryCreateView.as_view(), name='library-create'),
    url(r'library/(?P<pk>[0-9]*)/update$', views.LibraryUpdateView.as_view(), name='library-update'),
    url(r'library/(?P<pk>[0-9]*)/delete$', views.LibraryDeleteView.as_view(), name='library-delete'),
    url(r'library/(?P<pk>[0-9]*)/$', views.LibraryDetailView.as_view(), name='library-detail'),
    
        
    url(r'collectors/$', views.CollectorListView.as_view(), name='collector-list'),
    url(r'collectors/create$', views.CollectorCreateView.as_view(), name='collector-create'),
    url(r'collector/(?P<pk>[0-9]*)/update$', views.CollectorUpdateView.as_view(), name='collector-update'),
    url(r'collector/(?P<pk>[0-9]*)/delete$', views.CollectorDeleteView.as_view(), name='collector-delete'),
    url(r'collector/(?P<pk>[0-9]*)/$', views.CollectorDetailView.as_view(), name='collector-detail'),
            
    url(r'roles/$', views.RoleListView.as_view(), name='role-list'),
    url(r'roles/create$', views.RoleCreateView.as_view(), name='role-create'),
    url(r'role/(?P<pk>[0-9]*)/update$', views.RoleUpdateView.as_view(), name='role-update'),
    url(r'role/(?P<pk>[0-9]*)/delete$', views.RoleDeleteView.as_view(), name='role-delete'),
    url(r'role/(?P<pk>[0-9]*)/$', views.RoleDetailView.as_view(), name='role-detail'),
            
    url(r'books/$', views.BookListView.as_view(), name='book-list'),
    url(r'books/create$', views.BookCreateView.as_view(), name='book-create'),
    url(r'book/(?P<pk>[0-9]*)/update$', views.BookUpdateView.as_view(), name='book-update'),
    url(r'book/(?P<pk>[0-9]*)/delete$', views.BookDeleteView.as_view(), name='book-delete'),
    url(r'book/(?P<pk>[0-9]*)/$', views.BookDetailView.as_view(), name='book-detail'),
)