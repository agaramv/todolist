from collections import UserDict
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .serializers import TaskListSerializer, UserSerializer
from .models import TaskList
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from tasklist import serializers

# API Overview

@api_view(['GET'])
def apiOverview(request):
  api_urls = {
    'Task List' : '/task/all',
    'Task-Retrieve': '/task/view/<str:pk>',
    'Task-Create': '/task/create',
    'Task-Update': '/task/update/<str:pk>',
    'Task-Delete': '/task/delete/<str:pk>',
    'Task_CRUD': '/task/<str:pk>',
    'User-List': '/user/',
    'User-Retrieve': '/user/<int:pk>'
  }
  return Response(api_urls)

@api_view(['GET'])
def taskList(request):
  taskList = TaskList.objects.all()
  serializer = TaskListSerializer(taskList, many = True)
  return Response(serializer.data)

"""
This Function going to display Detailed view of one perticuler task with the help of pk.
"""
@api_view(['GET'])
def taskView(request, id):
  print(request," ID: ",id)
  task = TaskList.objects.get(id=id)
  serializer = TaskListSerializer(task, many = False)
  print(serializer)
  return Response(serializer.data)

@api_view(['PUT'])
def taskUpdate(request, id):
  task = TaskList.objects.get(id=id)
  serializer = TaskListSerializer(instance=task, data=request.data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
  print(request) 
  # serializer is taking the data given in response and converting the request data through the task list serializer into jSON
  serializer = TaskListSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
  print(serializer)
  return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
  # print(request) 
  task = TaskList.objects.get(id=pk)
  # print(task)
  # Find out how to do error handling with invalid delete
  # No need for serializer bc the task data isn't being converted from or to json
  task.delete()
  return Response("Task Deleted Successfully")

class TaskListAll(generics.ListCreateAPIView):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
      serializer.save(owner=self.request.user)


class TaskListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class TaskListUniversal(APIView):
#   """
#     List all snippets, or create a new snippet.
#   """
#   def get_obj(self, pk):
#     try:
#       return TaskList.objects.get(id=pk)
#     except TaskList.DoesNotExist:
#       return Response(status = status.HTTP_404_NOT_FOUND)

#   def get(self, request, pk, format=None):
#       tasks = TaskList.objects.all()
#       serializer = TaskListSerializer(tasks, many=True)
#       return Response(serializer.data)
  
#   def post(self, request, pk, format=None):
#     serializer = TaskListSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#     print(serializer)
#     return Response(serializer.data)

#   def put(self, request, pk, format=None):
#     task = TaskList.get_obj(pk)
#     serializer = TaskListSerializer(instance=task, data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#   def delete(self, request, pk, format=None):
#     task = TaskList.get_obj(pk)
#     task.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
