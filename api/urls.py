from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, PaymentsListAPIView, SubscriptionAPIView, PaymentCreateAPIView

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/new/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/edit/', LessonUpdateAPIView.as_view(), name='lesson_edit'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('courses/<int:pk>/subs/', SubscriptionAPIView.as_view(), name='course_subs'),
    path('courses/<int:pk>/payment/', PaymentCreateAPIView.as_view(), name='course_payment')
]
