from django.http import JsonResponse, Http404
from django.views import View
from django.shortcuts import render

from database.models import Users, Courses
from users.forms import CreateUserForm, UpdateUserForm


class ListUsersView(View):
    def get(self, request):
        users = Users.get_all()
        ctx = {
            'users': users
        }
        return render(request, 'home.html', ctx)


class ListCourses(View):
    def get(self, request):
        courses = Courses.get_all()
        ctx = {
            'courses': courses
        }
        return render(request, 'courses.html', ctx)


class CreateUserView(View):
    def get(self, request):
        return render(request, 'user/create.html', {})

    def post(self, request):
        user_form = CreateUserForm(request.POST or None)
        if user_form.is_valid():
            Users.create_or_update(**user_form.cleaned_data)
            data = {
                'status': 'ok',
            }
            return JsonResponse(data=data)
        else:
            data = {
                'status': 'error',
                'errors': user_form.errors
            }
            return JsonResponse(data=data)


class UpdateUserView(View):
    def get(self, request, u_id):
        try:
            user = Users.get_by_id(user_id=u_id)
        except ValueError:
            raise Http404
        return render(request, 'user/update.html', {'user': user})

    def post(self, request, u_id):
        user_form = UpdateUserForm(request.POST or None)
        if user_form.is_valid():
            Users.create_or_update(**user_form.cleaned_data,
                                   update=True, u_id=u_id)
            data = {
                'status': 'ok',
            }
            return JsonResponse(data=data)
        else:
            data = {
                'status': 'error',
                'errors': user_form.errors
            }
            return JsonResponse(data=data)


def delete_user(request):
    # method should be DELETE
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('id', None)
        Users.delete_by_id(user_id=user_id)
        data = {
            'status': 'ok'
        }
        return JsonResponse(data)
    else:
        raise Http404
