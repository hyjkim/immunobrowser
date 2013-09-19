from django import template
from dashboard.forms import SearchForm

register = template.Library()

@register.inclusion_tag('menu_tag.html')
def menu_tag(*args):
    # These menu items are a list of valid menu items
    MENU_FIELDS = [
        {'view': 'samples.views.home', 'name': 'Browse', 'active': False},
        {'view': 'cf_comparisons.views.compare_v3', 'name': 'Compare', 'active': False},
        {'view': 'lit_search.views.new', 'name': 'Literature Search', 'active': False},
        {'view': '', 'name': 'Upload', 'active': False},
    ]

    # Generate an empty search form
    search_form = SearchForm()

    # Try to find the active clas
    try:
        arg = args[0]
        if type(arg) == SearchForm:
            search_form = arg
        else:
            active_view = arg
            for item in MENU_FIELDS:
                if item['view'] == active_view:
                    item['active']=True
    except:
        pass

    context = {'menu': MENU_FIELDS,
               'search_form': search_form,
               }
    return context
