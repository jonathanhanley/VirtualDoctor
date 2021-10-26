from django.contrib.auth import get_user_model
from django.test import TestCase

from vdoc_api.models import Consultant

User = get_user_model()


class TestConsultant(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            email="testconsultant@gmail.com",
            username="testconsultant@gmail.com",
            first_name="test",
            last_name="consultant",
        )
        self.consultant = Consultant.objects.create(
            user=user
        )
        self.consultant.save()
        user = User.objects.create_user(
            email="testconsultant1@gmail.com",
            username="testconsultant1@gmail.com",
            first_name="test1",
            last_name="consultant1",
        )
        self.consultant1 = Consultant.objects.create(
            user=user
        )
        self.consultant1.save()

    def test_user(self):
        user = self.consultant.user
        self.assertEqual(user.username, "testconsultant@gmail.com")
        self.assertEqual(user.email, "testconsultant@gmail.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "consultant")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_consultant_code(self):
        self.assertEqual(self.consultant.code, '2ec16')
        self.assertEqual(self.consultant1.code, 'f12ab')
        self.assertNotEqual(self.consultant.code, self.consultant1.code)
