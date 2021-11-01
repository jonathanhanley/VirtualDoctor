from django.core.management.base import BaseCommand, CommandError
from vdoc_api.models import *

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates data for testing'

    def handle(self, *args, **options):

        try:
            c_user = User.objects.create_user(
                username="testconsultant@gmail.com",
                email="testconsultant@gmail.com",
                password="TestPassword",
                first_name="Test",
                last_name="Consultant"
            )
            c = Consultant.objects.create(
                user=c_user,
            )
            c.save()
        except:
            c = Consultant.objects.get(user__username="testconsultant@gmail.com")

        try:
            user = User.objects.create_user(
                username="testuser@gmail.com",
                email="testuser@gmail.com",
                password="TestPassword",
                code=c.code,
            )
        except:
            user = User.objects.get(username="testuser@gmail.com")

        question_set = QuestionSet.objects.create(
            consultant=c,
            name="Test Question Set",
            description="Test Question Set",
        )
        question_set.save()
        question2 = Question.objects.create(
            set=question_set,
            text="Test Question 2",
            hint="This is a hint for the user"
        )
        question2.save()
        question1 = Question.objects.create(
            set=question_set,
            text="Test Question 1",
            hint="This is a hint for the user",
            next_question=question2
        )
        question1.save()


