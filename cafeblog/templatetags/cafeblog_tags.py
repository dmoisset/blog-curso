from django import template
from django.forms.util import ErrorList, ErrorDict
register = template.Library()


HIGH = "progress-danger"
MEDIUM = "progress-warning"
LOW = "progress-info"

error_snippet = u"""
  <div class='alert alert-error'>
    <button type='button' class='close' data-dismiss='alert'>&times;</button>
    <strong>Warning!</strong> %s
  </div>
"""

@register.simple_tag
def display_error(message, **kwargs):
    return error_snippet%message

@register.simple_tag
def display_error_if(messages, **kwargs):
    ret_val = ""
    if isinstance(messages, ErrorList):
        for e in messages:
            ret_val += display_error(e)+'\n'
    elif isinstance(messages, ErrorDict):
        # Show errors general of the form, not field specific.
        try:
            ret_val = display_error(messages['__all__'])
        except KeyError:
            pass
    elif isinstance(messages, unicode) or isinstance(messages, str):
        ret_val = error_snippet%messages
    return ret_val