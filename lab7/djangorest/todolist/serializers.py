from rest_framework import serializers
from .models import Task,Tasklist, Tag, Share
from django.contrib.auth.models import User
# from django.contrib import auth

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password','email')

class ShareSerializer2(serializers.ModelSerializer):
    user = serializers.CharField(max_length=100)

    class Meta:
        model = Tasklist
        fields = ('user',)


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    class Meta:
        model = Task
        fields = ('id', 'name','owner','tags_string', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority', 'tasklist_id')
        read_only_fields = ('date_created', 'date_modified')



class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True, read_only = True)
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Tasklist
        fields = ('id','name','owner', 'tasks')

class ShareSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    tasklist = serializers.ReadOnlyField(source='tasklist.id', read_only = True)
    owner = serializers.ReadOnlyField(source='owner.username', read_only = True)
    #username = serializers.CharField(write_only=True)
    class Meta:
        model = Share
        fields = ('username','tasklist','permission','owner')

