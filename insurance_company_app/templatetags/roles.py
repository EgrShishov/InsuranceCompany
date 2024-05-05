from django import template

register = template.Library()


@register.filter(name='is_employee')
def is_employee(user):
    return user.groups.filter(name='Employee').exists()


@register.filter(name='is_user')
def is_user(user):
    return user.groups.filter(name='User').exists()


@register.filter(name='is_superuser')
def is_user(user):
    return user.is_superuser
