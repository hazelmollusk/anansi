from optparse import make_option
try: import json
except ImportError: import simplejson as json
from django.core.management.base import BaseCommand, CommandError
from anansi.models import *

class Command(BaseCommand):
  args = '[options]'
  help = 'Generate dynamic inventory data for ansible'

  option_list = BaseCommand.option_list + (
        make_option('--list',
            action='store_true',
            dest='show_list',
            default=False,
            help='List all active groups and hosts'),
        make_option('--host',
            action='store',
            dest='host',
            help='Show information on a single host'),
        make_option('--update',
            action='store_true',
            dest='update',
            help='Update all collectors'),
        make_option('--update-groups',
            action='store_true',
            dest='update_groups',
            help='Update group membership'),
        make_option('--collector',
            action='store',
            dest='collector',
            default=None,
            help='Use specified collector'),
        )

  def handle(self, *args, **options):
    c = options['collector']

    if    options['show_list']:     self.output_list(c)
    elif  options['host']:          self.output_host(options['host'])
    elif  options['update']:        self.update(c)
    if    options['update_groups']: self.update_groups(c)

  def output_list(self, name=None):
    jsobj = {}
    group_hosts = None
    for group in InventoryGroup.objects.all():
      group_hosts = group.hosts.filter(active=True)
      if name is not None: group_hosts = group_hosts.filter(source__slug=name)
      if group_hosts.exists():
        jsobj[group.name] = {
         'hosts': [ host.name for host in group_hosts ]
        }
        if group.subgroups.exists():
          jsobj[group.name]['children'] = [ g.name for g in group.subgroups.all() ]
        if group.variables.exists():
          jsobj[group.name]['vars'] = {}
          for var in group.variables.all():
            jsobj[group.name]['vars'][var.name] = var.value
    if group_hosts is not None:
      jsobj['_meta'] = {}
      for host in group_hosts:
        jsobj['_meta'][host.name] = dict( [ (v.name, v.value) for v in host.variables.all() ] )
        if host.source:
          jsobj['_meta'][host.name]['source'] = host.source.name
    self.stdout.write(json.dumps(jsobj, indent=4, separators=(',',': ')))

  #TODO should this include inherited group vars?
  def output_host(self, hostname):
    try:
      host = InventoryHost.objects.get(name=hostname)
      jsobj = dict( [ (v.name, v.value) for v in host.variables.all() ] )
      self.stdout.write(json.dumps(jsobj, indent=4, separators=(',',': ')))
    except: return

  def update(self, name=None):
    collectors = InventoryCollector.objects.all()
    if name is not None: collectors = collectors.filter(slug=name)
    for c in collectors:
      self.stdout.write('Collecting for %s...' % c.name)
      c.collect()

  def update_groups(self, name=None):
    collectors = InventoryCollector.objects.all()
    if name is not None: collectors = collectors.filter(slug=name)
    for c in collectors:
      self.stdout.write(' for %s...' % c.name)
      c.update_groups()
