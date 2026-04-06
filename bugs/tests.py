from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from bugs.models import Bug

UserModel = get_user_model()

class BugFilterTest(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', password='password123')
        self.user2 = UserModel.objects.create_user(username='user2', password='password123')
        
        # Profiles are created by signals
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile
        
        self.bug1 = Bug.objects.create(
            name='Bug 1', 
            type=Bug.BugTypeChoices.FIRE, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.profile1,
            image_url='http://example.com/bug1.jpg',
            description='Test bug 1 description'
        )
        self.bug2 = Bug.objects.create(
            name='Bug 2', 
            type=Bug.BugTypeChoices.WATER, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.profile2,
            image_url='http://example.com/bug2.jpg',
            description='Test bug 2 description'
        )

    def test_bug_list_all(self):
        response = self.client.get(reverse('bugs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 2')

    def test_bug_list_filter_my_bugs(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('bugs:list'), {'filter': 'my_bugs'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertNotContains(response, 'Bug 2')

    def test_bug_list_filter_all(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('bugs:list'), {'filter': 'all'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 2')

    def test_bug_list_filter_my_bugs_anonymous(self):
        # Anonymous user should see all bugs even if filter=my_bugs is passed
        # Because in code we check self.request.user.is_authenticated
        response = self.client.get(reverse('bugs:list'), {'filter': 'my_bugs'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 2')
