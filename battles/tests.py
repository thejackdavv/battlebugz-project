from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from bugs.models import Bug
from battles.models import Battle
from locations.models import Location

UserModel = get_user_model()

class BattleFilterTest(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', password='password123')
        self.user2 = UserModel.objects.create_user(username='user2', password='password123')
        
        self.loc = Location.objects.create(
            name='Arena', 
            type=Location.LocationTypeChoices.EARTH,
            image_url='http://example.com/arena.jpg',
            description='Fighting ground'
        )
        
        self.bug1 = Bug.objects.create(
            name='Bug 1', 
            type=Bug.BugTypeChoices.FIRE, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.user1.profile,
            image_url='http://example.com/bug1.jpg',
            description='User 1 Bug'
        )
        self.bug2 = Bug.objects.create(
            name='Bug 2', 
            type=Bug.BugTypeChoices.WATER, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.user2.profile,
            image_url='http://example.com/bug2.jpg',
            description='User 2 Bug'
        )
        
        self.battle1 = Battle.objects.create(
            attacker=self.bug1,
            defender=self.bug2,
            location=self.loc,
            winner=self.bug1,
            rounds=3
        )

        # Another user's battle
        self.user3 = UserModel.objects.create_user(username='user3', password='password123')
        self.bug3 = Bug.objects.create(
            name='Bug 3', 
            type=Bug.BugTypeChoices.GRASS, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.user3.profile,
            image_url='http://example.com/bug3.jpg',
            description='User 3 Bug'
        )
        self.bug4 = Bug.objects.create(
            name='Bug 4', 
            type=Bug.BugTypeChoices.EARTH, 
            max_health_points=100, 
            armor=10, 
            strength=10, 
            mobility=10, 
            healing_factor=10, 
            owner=self.user3.profile,
            image_url='http://example.com/bug4.jpg',
            description='User 3 Bug 2'
        )
        self.battle2 = Battle.objects.create(
            attacker=self.bug3,
            defender=self.bug4,
            location=self.loc,
            winner=self.bug3,
            rounds=2
        )

    def test_battle_list_all(self):
        response = self.client.get(reverse('battles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 3')

    def test_battle_list_filter_my_battles(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('battles:list'), {'filter': 'my_battles'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertNotContains(response, 'Bug 3')

    def test_battle_list_filter_all(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('battles:list'), {'filter': 'all'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 3')

    def test_battle_list_filter_my_battles_anonymous(self):
        response = self.client.get(reverse('battles:list'), {'filter': 'my_battles'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug 1')
        self.assertContains(response, 'Bug 3')
