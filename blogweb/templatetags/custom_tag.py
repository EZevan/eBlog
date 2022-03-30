from django import template

# Instantiate a new object of django template.Library
register = template.Library()


# Customize a filter with plus functionality
@register.filter()
def plus(item):
    return int(item) + 1
