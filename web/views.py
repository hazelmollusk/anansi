from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models.loading import get_models
from ..models import *

class DashView(TemplateView):
    template_name = 'anansi/dash.html'
    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)

        return context

class NameDetailView(DetailView): slug_field = 'name'

class HostListView(ListView): model = Host
class HostDetailView(NameDetailView): model = Host
class HostUpdateView(UpdateView): model = Host
class HostCreateView(CreateView): model = Host
class HostDeleteView(DeleteView): model = Host

class GroupListView(ListView): model = Group
class GroupDetailView(NameDetailView): model = Group
class GroupUpdateView(UpdateView): model = Group
class GroupCreateView(CreateView): model = Group
class GroupDeleteView(DeleteView): model = Group

class CollectorListView(ListView):
    model = Collector
    def get_context_data(self, **kwargs):
        context = super(CollectorListView, self).get_context_data(**kwargs)
        context['collector_types'] = [
            (m.__name__, m._meta.verbose_name.title())
            for m in get_models()
            if issubclass(m, Collector) and m is not Collector
        ]
        return context

class CollectorDetailView(NameDetailView): model = Collector
class CollectorUpdateView(UpdateView): model = Collector
class CollectorCreateView(CreateView): model = Collector
class CollectorDeleteView(DeleteView): model = Collector

class LibraryListView(ListView): model = Library
class LibraryDetailView(NameDetailView): model = Library
class LibraryUpdateView(UpdateView): model = Library
class LibraryCreateView(CreateView): model = Library
class LibraryDeleteView(DeleteView): model = Library

class BookListView(ListView): model = Book
class BookDetailView(NameDetailView): model = Book
class BookUpdateView(UpdateView): model = Book
class BookCreateView(CreateView): model = Book
class BookDeleteView(DeleteView): model = Book

class RoleListView(ListView): model = Role
class RoleDetailView(NameDetailView): model = Role
class RoleUpdateView(UpdateView): model = Role
class RoleCreateView(CreateView): model = Role
class RoleDeleteView(DeleteView): model = Role