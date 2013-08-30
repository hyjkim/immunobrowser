from django import template

register = template.Library()

@register.inclusion_tag('menu_tag.html')
def menu_tag(*args):
    MENU_FIELDS = [
        {'view': 'samples.views.home', 'name': 'Browse', 'active': False},
        {'view': 'dashboard.views.compare_v2', 'name': 'Compare', 'active': False},
        {'view': '', 'name': 'Blast', 'active': False},
        {'view': '', 'name': 'Upload', 'active': False},
    ]

    try:
        active_view = args[0]
        for item in MENU_FIELDS:
            if item['view'] == active_view:
                item['active']=True
    except:
        pass

    context = {'menu': MENU_FIELDS}
    return context
