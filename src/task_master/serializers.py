from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer converts Task model instances to JSON format and vice versa.
    It includes all fields in the Task model by default.

    Attributes:
        model (Task): The model being serialized.
        fields (str): Specifies that all fields in the Task model are included in the serialization.
    """
    owner = serializers.ReadOnlyField(source='owner.id')
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_completed', 'is_deleted', 'created_at', 'updated_at', 'owner']