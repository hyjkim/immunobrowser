def undefaulted(x):
    '''
    Given an arbitrarily nested defaultdict, return a nested native dict.
    Code from http://stackoverflow.com/questions/4442975/how-do-i-convert-a-derived-recursive-data-type-to-a-base-data-type
    '''
    from collections import defaultdict
    return dict(
        (k, undefaulted(v))
        for (k, v) in x.iteritems()
    ) if isinstance(x, defaultdict) else x


def sub_dict_remove(somedict, somekeys, default=None):
    '''
    Retrieves a subset of a dict given a list of keys. Preserves
    original dict
    '''
    return dict([ (k, somedict.pop(k, default)) for k in somekeys ])

def sub_dict_remove_strict(somedict, somekeys):
    '''
    Retrieves a subset of a dict given a list of keys. Modifies
    original dict by removing queried key:value pairs
    '''
    return dict([ (k, somedict.pop(k)) for k in somekeys ])
