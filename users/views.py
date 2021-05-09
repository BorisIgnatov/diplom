from datetime import date, datetime
import random
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from users.models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from serializers.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Student.objects
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            new_user = CustomUser.objects.create_user(first_name=data['first_name'],
                                                      surname=data['surname'], middle_name=data['middle_name'],
                                                      date_of_birth=data['date_of_birth'])
            try:
                new_student = Student.objects.create(user=new_user[0], classroom_id=request.data['classroom'])
                new_student.save()
            except KeyError as e:
                print(e)
                new_user[0].delete()
                return Response({'error': 'Send classroom id', 'error_code': 400}, 400)

            for i in request.FILES.getlist('images'):
                image = Image(image=i)
                image.save()
                new_user[0].images.add(image)

        except IntegrityError as e:
            print(e)
            return Response({'error': 'Data is not valid', 'error_code': 400}, 400)
        except ValidationError as e:
            print(e)
            return Response({'error': 'Data is not valid', 'error_code': 400}, 400)

        return Response({'id': new_user[0].id, 'username': new_user[0].username, 'password': new_user[1],
                         'classroom': new_student.classroom.title})

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Teacher.objects.all().order_by('-user__date_joined')
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Teacher.objects.all()
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #try:
        data = request.data
        new_user = CustomUser.objects.create_user(
                                                 first_name=data['first_name'],
                                                 surname=data['surname'], middle_name=data['middle_name'],
                                                 date_of_birth=data['date_of_birth']
                                                 )
        new_teacher = Teacher.objects.create(user=new_user[0])

        for i in request.FILES.getlist('images'):
            image = Image(image=i)
            image.save()
            new_user[0].images.add(image)

        if 'classroom' in [*data]:
            if type(data['classroom']) == type(12):
                new_teacher.classroom = Classroom.objects.get(id=data['classroom'])
        if 'is_head_teacher' in [*data]:
            if type(data['is_head_teacher']) == type(True):
                new_teacher.is_head_teacher = data['is_head_teacher']
        new_teacher.save()

        '''except IntegrityError as e:
            print(e)
            return Response({'error': 'Data is not valid', 'error_code': 400}, 400)
        except ValidationError as e:
            print(e)
            return Response({'error': 'Data is not valid', 'error_code': 400}, 400)'''

        return Response({'id': new_user[0].id, 'username': new_user[0].username, 'password': new_user[1],
                         'classroom': new_teacher.classroom})

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class UserChangePassword(APIView):

    def post(self, request):
        try:
            username = request.data['username']
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            user = CustomUser.objects.get(username=username)
            if user:
                if user.check_password(old_password):
                    try:
                        validate_password(new_password)
                        user.set_password(new_password)
                        user.save()
                    except ValidationError as e:
                        return Response(str(e), 401)
                else:
                    return Response({'error': 'Password are not matching', 'response_code': 401}, 401)
            else:
                return Response({'error': 'No such user', 'response_code': 404}, 404)

            return Response({'response_code': 200}, 200)
        except KeyError:
            return Response({'error': 'no data', 'response_code': 400}, 400)
