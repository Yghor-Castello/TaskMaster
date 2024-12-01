from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing tasks.

    Provides:
        - List all tasks (GET /tasks/) owned by the authenticated user or all tasks if the user is a superuser.
        - Retrieve a specific task (GET /tasks/<id>/) if owned by the user or if the user is a superuser.
        - Create a new task (POST /tasks/) and assign ownership to the user.
        - Update an existing task (PUT /tasks/<id>/ or PATCH /tasks/<id>/) if owned by the user or if the user is a superuser.
        - Soft delete a task (DELETE /tasks/<id>/) if owned by the user or if the user is a superuser.
        - Mark a task as completed (PATCH /tasks/<id>/complete/) if owned by the user or if the user is a superuser.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    def get_queryset(self):
        """
        Return tasks owned by the authenticated user, or all tasks if the user is a superuser.

        Query parameters:
            include_deleted (bool): If true, include soft-deleted tasks.

        Returns:
            QuerySet: Filtered queryset based on the query parameter.
        """
        include_deleted = self.request.query_params.get('include_deleted', 'false').lower() == 'true'

        if self.request.user.is_superuser:
            queryset = Task.all_objects.all() if include_deleted else Task.objects.filter(is_deleted=False)
        else:
            queryset = Task.all_objects.filter(owner=self.request.user) if include_deleted else Task.objects.filter(owner=self.request.user, is_deleted=False)

        return queryset.order_by('-created_at')


    def perform_create(self, serializer):
        """
        Set the owner of the task to the currently authenticated user upon creation.
        """
        serializer.save(owner=self.request.user)


    def perform_update(self, serializer):
        """
        Prevent changing the owner of the task during update.
        """
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """
        Marks a task as completed if it is owned by the authenticated user or the user is a superuser.

        Args:
            request: The HTTP request object.
            pk: The primary key of the task.

        Returns:
            Response: The updated task or an error message if not found or unauthorized.
        """
        try:
            task = self.get_object()

            if task.is_completed:
                return Response(
                    {"message": "Task is already completed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            task.is_completed = True
            task.save()
            return Response(
                {"message": "Task marked as completed.", "task": TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)