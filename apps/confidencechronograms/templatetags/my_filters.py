from django import template

register = template.Library()


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    result = round(float(qty*unit_price), 2)
    return (str(result).replace(".", ","))


@register.simple_tag()
def total(tl, *args, **kwargs):
    # you would need to do any localization of the result here
    result = round(float(tl), 2)
    return (str(result).replace(".", ","))


@register.simple_tag()
def sumthree(n1, n2, n3, *args, **kwargs):
    # you would need to do any localization of the result here
    result = round(float(n1+n2+n3), 2)
    return (str(result).replace(".", ","))

@register.simple_tag()
def substitui(subs, *args, **kwargs):
    # you would need to do any localization of the result here
    result = round(float(subs), 2)
    return (str(result).replace(".", ","))
