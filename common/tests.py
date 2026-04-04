from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class NavbarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.url = reverse('common:welcome')

    def test_admin_link_not_visible_to_regular_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Admin Panel')

    def test_admin_link_visible_to_staff_user(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'Admin Panel')
        self.assertContains(response, reverse('admin:index'))
