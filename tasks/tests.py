from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task


class TaskTests(TestCase):
    """Basic tests for the Tasks module — demonstrates QA coverage."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.today = timezone.localdate()

    def test_task_list_page_loads(self):
        """The tasks list page should return HTTP 200."""
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        """A task can be created via POST and the DB count increases."""
        self.client.post('/tasks/add/', {
            'title': 'Write FYP report',
            'date': self.today.isoformat(),
            'priority': 'high',
        }, follow=True)
        self.assertEqual(Task.objects.filter(user=self.user, title='Write FYP report').count(), 1)

    def test_task_defaults_to_not_completed(self):
        """A newly created task should not be completed by default."""
        Task.objects.create(user=self.user, title='Test task', date=self.today)
        task = Task.objects.get(title='Test task')
        self.assertFalse(task.completed)

    def test_dashboard_redirects_when_not_logged_in(self):
        """Unauthenticated users are redirected away from the dashboard."""
        self.client.logout()
        response = self.client.get('/dashboard/')
        self.assertNotEqual(response.status_code, 200)  # Should redirect

    def test_task_list_requires_login(self):
        """Task list should redirect unauthenticated users."""
        self.client.logout()
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)
