from django.test import TestCase
from django.urls import reverse
from locations.models import Location

class LocationFilterTest(TestCase):
    def setUp(self):
        Location.objects.create(
            name='Fire Peak', 
            type=Location.LocationTypeChoices.FIRE,
            image_url='http://example.com/fire.jpg',
            description='Hot place'
        )
        Location.objects.create(
            name='Water Cave', 
            type=Location.LocationTypeChoices.WATER,
            image_url='http://example.com/water.jpg',
            description='Wet place'
        )

    def test_location_list_all(self):
        response = self.client.get(reverse('locations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fire Peak')
        self.assertContains(response, 'Water Cave')

    def test_location_list_filter_fire(self):
        response = self.client.get(reverse('locations:list'), {'type': 'FIRE'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fire Peak')
        self.assertNotContains(response, 'Water Cave')

    def test_location_list_filter_water(self):
        response = self.client.get(reverse('locations:list'), {'type': 'WATER'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Water Cave')
        self.assertNotContains(response, 'Fire Peak')
