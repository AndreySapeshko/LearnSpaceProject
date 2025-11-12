from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, generics, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from users.models import Payments
from users.permissions import IsModerator, IsOwner
from .paginators import ContentPagination
from .serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from .servises import create_stripe_price, create_stripe_session
from courses.tasks import course_update_notice


class CourseViewSet(viewsets.ModelViewSet):
    """ Класс для создания, просмотра, редактирования и удаления курса """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = ContentPagination

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action == 'create':
            permission_classes = [~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        payments = course.payments.all()
        users_email = []
        for payment in payments:
            if payment.user.email not in users_email:
                users_email.append(payment.user.email)
        course_update_notice.delay(course_id=course.id, users_email=users_email)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = ContentPagination

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        payments = course.payments.all()
        users_email = []
        for payment in payments:
            if payment.user.email not in users_email:
                users_email.append(payment.user.email)
        course_update_notice.delay(course_id=course.id, users_email=users_email)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']


class SubscriptionAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    # queryset = Subscription.ogjects.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.kwargs.get('pk')
        course = Course.objects.get(id=course_id)
        subs_item, created = Subscription.objects.get_or_create(user=user, course=course)
        if created:
            message = 'подписка добавлена'
        else:
            subs_item.delete()
            message = 'подписка удалена'

        return Response({'message': message})


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def create(self, request, *args, **kwargs):
        try:
            course_id = self.kwargs.get('pk')
            course = get_object_or_404(Course, id=course_id)

            stripe_price = create_stripe_price(course)
            session_id, link = create_stripe_session(stripe_price)

            payment = Payments.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                payment_method='transfer',
                session_id=session_id,
                link=link
            )

            return Response({
                'payment_id': payment.id,
                'session_id': session_id,
                'checkout_url': link,
                'message': 'Payment session created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Payment creation failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
