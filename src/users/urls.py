from django.conf.urls import url

from .views import (
    ListUsersView,
    CreateUserView,
    delete_user,
    UpdateUserView,
    ListCourses
)


urlpatterns = [
    url(r'^$', ListUsersView.as_view(), name='users'),
    url(r'^courses$', ListCourses.as_view(), name='courses'),
    url(r'^user/create$', CreateUserView.as_view(), name='user-create'),
    url(r'^user/(?P<u_id>[0-9]+)$', UpdateUserView.as_view(), name='user'),
    url(r'^user/delete$', delete_user),
]
