from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from task_master.models import Task


class TaskViewSetTest(APITestCase):
    """
    Test cases for the TaskViewSet.
    """

    def setUp(self):
        """
        Set up test data for TaskViewSet tests.
        """
        # Create users
        self.user = User.objects.create_user(username='user', password='userpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        # Authenticate regular user
        self.client.login(username='user', password='userpassword')

        # Create tasks
        self.task = Task.objects.create(title='Sample Task', owner=self.user)
        self.other_user_task = Task.objects.create(title='Other User Task', owner=self.superuser)

        # URLs
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.id])
        self.other_task_url = reverse('task-detail', args=[self.other_user_task.id])

    def test_list_tasks(self):
        """
        Ensure we can retrieve a list of tasks owned by the authenticated user.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.task.title)

    def test_create_task(self):
        """
        Ensure we can create a new task and assign it to the authenticated user.
        """
        data = {'title': 'New Task'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)  # Two existing tasks + new one
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.owner, self.user)

    def test_retrieve_own_task(self):
        """
        Ensure we can retrieve a task owned by the authenticated user.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_retrieve_other_user_task(self):
        """
        Ensure we cannot retrieve a task owned by another user.
        """
        response = self.client.get(self.other_task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_task(self):
        """
        Ensure we can update a task owned by the authenticated user.
        """
        data = {'title': 'Updated Task', 'is_completed': True}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertTrue(self.task.is_completed)

    def test_update_other_user_task(self):
        """
        Ensure we cannot update a task owned by another user.
        """
        data = {'title': 'Hacked Task', 'is_completed': True}
        response = self.client.put(self.other_task_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_user_task.refresh_from_db()
        self.assertNotEqual(self.other_user_task.title, 'Hacked Task')

    def test_delete_own_task(self):
        """
        Ensure we can delete a task owned by the authenticated user.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check using all_objects to confirm it's soft-deleted
        self.assertTrue(Task.all_objects.filter(id=self.task.id, is_deleted=True).exists())

    def test_delete_other_user_task(self):
        """
        Ensure we cannot delete a task owned by another user.
        """
        response = self.client.delete(self.other_task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=self.other_user_task.id).exists())

    def test_superuser_can_access_all_tasks(self):
        """
        Ensure the superuser can access all tasks, regardless of the owner.
        """
        # Login as superuser
        self.client.logout()
        self.client.login(username='admin', password='adminpassword')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_complete_own_task(self):
        """
        Ensure we can mark our own task as completed.
        """
        complete_url = reverse('task-complete', args=[self.task.id])
        response = self.client.patch(complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_complete_other_user_task(self):
        """
        Ensure we cannot mark another user's task as completed.
        """
        complete_url = reverse('task-complete', args=[self.other_user_task.id])
        response = self.client.patch(complete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_user_task.refresh_from_db()
        self.assertFalse(self.other_user_task.is_completed)