from django.contrib.auth.models import User
from django.test import TestCase

from task_master.models import Task
from task_master.serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    """
    Test cases for the TaskSerializer.
    """

    def setUp(self):
        """
        Set up test data for the serializer tests.
        """
        # Create users
        self.user = User.objects.create_user(username='user', password='userpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        # Create task instance
        self.task_data = {'title': 'Sample Task', 'is_completed': False, 'owner': self.user}
        self.task = Task.objects.create(**self.task_data)
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_contains_expected_fields(self):
        """
        Ensure the serializer includes the expected fields.
        """
        data = self.serializer.data
        expected_fields = ['id', 'title', 'is_completed', 'is_deleted', 'created_at', 'updated_at', 'owner']
        self.assertCountEqual(data.keys(), expected_fields)

    def test_serializer_field_content(self):
        """
        Ensure the serializer data matches the Task instance.
        """
        data = self.serializer.data
        self.assertEqual(data['title'], self.task.title)
        self.assertEqual(data['is_completed'], self.task.is_completed)
        self.assertEqual(data['is_deleted'], self.task.is_deleted)
        self.assertEqual(data['owner'], self.task.owner.id)

    def test_serializer_create_task(self):
        """
        Ensure the serializer can create a Task instance.
        """
        task_data = {'title': 'New Task', 'is_completed': False}
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save(owner=self.user)  # Passa explicitamente o owner
        self.assertEqual(task.title, task_data['title'])
        self.assertFalse(task.is_completed)
        self.assertEqual(task.owner, self.user)

    def test_serializer_update_task(self):
        """
        Ensure the serializer can update a Task instance.
        """
        updated_data = {'title': 'Updated Task', 'is_completed': True}
        serializer = TaskSerializer(instance=self.task, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()
        self.assertEqual(updated_task.title, updated_data['title'])
        self.assertTrue(updated_task.is_completed)

    def test_serializer_with_superuser(self):
        """
        Ensure the serializer handles tasks owned by the superuser.
        """
        superuser_task_data = {'title': 'Superuser Task', 'is_completed': False, 'owner': self.superuser}
        superuser_task = Task.objects.create(**superuser_task_data)
        serializer = TaskSerializer(instance=superuser_task)
        data = serializer.data
        self.assertEqual(data['title'], superuser_task.title)
        self.assertEqual(data['owner'], self.superuser.id)