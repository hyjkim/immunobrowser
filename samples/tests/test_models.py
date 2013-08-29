from django.test import TestCase
#from datetime import date
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
from test_utils.factories import UserFactory, SampleFactory
from samples.models import Sample
#from patients.models import Patient


class SampleModelTest(TestCase):

    def test_search_finds_samples_where_any_field_matches_a_keyword(self):
        SampleFactory(cell_type="cd4+")
        SampleFactory(cell_type="cd8+")
        terms = ['cd4+']
        self.assertEqual(map(repr, Sample.objects.search(terms)),
                map(repr,Sample.objects.filter(cell_type="cd4+")))

    def test_public_and_private_sample_are_visible_to_private_query_when_user_is_specified(self):
        user = UserFactory()
        SampleFactory(private=True, users=[user])
        SampleFactory(private=False)
        self.assertEqual(2, len(Sample.objects.private(user)))

    def test_private_sample_is_visible_to_private_query_when_user_is_specified(self):
        user = UserFactory()
        SampleFactory(private=True, users=[user])
        self.assertEqual(1, len(Sample.objects.private(user)))

    def test_a_private_sample_is_not_visible_to_public_query(self):
        user = UserFactory()
        SampleFactory(private=True, users=[user])
        self.assertEqual(0, len(Sample.objects.public()))

    def test_complex_queries_are_chainable_with_custom_queryset(self):
        SampleFactory(private=False)
        self.assertEqual(map(repr, Sample.objects.public()),
                         map(repr, Sample.objects.all().public()))

    def test_SampleManager_uses_custom_queryset(self):
        from samples.models import SampleQuerySet
        self.assertIsInstance(Sample.objects.all(), SampleQuerySet)

    def test_sample_has_custom_manager(self):
        from samples.models import SampleManager
        self.assertIsInstance(Sample.objects, SampleManager)

    def test_sample_contains_a_list_of_approved_users(self):
        u = UserFactory()
        s = SampleFactory()
        s.users.add(u)
        self.assertTrue(len(Sample.objects.filter(users=u)))

    def test_sample_can_be_private(self):
        s = SampleFactory(private=True)
        self.assertEqual(s.private, True)

    def test_create_samples_for_a_patient(self):
        make_fake_patient_with_3_clonotypes()
        # Try retreiving the sample from the database
        s = Sample.objects.get()
        all_samples = Sample.objects.all()
        self.assertEqual(len(all_samples), 1)

        # Check to see if the attributes have been saved

        # Make sure the sample is linked to the patient
        self.assertEqual(all_samples[0].patient, s.patient)

    def test_samples_have_a_draw_date(self):
        make_fake_patient_with_3_clonotypes()
        # Retrieve the sample from the db
        all_samples = Sample.objects.all()
        # make sure the draw dates are equal
        self.assertTrue(all_samples[0].draw_date)
