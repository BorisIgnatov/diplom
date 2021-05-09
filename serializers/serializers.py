from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import *
from school.models import *
from rest_framework import serializers


class ImagesSerializer(serializers.HyperlinkedModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Image
        fields = ['image_url']

    def get_image_url(self, obj):
        return obj.image.url


class UserSerializer(serializers.HyperlinkedModelSerializer):
    images = ImagesSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'surname', 'middle_name', 'date_of_birth', 'images']


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'title']


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=True)
    classroom = ClassroomSerializer(required=True)

    class Meta:
        model = Student
        fields = ['classroom', 'user']


class TeacherSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=True)
    classroom = ClassroomSerializer()

    class Meta:
        model = Teacher
        fields = ['classroom', 'user']


class TeacherUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Teacher
        fields = ['user']


class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField(many=False)

    def validate(self, data):
        try:
            if not data['teacher']:
                raise serializers.ValidationError({'response_code': '400', 'error': 'no teacher'})
        except KeyError:
            raise serializers.ValidationError('no teacher')
        return data

    class Meta:
        model = Subject
        fields = ['id', 'teacher', 'title']


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):

    subject = SubjectSerializer()
    classroom = ClassroomSerializer()

    class Meta:
        model = Schedule
        fields = ['classroom', 'subject', 'day_of_the_week', 'time']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        print(self.user)
        user = UserSerializer(self.user)

        data['user'] = user.data
        return data

