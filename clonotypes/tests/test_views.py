from django.test import TestCase
#from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype, ClonoFilter, AminoAcid, Recombination
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient, make_fake_patient_with_3_clonotypes
from mock import MagicMock, patch, call
from clonotypes.views import all, detail, bubble, bubble_default, spectratype, spectratype_default, amino_acid_detail, v_usage_graph, j_usage_graph, functionality_graph, domination_graph
from test_utils.factories import render_echo, FakeRequestFactory, ClonotypeFactory


class RecombinationViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''
    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
#        make_fake_patient()
        ClonotypeFactory()
        self.s = Sample.objects.get()
        self.recombination = Recombination.objects.get()

    def test_recombination_detail_view_uses_amino_acid_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load clonotype_tags %}{% recombination_tag recombination %}')
        c = Context({'recombination': self.recombination})
        t.render(c)
        self.assertEqual(c['recombination'], self.recombination)


class AminoAcidViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient()
        self.s = Sample.objects.get()
        self.aa = AminoAcid.objects.get()

    def tearDown(self):
        self.renderPatch.stop()

    def test_amino_acid_detail_view_passes_amino_acid_to_template(self):
        mock_response = amino_acid_detail(self.request, self.aa.id)
        self.assertEqual(self.aa, mock_response.get('amino_acid'))

    def test_amino_acid_detail_view_uses_amino_acid_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load clonotype_tags %}{% amino_acid_tag amino_acid %}')
        c = Context({'amino_acid': self.aa})
        t.render(c)
        self.assertEqual(c['amino_acid'], self.aa)



class AminoAcidViewIntegrationTest(TestCase):
    ''' Integration tests for all amino acids views
    '''
    def setUp(self):
        make_fake_patient()
        self.fake_sample = Sample.objects.get()
        self.aa = AminoAcid.objects.get()

    def test_amino_acid_detail_view_contains_links_to_samples(self):
        pass

    def test_amino_acid_detail_view_contains_links_to_clonotype(self):
        response = self.client.get(
            reverse('clonotypes.views.amino_acid_detail', args=[self.aa.id]))

        for recombination in self.aa.recombination_set.all():
            for clonotype in recombination.clonotype_set.all():
                self.assertIn(reverse('clonotypes.views.detail', args=[clonotype.id]),
                        response.content)

    def test_amino_acid_detail_view_uses_amino_acid_template(self):
        response = self.client.get(
            reverse('clonotypes.views.amino_acid_detail', args=[self.aa.id]))
        self.assertTemplateUsed(response, 'amino_acid_detail.html')

    def test_amino_acid_detail_view_shows_amino_acid_sequence(self):
        from django.utils.html import strip_tags
        response = self.client.get(
            reverse('clonotypes.views.amino_acid_detail', args=[self.aa.id]))
        self.assertIn(self.aa.sequence, strip_tags(response.content))

    def test_amino_acid_detail_view_shows_all_recombinations(self):
        from django.utils.html import strip_tags
        response = self.client.get(
            reverse('clonotypes.views.amino_acid_detail', args=[self.aa.id]))
        recombinations = self.aa.recombination_set.all()
        for recombination in recombinations:
            self.assertIn(recombination.nucleotide, strip_tags(response.content))


class ClonotypesViewUnitTest(TestCase):
    ''' ClonotypesViewTest mocks out the Django call stack for faster
    unit tests. This is useful for testing the view and making sure objects
    exist in the context and that the correct templates are being used.
    This also increases the speed of the unittesting
    '''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient_with_3_clonotypes()

    def tearDown(self):
        self.renderPatch.stop()

    def test_all_clonotypes_passes_page_number_to_template(self):
        sample = Sample.objects.get()
        self.request.GET={'page': 1}
        mock_response = all(self.request, sample.id)
        self.assertEqual(1, mock_response.get('page'))

    def test_all_clonotypes_passes_valid_sorts_to_template(self):
        valid_sorts = ['freq', 'freqd', 'countd', 'count']
        sample = Sample.objects.get()
        mock_response = all(self.request, sample.id)
        self.assertEqual(set(valid_sorts), set(mock_response.get('valid_sorts')))

    def test_all_clonotypes_view_can_be_sorted_by_copy_freq_or_norm_freq_norm_copy(self):
        sample = Sample.objects.get()

        # sort by freq ascending
        self.request.GET = {'sort': 'freq'}
        mock_response = all(self.request, sample.id)
        sorted_clonotypes = Clonotype.objects.filter(sample=sample).order_by('frequency')
        self.assertEqual(list(sorted_clonotypes),
                         list(mock_response.get('clonotypes')))

        # sort by freq descending
        self.request.GET = {'sort': 'freqd'}
        mock_response = all(self.request, sample.id)
        sorted_clonotypes = Clonotype.objects.filter(sample=sample).order_by('-frequency')
        self.assertEqual(list(sorted_clonotypes),
                         list(mock_response.get('clonotypes')))

        # sort by count ascending
        self.request.GET = {'sort': 'count'}
        mock_response = all(self.request, sample.id)
        sorted_clonotypes = Clonotype.objects.filter(sample=sample).order_by('count')
        self.assertEqual(list(sorted_clonotypes),
                         list(mock_response.get('clonotypes')))

        # sort by count descending
        self.request.GET = {'sort': 'countd'}
        mock_response = all(self.request, sample.id)
        sorted_clonotypes = Clonotype.objects.filter(sample=sample).order_by('-count')
        self.assertEqual(list(sorted_clonotypes),
                         list(mock_response.get('clonotypes')))

    def test_all_clonotypes_view_is_sorted_by_count_by_default(self):
        sample = Sample.objects.get()
        mock_response = all(self.request, sample.id)
        sorted_clonotypes = Clonotype.objects.filter(sample=sample).order_by('-count')
        self.assertEqual(list(sorted_clonotypes),
                         list(mock_response.get('clonotypes')))

    def test_clonotypes_all_view_returns_paginator_object(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        self.assertEqual('Page',
                         mock_response.get('clonotypes').__class__.__name__)

    def test_clonotypes_all_view_returns_last_page_if_EmptyPage_is_thrown(self):
        from django.core.paginator import Paginator
        fake_request = FakeRequestFactory(GET={'page': 99999})
        fake_sample = Sample.objects.get()
        clonotypes = Clonotype.objects.filter(sample=fake_sample)
        paginator = Paginator(clonotypes, 2)
        mock_response = all(fake_request, fake_sample.id)
        self.assertQuerysetEqual(paginator.page(2).object_list,
                                 map(repr,
                                     mock_response.get(
                                         'clonotypes').object_list),
                                 ordered=False)

    def test_clonotypes_all_view_returns_first_page_if_PageNotAnInteger_is_thrown(self):
        from django.core.paginator import Paginator
        fake_request = FakeRequestFactory(GET={'page': 'notAnInt'})
        fake_sample = Sample.objects.get()
        clonotypes = Clonotype.objects.filter(sample=fake_sample)
        paginator = Paginator(clonotypes, 2)
        mock_response = all(fake_request, fake_sample.id)
        self.assertQuerysetEqual(paginator.page(1).object_list,
                                 map(repr,
                                     mock_response.get(
                                         'clonotypes').object_list),
                                 ordered=False)

    def test_clonotypes_all_view_calls_paginator_on_clonotypes(self):
        # Patch with a mock and then track the calls on the mock
        fake_sample = Sample.objects.get()
        mock = MagicMock()
        with patch('clonotypes.views.Paginator', return_value=mock):
            all(self.request, fake_sample.id)
            mock.page.assert_called_with(None)

    def test_clonotypes_all_view_uses_all_template(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        self.assertEqual(mock_response.get('template'), 'all.html')

    def test_clonotypes_all_view_passes_clonotypes_to_template(self):
        fake_sample = Sample.objects.get()
        fake_clonotypes = Clonotype.objects.filter(sample=fake_sample)

        mock_response = all(self.request, fake_sample.id)
        clonotypes_in_context = mock_response.get('clonotypes')

        self.assertQuerysetEqual(fake_clonotypes,
                                 map(repr, clonotypes_in_context),
                                 ordered=False)

    def test_clonotypes_all_view_passes_sample_to_template(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        sample_in_context = mock_response.get('sample')
        self.assertEqual(sample_in_context, fake_sample)

    def test_clonotype_detail_view_returns_clonotype_in_context(self):
        clonotype = Clonotype.objects.all()[:1].get()
        mock_response = detail(self.request, clonotype.id)
        self.assertEqual(clonotype, mock_response.get('clonotype'))

    def test_detail_view_has_sample_in_context(self):
        clonotype = Clonotype.objects.all()[:1].get()
        sample = clonotype.sample
        mock_response = detail(self.request, clonotype.id)
        self.assertEqual(sample, mock_response.get('sample'))


class ClonotypesAllViewIntegrationTest(TestCase):
    ''' Integration tests for all clonotypes view
    '''
    def setUp(self):
        make_fake_patient()
        self.fake_sample = Sample.objects.get()
        self.response = self.client.get(
            reverse('clonotypes.views.all', args=[self.fake_sample.id]))

    def test_clonotypes_all_view_has_links_to_sort_methods(self):
        valid_sorts = ['count',
                       'countd',
                       'freq',
                       'freqd',
                       ]

        for sort in valid_sorts:
            self.assertIn('%s?sort=%s' %
                          (reverse('clonotypes.views.all', args=[self.fake_sample.id]), sort),
                          self.response.content)

    def test_clonotypes_all_view_shows_patient_name(self):
        self.assertIn('test patient', self.response.content)

    def test_clonotypes_all_view_contains_pagination_page_information(self):
        self.assertIn('Page 1 of 1', self.response.content)

    def test_all_view_has_links_to_detail_view(self):
        clonotype = Clonotype.objects.all()[:1].get()
        self.assertIn('Details', self.response.content)
        self.assertIn(reverse('clonotypes.views.detail', args=[clonotype.id]),
                      self.response.content)


class ClonotypesDetailViewIntegrationTest(TestCase):
    ''' Integration tests for clonotype detail view '''
    def setUp(self):
        make_fake_patient()
        self.fake_sample = Sample.objects.get()
        self.clonotype = Clonotype.objects.all()[:1].get()
        self.response = self.client.get(
            reverse('clonotypes.views.detail', args=[self.clonotype.id]))

    def test_clonotype_detail_view_formats_nucleotide_sequence_with_spans(self):
        clonotype = Clonotype.objects.get()
        self.assertIn('<span class="v_gene"', self.response.content)
        self.assertIn('<span class="j_gene"', self.response.content)

    def test_detail_view_lists_all_info(self):
        self.assertIn('nucleotide', self.response.content)

    def test_detail_view_shows_sample_name(self):
        self.assertIn(str(self.fake_sample), self.response.content)

    def test_detail_view_uses_clonotype_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load clonotype_tags %}{% clonotype_tag clonotype %}')
        c = Context({'clonotype': self.clonotype})
        t.render(c)
        self.assertEqual(c['clonotype'], self.clonotype)


def bubble_patch(request, clonofilter):
    ''' Mock method used to patch out image rendering method'''
    return (request, clonofilter)


class ClonotypesImagesTest(TestCase):
    ''' For testing creation of images '''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient_with_3_clonotypes()

    def tearDown(self):
        self.renderPatch.stop()

    def test_domaintion_graph_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        clonofilter.save()
        response = domination_graph(self.request, clonofilter.id)
        self.assertEqual('image/png', response['content-type'])

    def test_functionality_graph_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        clonofilter.save()
        response = functionality_graph(self.request, clonofilter.id)
        self.assertEqual('image/png', response['content-type'])

    def test_j_usage_graph_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        clonofilter.save()
        response = j_usage_graph(self.request, clonofilter.id)
        self.assertEqual('image/png', response['content-type'])

    def test_v_usage_graph_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        clonofilter.save()
        response = v_usage_graph(self.request, clonofilter.id)
        self.assertEqual('image/png', response['content-type'])

    def test_spectratype_default_applies_clonofilter_passed_in_through_get(self):
        s = Sample.objects.get()
        cf = ClonoFilter(sample=s)
        cf.save()
        self.request = FakeRequestFactory(GET={'clonofilter': cf.id})
        with patch('clonotypes.views.spectratype', bubble_patch):
            (request_echo,
             clonofilter_echo) = spectratype_default(self.request, s.id)
            self.assertEqual(cf.id, clonofilter_echo.id)
            self.assertEqual(cf, clonofilter_echo)

    def test_bubble_default_applies_clonofilter_passed_in_through_get(self):
        s = Sample.objects.get()
        cf = ClonoFilter(sample=s)
        cf.save()
        self.request = FakeRequestFactory(GET={'clonofilter': cf.id})
        with patch('clonotypes.views.bubble', bubble_patch):
            (request_echo, clonofilter_echo) = bubble_default(
                self.request, s.id)
            self.assertEqual(cf.id, clonofilter_echo.id)
            self.assertEqual(cf, clonofilter_echo)

    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg.print_png')
    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg')
    def DONTtest_bubble_prints_png_to_reponse(self, mock_canvas, mock_png):
        bubble(self.request, MagicMock())
        #        self.assertTrue(mock_canvas.print_png.called)
        # This is not the right way to test this
        self.assertTrue(mock_canvas.mock_calls[1].called)

    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg.print_png')
    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg')
    def DONTtest_bubble_creates_a_new_canvas(self, mock_canvas, mock_png):
        bubble(self.request, MagicMock())
        self.assertTrue(mock_canvas.called)

    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg.print_png')
    @patch('matplotlib.figure.Figure')
    def DONTtest_bubble_makes_a_subplot(self, mock_canvas, mock_png):
        bubble(self.request, MagicMock())
        self.assertIn("add_subplot()",
                      str(mock_canvas.mock_calls))

    @patch('matplotlib.backends.backend_agg.FigureCanvasAgg.print_png')
    @patch('matplotlib.figure.Figure')
    def DONTtest_bubble_makes_a_figure(self, mock_figure, mock_canvas):
        bubble(self.request, MagicMock())
        self.assertTrue(mock_figure.called)

    def test_bubble_default_png_is_open_to_world(self):
        s = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.bubble_default', args=[s.id]))
        self.assertEqual('image/png', response['content-type'])

    def test_bubble_default_png_uses_an_empty_filter(self):
        s = Sample.objects.get()
        with patch('clonotypes.views.bubble', bubble_patch):
            (request, clonofilter) = bubble_default(self.request, s.id)
            self.assertEqual(ClonoFilter(), clonofilter)

    def test_bubble_default_creates_a_filter_with_sample(self):
        s = Sample.objects.get()
        with patch('clonotypes.views.bubble', bubble_patch):
            (request, clonofilter) = bubble_default(self.request, s.id)
            self.assertEqual(s, clonofilter.sample)

    def test_bubble_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        response = bubble(self.request, clonofilter)
        self.assertEqual('image/png', response['content-type'])

    def DONTtest_bubble_takes_in_clonotype_queryset_as_arguement(self):
        mock_response = bubble(self.request, MagicMock())
        self.assertEqual('image/png', mock_response['content-type'])

    def test_spectratype_returns_a_png(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        response = spectratype(self.request, clonofilter)
        self.assertEqual('image/png', response['content-type'])

    def test_spectratype_default_url_resolves_and_returns_a_png(self):
        s = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.spectratype_default', args=[s.id]))
        self.assertEqual('image/png', response['content-type'])


class ClonotypesImagesIntegrationTests(TestCase):
    def setUp(self):
        make_fake_patient_with_3_clonotypes()

    def test_j_usage_has_a_valid_url(self):
        s = Sample.objects.get()
        clonofilter = ClonoFilter(sample=s)
        response = reverse('clonotypes.views.j_usage_graph', args=[s.id])
        def test_v_usage_has_a_valid_url(self):
            s = Sample.objects.get()
            clonofilter = ClonoFilter(sample=s)
            response = reverse('clonotypes.views.v_usage_graph', args=[s.id])
