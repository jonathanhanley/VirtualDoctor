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

        try:
            user_done = User.objects.create_user(
                username="UserComplete@gmail.com",
                email="UserComplete@gmail.com",
                password="TestPassword",
                code=c.code,
            )
        except:
            user_done = User.objects.get(username="UserComplete@gmail.com")

        question_set = QuestionSet.objects.create(
            consultant=c,
            name="Breast Cancer Question Set",
            description="This is a test question set for breast cancer.",
        )
        question_set.save()
        question1 = Question.objects.create(
            set=question_set,
            text="How are you feeling today?",
            hint="I am feeling good/ I am feeling bad",
        )
        question2 = Question.objects.create(
            set=question_set,
            text="Do you have a history of cancer?",
            hint="Yes/ No"
        )
        question1.next_question = question2
        question2_sub = Question.objects.create(
            set=question_set,
            text="What type of cancer did you have?",
            hint="Skin cancer/ Bone Cancer/ Throat Cancer",
            parent_q=question2,
        )
        question2_sub_next = Question.objects.create(
            set=question_set,
            text="How long ago were you diagnosed with the cancer?",
            hint="10 years ago, 6 months ago, I am currently undergoing treatment."
        )
        question2_sub.next_question = question2_sub_next
        question3 = Question.objects.create(
            set=question_set,
            text="Has anyone in your family been diagnosed with cancer?",
            hint="Yes/ No"
        )
        question2.next_question = question3
        question3_sub = Question.objects.create(
            set=question_set,
            text="What kind of cancer have they been diagnosed with?",
            hint="Skin cancer"
        )

        question4 = Question.objects.create(
            set=question_set,
            text="Would you like a doctor to contact you about this application?",
            hint="Yes/ No"
        )
        question3.next_question = question4
        Satisfy.objects.create(
            parent_question=question3,
            sub_question=question3_sub,
            text="Yes",
        ).save()

        Satisfy.objects.create(
            parent_question=question2,
            sub_question=question2_sub,
            text="yes"
        ).save()
        question1.save()
        question2.save()
        question2_sub.save()
        question2_sub_next.save()
        question3.save()
        question3_sub.save()
        question4.save()

        Answer.objects.create(
            question=question1,
            text="I am good",
            user=user_done
        ).save()

        Answer.objects.create(
            question=question1,
            text="I am good",
            user=user_done
        ).save()

        Answer.objects.create(
            question=question2,
            text="Yes",
            user=user_done
        ).save()
        Answer.objects.create(
            question=question2_sub,
            text="Skin Cancer",
            user=user_done
        ).save()
        Answer.objects.create(
            question=question2_sub_next,
            text="10 years ago",
            user=user_done
        ).save()

        Answer.objects.create(
            question=question3,
            text="Yes",
            user=user_done
        ).save()
        Answer.objects.create(
            question=question3_sub,
            text="Breast cancer",
            user=user_done
        ).save()
        Answer.objects.create(
            question=question4,
            text="Yes please.",
            user=user_done
        ).save()



