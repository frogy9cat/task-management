from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'due_date'] # Поля для фильтрации
    
    @extend_schema(
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, location=OpenApiParameter.QUERY, description="Filter by status (Pending, In Progress, Completed)"),
            OpenApiParameter("due_date", OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description="Filter by due date (YYYY-MM-DD)")
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user) # Пользователь видит только свои задачи
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Задачу создаёт авторизованный пользователь



class CommentViewSet(viewsets.ModelViewSet):
    queryset =  Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
            parameters=[
                OpenApiParameter("task_id", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Filter comments by task id")
            ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if task_id:
            return Comment.objects.filter(task__id=task_id)
        return super().get_queryset()   # Возврат комментариев, связанных с конкретным объектом Task

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Автоматически добавляем пользователя, создавшего комментарий