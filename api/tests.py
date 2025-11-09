from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from courses.models import Course, Lesson

User = get_user_model()

class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser1@examle.com',
            password='testuser1'
        )
        self.course = Course.objects.create(
            name='test_course',
            description='test_description',
            user=self.user
        )
        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='test_description',
            course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'name': 'test',
            'description': 'test description',
            'course': self.course.id
        }
        response = self.client.post('/api/lesson/new/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertTrue(Lesson.objects.filter(name='test').exists())

    def test_list_lesson(self):
        response = self.client.get('/api/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_retrieve_lesson(self):
        response = self.client.get(f'/api/lesson/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.lesson.name)

    def test_update_lesson(self):
        data = {
            'name': 'test',
            'description': 'new test description',
            'course': self.course.id
        }
        response = self.client.put(f'/api/lesson/{self.lesson.id}/edit/',data)

        # print(f"Response status: {response.status_code}")
        # print(f"Response data json: {response.json()}")
        # print(f"Response data: {response.data}")
        # print(f"Request data: {data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('description'), data.get('description'))

    def test_delete_lesson(self):
        response = self.client.delete(f'/api/lesson/{self.lesson.id}/delete/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not Lesson.objects.filter(id=self.lesson.id).exists())
