from rest_framework import serializers
from courses.models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'preview', 'count_lessons']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
