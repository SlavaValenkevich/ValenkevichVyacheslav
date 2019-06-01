
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
    #url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^sign_up/$', SignUp.as_view()),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"),
    url(r'^activation/(?P<username>\w+)/$', activation),

    url(r'^todolists/shared/(?P<list_id>[0-9]+)/', SharedTasks.as_view()),
    url(r'^todolists/shared/(?P<list_id>[0-9]+)/edit/', EditList.as_view(), name='list-detail2'),
    url(r'^todolists/shared/$', Shared.as_view(), name="list-detail"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"),
    url(r'^todolists/(?P<pk>[0-9]+)/share/$', ToShare.as_view()),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="tasks"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),

}

urlpatterns = format_suffix_patterns(urlpatterns)