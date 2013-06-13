from django import template


register = template.Library()


@register.inclusion_tag('clonotype.html')
def clonotype_tag(clonotype):
    return {'clonotype': clonotype}

@register.inclusion_tag('amino_acid.html')
def amino_acid_tag(amino_acid):
    return {'amino_acid': amino_acid}
