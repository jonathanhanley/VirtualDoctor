import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from vdoc_api.models import Consultant, QuestionSet, Question

User = get_user_model()


class TestLogin(APITestCase):

    def setUp(self) -> None:
        User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234',
        )

    def test_valid(self):
        url = reverse('api-login')
        data = {
            'username': 'testuser',
            'password': 'testpassword1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertIsNotNone(response.data.get('token'))
        self.assertEqual(len(response.data.get('token')), 40)

    def test_invalid_combo(self):
        url = reverse('api-login')
        data = {
            'username': 'testuser',
            'password': 'WrongPassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('token' not in response.data)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data.get('non_field_errors')[0], 'Unable to log in with provided credentials.')

    def test_missing_username(self):
        url = reverse('api-login')
        data = {
            'password': 'password',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('token' not in response.data)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data.get('username')[0], 'This field is required.')

    def test_missing_password(self):
        url = reverse('api-login')
        data = {
            'username': 'username',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('token' not in response.data)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data.get('password')[0], 'This field is required.')

    def test_missing_username_password(self):
        url = reverse('api-login')
        data = {
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('token' not in response.data)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data.get('username')[0], 'This field is required.')
        self.assertEqual(response.data.get('password')[0], 'This field is required.')


class TestLogout(TestCase):
    valid_token = None

    def setUp(self) -> None:
        user = User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234'
        )
        token = Token.objects.create(
            user=user
        )
        token.save()
        self.valid_token = token

    def test_valid_logout(self):
        url = reverse('api-logout')
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.valid_token.key)
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Logged out')

    def test_invalid_logout(self):
        url = reverse('api-logout')
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token kjsajdfiasipgjapudifghajrepu')
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Invalid token.')


class TestUser(TestCase):

    def test_valid_get(self):
        url = reverse('api-user')
        client = APIClient()
        data = {}
        user = User.objects.create_user(
            username='testuseremail@gmail.com',
            email='testuseremail@gmail.com',
            password='testpassword1234',
            code='abc12',
        )
        token = Token.objects.create(
            user=user
        )
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('code'), 'abc12')
        self.assertIsNone(response.data.get('password'))

    def test_valid_register(self):
        url = reverse('api-user')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "code": "abc12",
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('code'), 'abc12')
        self.assertIsNone(response.data.get('password'))

    def test_email_in_use(self):
        url = reverse('api-user')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "code": "abc12",
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertIsNone(response.data.get('password'))

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data.get("message"), "That email already exists")

    def test_email_missing(self):
        url = reverse('api-user')
        data = {
            "password": "MyTestPassword",
            "code": "abc12",
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Email is required")

    def test_password_missing(self):
        url = reverse('api-user')
        data = {
            "email": "testuseremail@gmail.com",
            "code": "abc12",
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Password is required")

    def test_code_missing(self):
        url = reverse('api-user')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyPassword1234",
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Code is required")

    def test_valid_delete(self):
        url = reverse('api-user')
        data = {}
        user = User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234',
            code="abc12"
        )
        token = Token.objects.create(
            user=user
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data.get("message"), "Account deleted.")

    def test_invalid_delete(self):
        url = reverse('api-user')
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token asdkjfafoiasjdf')
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "Invalid token.")


class TestConsultant(TestCase):

    def test_valid_get(self):
        url = reverse('api-consultant')
        client = APIClient()
        data = {}
        user = User.objects.create_user(
            username='testuseremail@gmail.com',
            email='testuseremail@gmail.com',
            password='testpassword1234',
            first_name='test',
            last_name='consultant',
        )
        consultant = Consultant.objects.create(user=user)
        consultant.save()
        token = Token.objects.create(
            user=user
        )
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('first_name'), 'test')
        self.assertEqual(response.data.get('last_name'), 'consultant')
        self.assertEqual(response.data.get('code'), 'ce0ec')
        self.assertIsNone(response.data.get('password'))

    def test_valid_register(self):
        url = reverse('api-consultant')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "first_name": 'test',
            "last_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('first_name'), 'test')
        self.assertEqual(response.data.get('last_name'), 'consultant')
        self.assertEqual(response.data.get('code'), 'ce0ec')
        self.assertIsNone(response.data.get('password'))

    def test_email_in_use(self):
        url = reverse('api-consultant')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "first_name": 'test',
            "last_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), 'testuseremail@gmail.com')
        self.assertEqual(response.data.get('username'), 'testuseremail@gmail.com')
        self.assertIsNone(response.data.get('password'))

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data.get("message"), "That email already exists")

    def test_email_missing(self):
        url = reverse('api-consultant')
        data = {
            "password": "MyTestPassword",
            "first_name": 'test',
            "last_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Email is required")

    def test_password_missing(self):
        url = reverse('api-consultant')
        data = {
            "email": "testuseremail@gmail.com",
            "first_name": 'test',
            "last_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Password is required")

    def test_first_name_missing(self):
        url = reverse('api-consultant')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "last_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "First Name is required")

    def test_last_name_missing(self):
        url = reverse('api-consultant')
        data = {
            "email": "testuseremail@gmail.com",
            "password": "MyTestPassword",
            "first_name": 'consultant',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "Last Name is required")

    def test_valid_delete(self):
        url = reverse('api-consultant')
        data = {}
        user = User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234'
        )
        Consultant.objects.create(user=user).save()
        token = Token.objects.create(
            user=user
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data.get("message"), "Account deleted.")

    def test_invalid_delete(self):
        url = reverse('api-consultant')
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token asdkjfafoiasjdf')
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "Invalid token.")


class TestQuestionSet(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234',
            code="12345"
        )
        token = Token.objects.create(
            user=user
        )
        token.save()
        self.user_token = token
        user = User.objects.create_user(
            username='testconsultant',
            email='testconsultant@gmail.com',
            password='testpassword1234'
        )
        self.consultant = Consultant.objects.create(
            user=user,
        )
        self.consultant.save()
        token = Token.objects.create(
            user=user
        )
        token.save()
        self.consultant_token = token

    def test_valid_get(self):
        url = reverse('api-question-set')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        data = {'id': question_set.id}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("consultant"), self.consultant.id)
        self.assertEqual(response.data.get("name"), "Test Question Set")
        self.assertEqual(response.data.get("description"), "This is a test question set")
        self.assertEqual(response.data.get("created"), f"{datetime.datetime.today().date()}")

    def test_get_no_id(self):
        url = reverse('api-question-set')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        data = {}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "ID is required")

    def test_get_invalid_id(self):
        url = reverse('api-question-set')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        data = {"id": -1}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("message"), "No question set was found matching that ID")

    def test_valid_post(self):
        url = reverse('api-question-set')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.consultant_token.key)
        data = {
            "name": "This is my test set",
            "description": "This is my test set description",
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("consultant"), self.consultant.id)
        self.assertEqual(response.data.get("name"), 'This is my test set')
        self.assertEqual(response.data.get("description"), 'This is my test set description')
        self.assertEqual(len(QuestionSet.objects.all()), 1)

    def test_post_by_user(self):
        url = reverse('api-question-set')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {
            "name": "This is my test set",
            "description": "This is my test set description",
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class TestQuestion(TestCase):
    
    def setUp(self) -> None:
        user = User.objects.create_user(
            username='testuser',
            email='testuseremail@gmail.com',
            password='testpassword1234',
            code="12345"
        )
        token = Token.objects.create(
            user=user
        )
        token.save()
        self.user_token = token
        user = User.objects.create_user(
            username='testconsultant',
            email='testconsultant@gmail.com',
            password='testpassword1234'
        )
        self.consultant = Consultant.objects.create(
            user=user,
        )
        self.consultant.save()
        token = Token.objects.create(
            user=user
        )
        token.save()
        self.consultant_token = token

    def test_valid_get(self):
        url = reverse('api-question')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        question = Question.objects.create(
            set=question_set,
            text="How are ye doing a bit of testing?",
            hint="Yes/ No"
        )
        question.save()
        question1 = Question.objects.create(
            set=question_set,
            text="How are ye doing a bit of validating?",
            hint="Yes/ No"
        )
        question1.save()
        question.next_question = question1
        question.save()
        data = {'id': question.id}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("set"), question_set.id)
        self.assertEqual(response.data.get("text"), question.text)
        self.assertEqual(response.data.get("hint"), question.hint)
        self.assertEqual(response.data.get("next_question"), question1.id)

        data = {'id': question1.id}
        response = client.get(url, data, format='json')
        self.assertEqual(response.data.get("next_question"), None)

    def test_get_no_id(self):
        url = reverse('api-question')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        question = Question.objects.create(
            set=question_set,
            text="How are ye doing a bit of testing?",
            hint="Yes/ No"
        )
        question.save()
        data = {}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "ID is required")

    def test_get_invalid_id(self):
        url = reverse('api-question')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        data = {"id": -1}
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("message"), "No question set was found matching that ID")

    def test_valid_post(self):
        url = reverse('api-question')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.consultant_token.key)
        question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="This is a test question set",
        )
        question_set.save()
        data = {
            "set": question_set.id,
            "text": "Are ye doing a bit of requesting?",
            "hint": "Yes/ No"
        }
        response = client.post(url, data, format='json')
        print(response.data)