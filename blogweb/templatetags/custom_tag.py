from django import template

# Instantiate a new object of django template.Library
register = template.Library()


# Customize a filter with plus functionality, just for testing.
# @register.filter()
# def plus(item):
#     return int(item) + 1


@register.inclusion_tag("custom_tag/headers.html")
def banner(name):
    """
    Use "inclusion_tag" to render a header template
    """
    print(name)

    header_img_list = [
        "/static/assets/img/header/g-class1.png",
        "/static/assets/img/header/g-class2.png",
        "/static/assets/img/header/g-class3.png",
        "/static/assets/img/header/g-class4.png"
    ]

    return {"img_list": header_img_list}
