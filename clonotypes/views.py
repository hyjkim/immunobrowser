from django.shortcuts import render
from clonotypes.models import Clonotype, ClonoFilter, Recombination
from samples.models import Sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


def domination_graph(request, clonofilter_id):
    '''
    Returns a PNG of the domination of a repertoire by a few highly expanded clones
    '''
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    response = HttpResponse(content_type='image/png')
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)

    clonofilter = ClonoFilter.objects.get(id=clonofilter_id)
    # Get clonotypes ordered by copy number

    canvas.print_png(response)
    return response

def functionality_graph(request, clonofilter_id):
    '''
    Returns a PNG of functionality of the clonofilter as a pie chart
    '''
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    response = HttpResponse(content_type='image/png')
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)

    clonofilter = ClonoFilter.objects.get(id=clonofilter_id)
    functionality_dict = clonofilter.functionality_dict()
    values = functionality_dict.values()
    labels = functionality_dict.keys()
    ax.pie(values, labels=labels)
    print functionality_dict


    canvas.print_png(response)
    return response

def j_usage_graph(request, clonofilter_id):
    '''
    Returns a PNG of j usage as a line graph
    '''
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    response = HttpResponse(content_type='image/png')
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)

    # variables which will contain data to be plotted
    usage = []
    gene_index = []

    # Retreive the clonofilter
    cf = ClonoFilter.objects.get(id=clonofilter_id)

    # Get v usage data
    j_usage_dict = cf.j_usage_dict()

    # Get a list of v family names
    j_gene_names = sorted(Recombination.j_gene_names())

    # Convert v usage dict into two lists for plotting
    for j_index, j_gene in enumerate(j_gene_names):
        if j_gene in j_usage_dict:
            usage.append(j_usage_dict[j_gene])
        else:
            usage.append(0)
        gene_index.append(j_index)

    # Generate the image
    ax.plot(gene_index, usage, '-', marker='o')

    # Axes labels and title
    ax.set_title('%s J Usage' % cf.sample)
    ax.set_xlabel('J Gene Family')
    ax.set_ylabel('Usage')

    xtickNames = plt.setp(ax, xticklabels=j_gene_names)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    ax.xaxis.set_ticks(range(len(j_gene_names)))

    canvas.print_png(response)


    return response

def v_usage_graph(request, clonofilter_id):
    '''
    Returns a PNG of v usage as a line graph
    '''
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    response = HttpResponse(content_type='image/png')
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)

    # variables which will contain data to be plotted
    usage = []
    family_index = []

    # Retreive the clonofilter
    cf = ClonoFilter.objects.get(id=clonofilter_id)

    # Get v usage data
    v_usage_dict = cf.v_usage_dict()

    # Get a list of v family names
    v_family_names = sorted(Recombination.v_family_names())

    # Convert v usage dict into two lists for plotting
    for v_index, v_family in enumerate(v_family_names):
        if v_family in v_usage_dict:
            usage.append(v_usage_dict[v_family])
        else:
            usage.append(0)
        family_index.append(v_index)

    # Generate the image
    ax.plot(family_index, usage, '-', marker='o')

    # Axes labels and title
    ax.set_title('%s V Usage' % cf.sample)
    ax.set_xlabel('V Gene Family')
    ax.set_ylabel('Usage')

    xtickNames = plt.setp(ax, xticklabels=v_family_names)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    ax.xaxis.set_ticks(range(len(v_family_names)))

    canvas.print_png(response)
    return response

def amino_acid_detail(request, amino_acid_id):
    '''
    View for displaying amino acid details. Shows other samples that share this amino acid sequence
    '''
    from clonotypes.models import AminoAcid
    amino_acid = AminoAcid.objects.get(id=amino_acid_id)
    context = {'amino_acid': amino_acid}
    return render(request, 'amino_acid_detail.html', context)


def all(request, sample_id):
    VALID_SORTS = {
            'copy': 'copy',
            'copyd': '-copy',
            'freq': 'raw_frequency',
            'freqd': '-raw_frequency',
            'ncopy': 'normalized_copy',
            'ncopyd': '-normalized_copy',
            'nfreq': 'normalized_frequency',
            'nfreqd': '-normalized_frequency',
            }
    try:
        sort_by = VALID_SORTS[request.GET.get('sort')]
    except:
        sort_by = VALID_SORTS['copyd']

    sample = Sample.objects.get(id=sample_id)
    clonotypes = Clonotype.objects.filter(sample=sample).order_by(sort_by)
    paginator = Paginator(clonotypes, 25)
    page = request.GET.get('page')

    try:
        clonotypes = paginator.page(page)
    except PageNotAnInteger:
        clonotypes = paginator.page(1)
        page = 1
    except EmptyPage:
        clonotypes = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {'sample': sample,
               'clonotypes': clonotypes,
               'valid_sorts': VALID_SORTS.keys(),
               'page': page,
              }
    return render(request, 'all.html', context)


def detail(request, clonotype_id):
    '''
    Displays a detailed view of a specific clonotype
    '''
    clonotype = Clonotype.objects.get(id=clonotype_id)
    sample = clonotype.sample
    context = {'clonotype': clonotype, 'sample': sample}
    return render(request, 'detail.html', context)


def bubble(request, clonofilter):
    ''' Takes in a filter and returns a bubble image generated by matplolib '''
#    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    import numpy as np
    from math import sqrt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import pylab

# Initialize required stuff for plotting
    response = HttpResponse(content_type='image/png')
#    fig = Figure()
#    ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)

# Initialize empty data variables
    x = []
    y = []
    color = []
    data = []
    area = []

    vj_counts_dict = clonofilter.vj_counts_dict()

    # Calculate the plotting area by finding the number of v's and j's
    v_list = sorted(Recombination.v_family_names())
    j_list = sorted(Recombination.j_gene_names())
    width = len(v_list)
    height = len(j_list)

    for v_index, v_family in enumerate(v_list):
        for j_index, j_gene in enumerate(j_list):
            x.append(v_index)
            y.append(j_index)
            if vj_counts_dict[v_family][j_gene]:
                color.append(vj_counts_dict[v_family][j_gene])
                data.append(vj_counts_dict[v_family][j_gene])
            else:
                color.append(0)
                data.append(0)

    # Normalize bubble areas
    if data:
        # Scales the area of a v-j junction by the size of the plot
        # and the maximum data value
        area_norm_factor = (2.0 / max(data)) * width * height
        area = [datapoint * area_norm_factor for datapoint in data]

# Use big outlines
#    sct = ax.scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
# Use small
    sct = ax.scatter(
        x, y, c=color, s=area, linewidths=1, edgecolor='lightgrey', alpha=.5)
#    sct.set_alpha(0.5)

# Labels, legends, titles etc
    # Set titles
    ax.set_title('%s V-J Usage Bubbleplot' % clonofilter.sample)
    ax.set_xlabel('V Gene Family')
    ax.set_ylabel('J Gene')
    # Add a grid
    ax.yaxis.grid(True, linestyle='-', which='both', color='lightgrey',
                  alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='both', color='lightgrey',
                  alpha=0.5)

    # Set the axes and plotting area
    ax.set_xlim(-1, width)
    ax.set_ylim(-1, height)
    xtickNames = plt.setp(ax, xticklabels=v_list)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    ax.xaxis.set_ticks(range(len(v_list)))
    ytickNames = plt.setp(ax, yticklabels=j_list)
    plt.setp(ytickNames, fontsize=9)
    ax.yaxis.set_ticks(range(len(j_list)))

    # Shrink the plot to make room for legends
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Draw the bubble size legend
    max_data = max(data)
    bubbles = []
    bubble_labels = []

    # Exponentially decreasing areas from max_data to max_data * 2^-8
    for bubble_area in [max_data * 1.35 ** (-exp) for exp in range(0, 15)]:
        # Determine marker size
        marker_size = sqrt(
            bubble_area / max_data * (len(j_list) * len(v_list * 2)))
        # Determine marker color. np.nextafter() is used because pylab.cm.jet
        # function is looking for a range from [0,1)
        marker_color = pylab.cm.jet(np.nextafter(bubble_area / max_data, -1))
        bubbles.append(plt.Line2D(range(1), range(1), marker='o', markersize=marker_size, color=marker_color, linewidth=0, markeredgecolor="lightgrey", alpha=0.5))
        bubble_labels.append('%g' % bubble_area)

    # Draw the legend
    #ax.legend(bubbles, bubble_labels, numpoints=1, loc='center left', bbox_to_anchor=(1.175, .5), prop={'size': 10})
    ax.legend(bubbles, bubble_labels, numpoints=1, loc='center left', bbox_to_anchor=(1.175, .5), labelspacing=1.5, prop={'size': 10}, title="Counts")

    # Colorbar
    # Make the colorbar a bit smaller
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    cb = plt.colorbar(sct, cax=cax)
    # Old way
#    cb = plt.colorbar(sct, ax=ax)
    cb.set_label("Counts")

    # Print the png and return
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
    ''' Given a clonofilter id, generate and return a spectratype
    plot. A spectratype plot shows the CDR3 length distributions
    of recombinations in a way that represents the total makeup
    of an immune repertoire sampling.
    '''
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from numpy import array

    response = HttpResponse(content_type='image/png')
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    cdr3_sums = array(clonofilter.cdr3_length_sum())
    ax.plot(cdr3_sums[:, 0].tolist(), cdr3_sums[:, 1].tolist(), '-')

    # Axes labels and title
    ax.set_title('%s Spectratype' % clonofilter.sample)
    ax.set_xlabel('CDR3 Length (Nucleotides)')
    ax.set_ylabel('Usage')

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
