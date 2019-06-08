from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login as auth_login


from django.shortcuts import render
from rest_framework import generics 
'''
, permissions
from .permissions import IsOwner'''
from .serializers import *
from .models import Task,Tasklist,Tag,Share
from django.contrib.auth.models import User
#from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from django.db.models import Q


class TasklistCreateView(generics.ListCreateAPIView):
   
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer
    
    def get_queryset(self):
        print(self.request.user)
        
        queryset = Tasklist.objects.filter(owner_id = self.request.user.id)
        return queryset
        

    def perform_create(self, serializer):
        print('helllo',self.request.user)
        serializer.save(owner=self.request.user)

from itertools import chain
class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = TasklistSerializer
    '''permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)'''
    def get_queryset(self):

        queryset1 = Tasklist.objects.filter(owner_id = self.request.user)
            
        user = self.request.user
        queryset2 = Tasklist.objects.filter(user = user)
        queryset = list(chain(queryset1,queryset2))
        print(queryset1)
        return queryset1
        

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)



class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        try:
            if list_id is not None:
                ownerset = Tasklist.objects.all()
                ownerset = ownerset.filter(owner_id = self.request.user)
                print(ownerset.values('id'))
                if Tasklist.objects.get(id = list_id) not in ownerset:
                    raise NotFound()
                queryset = queryset.filter(tasklist_id = list_id,owner = self.request.user)
        except:
            raise NotFound()
        return queryset


    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist, owner = self.request.user)
        #serializer.save(owner = self.request.user)

class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = TaskSerializer
    def get_queryset(self):
        try:
            queryset = Task.objects.all()
            list_id = self.kwargs.get('list_id', None)
            if list_id is not None:
                ownerset = Tasklist.objects.all()
                ownerset = ownerset.filter(owner_id = self.request.user)
                if Tasklist.objects.get(id = list_id) not in ownerset:
                    raise NotFound()
                queryset = queryset.filter(tasklist_id = list_id,owner = self.request.user)
            return queryset
        except:
            raise NotFound()

from django.db.models import Q

class ToShare(generics.CreateAPIView):

    serializer_class = TasklistSerializer

    def create(self,request,pk):
        try:
            tlist = Tasklist.objects.get(id=pk)
            u=User.objects.get(username=request.data.get('username'))
            tlist.user.add(u)
            tlist.save()
            return(HttpResponseRedirect('/todolists/'))
        except:
            raise NotFound()
    
class Shared(generics.ListAPIView):
    serializer_class = TasklistSerializer
    def get_queryset(self):
        user = self.request.user
        queryset = Tasklist.objects.filter(user = user)
        
        return queryset

class SharedTasks(generics.ListAPIView):
    serializer_class=TaskSerializer
    def get_queryset(self):

        list_id = self.kwargs.get('list_id', None)
        queryset = Task.objects.filter(tasklist_id=list_id)
        
        return queryset
        
class EditList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TasklistSerializer
    def get_queryset(self):
        list_id = self.kwargs.get('list_id', None)
        queryset = Tasklist.objects.filter(id=list_id)
        print(queryset)
        return queryset
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)




from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm
from django.contrib.auth import logout, login, authenticate


from django.http import HttpResponse
from django.core.mail import send_mail

class SignUp(generics.CreateAPIView):

    queryset = User.objects.all()   
    serializer_class = UserSerializer

    def create(self,request):
        print('hello')
        user = User.objects.create(username= self.request.POST['username'], email = self.request.POST['email'])
        user.set_password(self.request.POST['password'])
        user.is_active = False
        user.save()
        username = request.data.get('username') 
        email = [request.data.get('email')]
        print(email)
        message = 'THANK YOU FOR REGISTRATION!\nPlease activate your account http://127.0.0.1:8000/activation/{user}/'.format(user=username)
        send_mail('Activation', message, 'mypythonlab@gmail.com',email, fail_silently=False)
        return HttpResponse('Ok')


def activation(request,username):
    user = User.objects.get(username=username)
    user.is_active = True
    Token.objects.get_or_create(user=user)
    user.save()
    return HttpResponse('activated')