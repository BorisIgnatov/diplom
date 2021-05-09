from rest_framework_simplejwt.views import TokenObtainPairView

from school.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework import permissions
from serializers.serializers import *


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Classroom.objects.all()
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Classroom.objects.all()
        classroom = get_object_or_404(queryset, pk=pk)
        students =[{'name': i.__str__(), 'id': i.user.id} for i in classroom.student_set.all()]
        return Response({
                            'title': classroom.title,
                            'teacher': classroom.teacher.__str__(),
                            'students': students
                        })

    def create(self, request):
        with_teacher = False
        if 'teacher_id' in request.data.keys():
            teacher_id = request.data['teacher_id']
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
                with_teacher = True
            except ObjectDoesNotExist:
                return Response('Teacher not found', 404)
            except ValueError:
                return Response('teacher_id must be a number', 400)
        try:
            classroom = Classroom(title=request.data['title'])
            classroom.save()
            if with_teacher:
                classroom.teacher = teacher
                teacher.save()
        except KeyError as e:
            return Response({'error': str(e), 'response_code': 400}, 400)
        except IntegrityError as e:
            return Response(str(e), 400)

        return Response('ok')

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Subject.objects.all()
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)

    '''def retrieve(self, request, *args, **kwargs):
        queryset = Subject.objects.all()
        print(queryset)
        serializer = SubjectSerializer(queryset, many=False)
        return Response(serializer.data)'''

    def create(self, request, *args, **kwargs):
        is_valid = SubjectSerializer().validate(data=request.data)
        print(is_valid)
        teacher = request.data['teacher']
        title = request.data['title']
        try:
            subject = Subject(title=title, teacher_id=teacher)
            subject.save()
            return Response({'response_code': 200})
        except Exception as e:
            return Response({'response_code': 400, 'error': str(e)})

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Schedule
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Schedule.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Schedule.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        for i in request.data['schedule']:
            schedule = Schedule(classroom_id=request.data['classroom'], subject_id=i['subject'],
                                day_of_the_week=i['day'], time=i['time'])
            schedule.save()
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer