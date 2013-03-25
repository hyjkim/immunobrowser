from django.shortcuts import render
from clonotypes.models import Clonotype, ClonoFilter
from samples.models import Sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


def amino_acid_detail(request, amino_acid_id):
    from clonotypes.models import AminoAcid
    amino_acid = AminoAcid.objects.get(id=amino_acid_id)
    context = {'amino_acid': amino_acid}
    return render(request, 'amino_acid_detail.html', context)


def all(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    clonotypes = Clonotype.objects.filter(sample=sample)
    paginator = Paginator(clonotypes, 25)
    page = request.GET.get('page')
    try:
        clonotypes = paginator.page(page)
    except PageNotAnInteger:
        clonotypes = paginator.page(1)
    except EmptyPage:
        clonotypes = paginator.page(paginator.num_pages)
    context = {'sample': sample, 'clonotypes': clonotypes}
    return render(request, 'all.html', context)


def detail(request, clonotype_id):
#    pass
#    try:
    clonotype = Clonotype.objects.get(id=clonotype_id)
    sample = clonotype.sample
    context = {'clonotype': clonotype, 'sample': sample}
    return render(request, 'detail.html', context)


def bubble(request, clonofilter):
    ''' Takes in a filter and returns a bubble image generated by matplolib '''
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from pylab import text, xlabel, ylabel
    from numpy import median
    #from clonotypes.models import Clonotype
    from clonotypes.models import Recombination

    response = HttpResponse(content_type='image/png')
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    x = []
    y = []
    color = []
    data = []
    area = []

    vj_counts = clonofilter.vj_counts()

    # Calculate the plotting area by finding the number of v's and j's
    width = len(Recombination.v_family_names())
    height = len(Recombination.j_gene_names())



    # Data wrangling to generate plot stuff
    for v_index, list in enumerate(vj_counts):
        for j_index, counts in enumerate(list):
            x.append(v_index)
            y.append(j_index)
            color.append(counts)
            data.append(counts)
#        text(data[1], data[5],
#             data[0], size=11, horizontalalignment='center')

    # Normalize area by the median and plot area
    #area_norm_factor = (1.0/median(data)) * width * height
    if data:
        area_norm_factor = (2.0/max(data)) * width * height
        area = [datapoint * area_norm_factor for datapoint in data]

    sct = ax.scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)

#    ax.axis([0, 11, 200, 1280])
#    xlabel('Gene segments')
#    ylabel('Gene segments')

    canvas.print_png(response)
    return response


def bubble_default(request, sample_id):
    '''
    DEPRECATED
    If no filter is defined, you can still plot a bubble given just a
    sample id with this function. Otherwise, a clonofilter defined through
    GET will be passed to bubble()'''

    s = Sample.objects.filter(id=sample_id).get()

    try:
        clonofilter = ClonoFilter.objects.get(id=request.GET['clonofilter'])
    except:
        clonofilter = ClonoFilter(sample=s)

    return bubble(request, clonofilter)

def spectratype(request, clonofilter):
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from numpy import array

    response = HttpResponse(content_type='image/png')
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    cdr3_sums = array(clonofilter.cdr3_length_sum())
    ax.plot(cdr3_sums[:, 0].tolist(), cdr3_sums[:, 1].tolist(), '-')
    ax = fig.add_subplot(111)

    canvas.print_png(response)
    return response


def spectratype_default(request, sample_id):
    '''
    DEPRECRATED

    wrapper to create a spectratype given only a sample_id
    '''
    s = Sample.objects.filter(id=sample_id).get()
    try:
        clonofilter = ClonoFilter.objects.get(id=request.GET['clonofilter'])
    except:
        clonofilter = ClonoFilter(sample=s)

    return spectratype(request, clonofilter)
