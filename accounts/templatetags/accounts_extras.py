from django import template
from django.utils.html import format_html


register = template.Library()


# @register.filter
# def role_text(value):
#     if value:
#         value = format_html('<span class="text-success">&#10004;</span>')
#     else:
#         value = format_html('<span class="text-danger">&#10008;</span>')
#     return value