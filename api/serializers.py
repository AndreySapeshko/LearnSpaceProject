from rest_framework import serializers
from courses.models import Course, Lesson
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField()
    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'preview', 'count_lessons', 'lessons']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
