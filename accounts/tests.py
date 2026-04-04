from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword')
        self.password_change_url = reverse('accounts:password-change-view')
        self.password_change_done_url = reverse('accounts:password_change_done')

    def test_password_change_requires_login(self):
        response = self.client.get(self.password_change_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.password_change_url}')

    def test_password_change_view_accessible_after_login(self):
        self.client.login(username='testuser', password='oldpassword')
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    def test_password_change_success(self):
        self.client.login(username='testuser', password='oldpassword')
        data = {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(self.password_change_url, data)
        self.assertRedirects(response, self.password_change_done_url)
        
        # Verify password actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_change_fail_same_password(self):
        self.client.login(username='testuser', password='oldpassword')
        data = {
            'old_password': 'oldpassword',
            'new_password1': 'oldpassword',
            'new_password2': 'oldpassword',
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("Your new password must be different from your old password.", form.non_field_errors())

    def test_password_change_done_view(self):
        self.client.login(username='testuser', password='oldpassword')
        response = self.client.get(self.password_change_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_done.html')

