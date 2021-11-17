from django.contrib.auth import get_user_model
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
        question3 = Question.objects.create(
            set=question_set,
            text="Would you recommend this app?",
            hint="Yes/No"
        )
        question3.save()
        question2 = Question.objects.create(
            set=question_set,
            text="How many sisters do you have?",
            hint="I have 2 sisters",
            sub_should_loop=True,
            next_question=question3,
        )
        question2.save()
        sub_questions2 = Question.objects.create(
            set=question_set,
            parent_q=question2,
            text="Has {} had breast cancer?",
            hint="Yes/No",
            next_question=question2.next_question,
        )
        sub_questions2.save()
        Satisfy.objects.create(
            parent_question=question2,
            sub_question=sub_questions2,
            text="",
        )
        question1 = Question.objects.create(
            set=question_set,
            text="Do you have any signs of infection?",
            hint="Yes I do/ No I don't",
            next_question=question2
        )
        question1.save()
        sub_question = Question.objects.create(
            set=question_set,
            text="Where are these signs of infection?",
            hint="On my arm",
            parent_q=question1,
            next_question=question1.next_question,
        )
        sub_question.save()
        Satisfy.objects.create(
            parent_question=question1,
            sub_question=sub_question,
            text="yes I do",
        ).save()



