from django import template
from django.template.loader import get_template

register = template.Library()

@register.inclusion_tag('anansi/bootstrap_button_dropdown.html')
def bootstrap_button_dropdown(label, url, param, options):
    return {
        'button_label':label,
        'button_url':url,
        'button_param':param,
        'button_options':options,
    }