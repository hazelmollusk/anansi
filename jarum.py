import types, re
from django.db.models.base import ModelBase

# just another random utility module

def flatten(l, ltypes=(list, tuple)):
    """Flatten a list of lists"""
    ltype, l, i = type(l), list(l), 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

def type_list(obj):
    """Return a list of types and super-types for an object"""
    if obj is object: return []
    return flatten([type_list(base) for base in obj.__bases__]) +[obj]

def uncamel(name):
    """Convert a camelCaseString to one_with_underscores"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class AdditionalOptions(object):
    """Generic Meta-style model configuration object"""
    def __init__(self, name):
        self.__dict__['_opts'] = {}
        self.__dict__['_name'] = name

    def __getattr__(self, k):
        if k in self._opts: return self._opts[k]
        else: raise KeyError

    def __setattr__(self, k, v):
        self._set_option(k, v, False)

    def _set_option(self, k, v, init=False):
        if not k.startswith('_') and (init or k in self._opts):
            list_types = (types.ListType, types.TupleType)
            force, default = True, False
            if k.endswith('_merge'):
                k, force = k.rstrip('_merge'), False
            elif k.endswith('_default'):
                k, default, force = k.rstrip('_default'), True, False
            if force or not k in self._opts:
                self._opts[k] = v
            elif default:
                return
            elif type(self._opts[k]) in list_types:
                if type(v) not in list_types: v = [v]
                self._opts[k] = list(self._opts[k]) + list(v)
            elif (type(self._opts[k]), type(v)) == (dict, dict):
                self._opts[k].update(v)
        else: raise KeyError('No such option: %s.%s' % (self._name, k))

class AdditionalMeta(ModelBase):
    """Metaclass which adds support for arbitrary Meta-style model configuration"""
    def __init__(cls, name, parents, attrs):
        super(AdditionalMeta, cls).__init__(name, parents, attrs)
        opt_list = {}
        for t in type_list(cls):
            for k, v in t.__dict__.items():
                if type(v) in (types.ClassType, type) and k.endswith('Meta') and k != 'Meta':
                    if not k in opt_list: opt_list[k] = AdditionalOptions(k)
                    for kk, vv in v.__dict__.items():
                        if not kk.startswith('_'):
                            #print '[%s] %s.%s.%s -> %s' % (cls.__name__, t.__name__, k, kk, str(vv))
                            opt_list[k]._set_option(kk, vv, True)
        for k, v in opt_list.items():
            setattr(cls, '_'+uncamel(k), v)
        super(AdditionalMeta, cls).__init__(name, parents, attrs)

class GenericViewSet(object):
    model = None
    name_prefix = ''
    name = None
    plural = None
    _cache = {}

    @classmethod
    def get_url_patterns(cls):
        from django.conf.urls import url
        name = cls.name or cls.model._meta.verbose_name.replace(' ', '-')
        plural = cls.plural or cls.model._meta.verbose_name_plural.replace(' ', '-')
        return (
            url(r'%s/$' % plural, cls.list(), name='%s-%s' % (cls.name_prefix, plural)),
            url(r'%s/create$' % plural, cls.create(), name='%s-%s-create' % (cls.name_prefix, plural)),
            url(r'%s/(?P<id>[0-9]*)/update$' % name, cls.update(), name='%s-%s-update' % (cls.name_prefix, name)),
            url(r'%s/(?P<id>[0-9]*)/delete' % name, cls.delete(), name='%s-%s-delete' % (cls.name_prefix, name)),
            url(r'%s/(?P<id>[0-9]*)/$' % name, cls.detail(), name='%s-%s-detail' % (cls.name_prefix, name)),
        )

    @classmethod
    def get_view_class(cls, view_class):
        class GV(view_class): model = cls.model
        return GV

    @classmethod
    def list(cls):
        from django.views.generic import ListView
        return cls.get_view_class(ListView).as_view()

    @classmethod
    def detail(cls):
        from django.views.generic import DetailView
        return cls.get_view_class(DetailView).as_view()

    @classmethod
    def update(cls):
        from django.views.generic import UpdateView
        cls.get_view_class(UpdateView).as_view()

    @classmethod
    def create(cls):
        from django.views.generic import CreateView
        return cls.get_view_class(CreateView).as_view()

    @classmethod
    def delete(cls):
        from django.views.generic import DeleteView
        return cls.get_view_class(DeleteView).as_view()
