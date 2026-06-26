from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    request: HttpRequest = context.get("request")
    if request and request.resolver_match and request.resolver_match.url_name == url_name:
        return "active"
    return ""
