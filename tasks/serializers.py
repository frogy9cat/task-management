from rest_framework import serializers
from .models import Task, Comment
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},

            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'read_only': True},
        }

    def validate_due_date(self, value):
        # Проверяем, что дата выполнения не в прошлом
        if value < date.today():
            raise serializers.ValidationError("Дата выполнения не может быть в прошлом.")
        return value
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']