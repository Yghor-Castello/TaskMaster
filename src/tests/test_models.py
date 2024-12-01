from django.test import TestCase
from django.contrib.auth.models import User

from task_master.models import Task


class TaskModelTest(TestCase):
    """
    Test cases for the Task model.
    """

    def setUp(self):
        """
        Set up the initial test data.
        """
        # Create users
        self.user = User.objects.create_user(username='user', password='userpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        # Create tasks
        self.task = Task.objects.create(title='Sample Task', owner=self.user)
        self.completed_task = Task.objects.create(title='Completed Task', is_completed=True, owner=self.user)
        self.deleted_task = Task.objects.create(title='Deleted Task', is_deleted=True, owner=self.user)

    def test_task_creation(self):
        """
        Ensure that a Task instance is created successfully.
        """
        self.assertEqual(self.task.title, 'Sample Task')
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.owner, self.user)

    def test_task_str_method(self):
        """
        Ensure the string representation of the Task model returns the title.
        """
        self.assertEqual(str(self.task), 'Sample Task')

    def test_task_soft_delete(self):
        """
        Ensure that a Task instance is soft-deleted instead of being removed from the database.
        """
        self.task.delete()
        self.assertTrue(self.task.is_deleted)

        # Ensure the task is still in the database
        self.assertTrue(Task.all_objects.filter(id=self.task.id).exists())
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_filtering_for_regular_user(self):
        """
        Ensure that only tasks owned by the user are returned for regular users.
        """
        user_tasks = Task.objects.filter(owner=self.user)
        self.assertIn(self.task, user_tasks)
        self.assertNotIn(self.deleted_task, user_tasks)

    def test_task_filtering_for_superuser(self):
        """
        Ensure that the superuser can access all tasks, including soft-deleted ones.
        """
        all_tasks = Task.all_objects.all()
        self.assertIn(self.task, all_tasks)
        self.assertIn(self.deleted_task, all_tasks)
        self.assertIn(self.completed_task, all_tasks)

    def test_task_completion(self):
        """
        Ensure that a Task can be marked as completed.
        """
        self.task.is_completed = True
        self.task.save()
        self.assertTrue(self.task.is_completed)

    def test_deleted_task_access(self):
        """
        Ensure that soft-deleted tasks are not accessible in the default queryset.
        """
        visible_tasks = Task.objects.all()
        self.assertNotIn(self.deleted_task, visible_tasks)

        all_tasks = Task.all_objects.all()
        self.assertIn(self.deleted_task, all_tasks)