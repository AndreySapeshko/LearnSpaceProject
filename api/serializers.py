from rest_framework import serializers
from courses.models import Course, Lesson, Subscription
from users.models import Payments
from .validators import LinksTrustedSitesValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        trusted_sites = ['https://www.youtube.com/', 'https://vimeo.com/']
        validators = [LinksTrustedSitesValidator(trusted_sites=trusted_sites)]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField()
    subs = serializers.SerializerMethodField()

    def get_subs(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'preview', 'count_lessons', 'lessons', 'subs']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
