from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.utils.encoding import python_2_unicode_compatible
from polymorphic import PolymorphicModel


@python_2_unicode_compatible
class AnansiBaseEntity(PolymorphicModel):
    """Base class for Anansi objects"""
    name = models.SlugField(max_length=64)
    # TODO: do we want to subclass a more complex auditor?

    def __str__(self): return self.name

    def get_variable(self, key):
        try: return self.variables.get(name=key).value
        except ObjectDoesNotExist: return ''

    def set_variable(self, key, val, auto=False):
        var, created = self.variables.update_or_create(name=key, host=self, auto=auto, defaults={'value':val})

    def has_variable(self, key):
        return self.variables.filter(host=self, name=key).exists()

    def get_variables(self): #TODO must include vargroup vars
        return dict( [ (v.name, v.value) for v in self.variables.all() ])

class AnansiResourceEntity(AnansiBaseEntity):
    """Generic interface for connecting an external resource"""
    description = models.TextField()
    domain = models.CharField(max_length=64, blank=True, null=True)
    hostname = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)
    protocol = models.CharField(max_length=16, blank=True, null=True)
    secret = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=64, blank=True, null=True)

    class Meta: pass

class AnansiInventoryEntity(AnansiBaseEntity):
    auto = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_tag(self, key):
        return self.get_variable('anansi_tag_%s' % key)

    def set_tag(self, key, val):
        self.set_variable('anansi_tag_%s' % key, val, True)

    def has_tag(self, key):
        return self.has_variable(self, 'anansi_tag_%s' % key)

    class Meta:
        pass

@python_2_unicode_compatible
class AnansiVariable(models.Model):
    """Generic variable attached to any entity"""
    entity = models.ForeignKey(AnansiBaseEntity, related_name='variables', related_query_name='variable')
    name = models.SlugField(max_length=64)
    value = models.CharField(max_length=128)
    auto = models.BooleanField(default=True)
    # TODO: add fields for overrideable, variable type hints (for playbook usage)

    class Meta:
        verbose_name = 'variable'

    def __str__(self): return self.name

class AnansiVariableGroup(AnansiBaseEntity):
    entity = models.ManyToManyField(AnansiInventoryEntity, related_name='variable_sgroups', related_query_name='variable_group')

    class Meta:
        verbose_name = 'variable group'

@python_2_unicode_compatible
class AnansiTag(models.Model):
    """An inventory tag used in building group memberships"""
    name = models.SlugField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'tag'

    def __str__(self): return self.name

@python_2_unicode_compatible
class AnansiTagOption(models.Model):
    """A selectable option for the given tag"""
    tag = models.ForeignKey(AnansiTag, related_name='options', related_query_name='option')
    value = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'tag option'

    def __str__(self): return '%s(%s)' % (self.tag.name, self.value)

class AnansiHost(AnansiInventoryEntity):
    """A single discovered host"""
    source = models.ForeignKey('AnansiCollector', blank=True, null=True, related_name='hosts', related_query_name='host')
    active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'host'

    #TODO: must include group vars, vargroup vars
    def get_variables(self):
        pass

class AnansiGroup(AnansiInventoryEntity):
    """A group of discovered hosts; may contain variables and subgroups"""
    hosts = models.ManyToManyField(AnansiHost, related_name='groups', related_query_name='group')
    subgroups = models.ManyToManyField('self', symmetrical=False)

    class Meta:
        verbose_name = 'group'

    def get_hosts(self):
        """Recursively build list of all hosts in this group"""
        host_list = set(self.hosts.filter(active=True))
        subgroups = self.subgroups.all()
        if len(subgroups) > 0:
            for subgroup in subgroups:
                host_list = host_list.union(set(subgroup.get_hosts()))
        return list(host_list)

@python_2_unicode_compatible
class AnansiGroupPattern(models.Model):
    pattern = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'group pattern'

    def __str__(self): return self.pattern

@python_2_unicode_compatible
class AnansiCollector(AnansiResourceEntity):
    """Base class for collector implementations"""
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Collector'

    def __str__(self): return self.name

    def save(self): super(AnansiCollector, self).save()

    def get_absolute_url(self): return reverse('anansi:collector', args=[str(self.id)])

    def collect_hosts(self):
        """
        Collect hosts

        This method must be implemented by sub-classes of
        Collector, and should return a dictionary of
        { 'host_name' : { 'variable1' : 'value', ... } }
        """
        raise NotImplementedError

    def get_collector_type(self):
        """Short name for this collector type"""
        raise NotImplementedError

    def update(self, fetch=True):
        """
        Update the inventory for this collector

        Calls the sub-class implementation of collect_hosts(),
        updates inventory and adds necessary metadata.
        """
        try:
            if fetch:
                # deactivate existing hosts, add collected
                self.hosts.update(active=False)
                for hostname, variables in self.collect_hosts().items():
                    self._add_host(hostname, variables)
            # assign tags, groups
            self._update_metadata()
            self.last_updated = datetime.now()
            self.save()
        except Exception, e:
            pass

    #TODO: these should probably be cached class properties elsewhere
    @cached_property
    def _tag_map(self):
        return dict([
                (tag.name, [ opt.value for opt in tag.options.all() ])
                for tag in AnansiTag.objects.all()
            ])

    @cached_property
    def _pattern_list(self):
        return [ p.pattern for p in AnansiGroupPattern.objects.all() ]

    def _add_host(self, hostname, variables=None):
        """Add or update a discovered host"""
        # create/activate host as needed
        host, created = AnansiHost.objects.get_or_create(name=hostname)
        host.last_seen = datetime.now()
        host.active = True
        host.source = self
        host.save()
        # remove existing automatic variables
        host.variables.filter(auto=True).delete()
        # add collected variables
        if variables is not None:
            for k, v in variables.items():
                host.set_variable(k, v)
        # add collector variables
        host.set_variable('anansi_source', self.slug)
        host.set_variable('anansi_source_type', self.get_collector_type())
        host.set_variable('anansi_source_class', self.__class__.__name__.lower())

    def _update_metadata(self):
        for host in self.hosts.all():
            # add tag variables from hostname
            host_parts = host.name.split('-')
            # host_parts ~= [ 'db', 'us', 'prod', '1' ]
            for tag, tag_opts in self._tag_map:
                for opt in tag_opts:
                    if opt in host_parts:
                        host.set_tag(tag, opt, True)
            # add host to groups from tags
            for pattern in self._pattern_list:
                # pattern ~= 'type-site-stage'
                group_parts = []
                parts = pattern.split('-')
                # parts ~= [ 'type', 'site', 'stage' ]
                for part in parts:
                    if host.has_tag(part): group_parts.append(host.get_tag(part))
                    else: break
                else:
                    # host has all the required tags
                    # host_parts ~= [ 'db', 'us', 'prod' ]
                    group_name = '-'.join(group_parts)
                    # group_name ~= 'db-us-prod'
                    group, created = AnansiGroup.objects.get_or_create(name=group_name, auto=True)
                    if created: group.save()
                    host.groups.add(group)

#TODO: this
class AnansiEC2Collector(AnansiCollector):
    region = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'EC2 collector'

    def get_collector_type(self): return 'ec2'

    def collect_hosts(self): pass

class AnansiStaticCollector(AnansiCollector):
    filename = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Static Collector'

    def get_collector_type(self): return 'static'

    def collect_hosts(self): pass

class AnansiVMWareCollector(AnansiCollector):
    datacenter = models.CharField(max_length=32, blank=True, null=True)
    cluster = models.CharField(max_length=32, blank=True, null=True)
    resource_pool = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = 'VMWare collector'

    def get_collector_type(self): return 'vmware'

    def collect_hosts(self):
        host_list = {}
        try:
            params = { 'status':'poweredOn' }
            if self.datacenter: params['datacenter'] = self.datacenter
            if self.cluster: params['cluster'] = self.cluster
            if self.resource_pool: params['resource_pool'] = self.resource_pool
            vm_list = self._vserver.get_registered_vms(status='poweredOn')
            for vm_path in vm_list:
                vm = self._vserver.get_vm_by_path(vm_path)
                vm_name = vm.get_property('name')
                # TODO: collect more info
                host_list[vm_name] = {}
        except:
            pass
        return host_list

    @cached_property
    def _vserver(self):
        import pysphere
        vs = pysphere.VIServer()
        vs.connect(self.target.hostname, self.target.username, self.target.password)
        return vs
