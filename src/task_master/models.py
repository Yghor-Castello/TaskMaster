from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for created, updated timestamps,
    and soft delete functionality.

    Fields:
        created_at (DateTimeField): The datetime when the object was created.
        updated_at (DateTimeField): The datetime when the object was last updated.
        is_deleted (BooleanField): Indicates whether the object is soft-deleted.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Overrides the default delete method to implement soft delete.

        Instead of removing the object from the database, it sets `is_deleted` to True.
        """
        self.is_deleted = True
        self.save()


class TaskManager(models.Manager):
    """
    Manager that filters out soft-deleted tasks.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class TaskAllObjectsManager(models.Manager):
    """
    Manager that includes soft-deleted tasks.
    """
    def get_queryset(self):
        return super().get_queryset()


class Task(BaseModel):
    """
    Represents a task in the to-do list.

    Fields:
        title (CharField): The title of the task.
        is_completed (BooleanField): Indicates whether the task is completed.
        owner (ForeignKey): The user who created the task.
    """
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    # Add the custom managers
    objects = TaskManager()
    all_objects = TaskAllObjectsManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']