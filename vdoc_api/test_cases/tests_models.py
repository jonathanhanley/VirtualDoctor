from django.contrib.auth import get_user_model
from django.test import TestCase

from vdoc_api.models import Consultant, QuestionSet, Question, Answer, Satisfy, Loop

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
        self.assertTrue(user.is_consultant)

    def test_consultant_code(self):
        self.assertEqual(self.consultant.code, '2ec16')
        self.assertEqual(self.consultant1.code, 'f12ab')
        self.assertNotEqual(self.consultant.code, self.consultant1.code)


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            email="testuser@gmail.com",
            username="testuser@gmail.com",
            first_name="test",
            last_name="user",
            code="abc12"
        )

    def test_attributes(self):
        user = User.objects.get(code="abc12")
        self.assertEqual(user.code, "abc12")
        self.assertEqual(user.email, "testuser@gmail.com")
        self.assertEqual(user.username, "testuser@gmail.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "user")
        self.assertFalse(user.is_consultant)


class TestQuestionSet(TestCase):

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
        user1 = User.objects.create_user(
            email="testconsultant1@gmail.com",
            username="testconsultant1@gmail.com",
            first_name="test1",
            last_name="consultant1",
        )
        self.consultant1 = Consultant.objects.create(
            user=user1
        )
        self.consultant1.save()
        self.question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        self.question_set.save()

    def test_question_set_consultant(self):
        self.assertEqual(self.consultant, self.question_set.consultant)
        self.assertEqual(self.consultant.user, self.question_set.consultant.user)
        self.assertNotEqual(self.consultant1, self.question_set.consultant)
        self.assertNotEqual(self.consultant1.user, self.question_set.consultant.user)

    def test_question_set_name(self):
        self.assertEqual(self.question_set.name, "Test Question Set")
        self.assertNotEqual(self.question_set.name, "test question set")

    def test_question_set_description(self):
        self.assertEqual(self.question_set.description, "A set of questions used for testing")
        self.assertNotEqual(self.question_set.description, "a set of questions used for testing")


class TestQuestion(TestCase):

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
        self.question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        self.question_set.save()
        self.question = Question.objects.create(
            set=self.question_set,
            text="How do you like my test question?",
            hint="The answer is very much so...",
        )
        self.question.save()


    def test_question_consultant(self):
        self.assertEqual(self.consultant, self.question.set.consultant)
        self.assertEqual(self.consultant.user, self.question.set.consultant.user)

    def test_question_question_set(self):
        self.assertEqual(self.question_set, self.question.set)

    def test_question_text(self):
        self.assertEqual(self.question.text, "How do you like my test question?")
        self.assertNotEqual(self.question.text, "how do you like my test question?")

    def test_question_hint(self):
        self.assertEqual(self.question.hint, "The answer is very much so...")
        self.assertNotEqual(self.question.hint, "the answer is very much so...")

    def test_next_question(self):
        self.assertIsNone(self.question.next_question, None)
        next_q = Question.objects.create(
            set=self.question_set,
            text="Next question?",
            hint="This is the next question"
        )
        next_q.save()
        self.question.next_question = next_q
        self.question.save()
        self.assertEqual(self.question.next_question, next_q)


class TestAnswer(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            username="testuser@gmail.com",
            first_name="test",
            last_name="user",
            code="abc12"
        )
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
        self.question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        self.question_set.save()
        self.question = Question.objects.create(
            set=self.question_set,
            text="How do you like my test question?",
            hint="The answer is very much so...",
        )
        self.question.save()
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            text="Yes I like your test question..."
        )
        self.answer.save()

    def test_answer_question(self):
        self.assertEqual(self.answer.question, self.question)

    def test_answer_user(self):
        self.assertEqual(self.user, self.answer.user)

    def test_answer_text(self):
        self.assertEqual("Yes I like your test question...", self.answer.text)
        self.assertNotEqual("No I do not like your test question...", self.answer.text)

class TestLoop(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            username="testuser@gmail.com",
            first_name="test",
            last_name="user",
            code="abc12"
        )
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
        self.question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        self.question_set.save()
        self.question = Question.objects.create(
            set=self.question_set,
            text="How do you like my test question?",
            hint="The answer is very much so...",
        )
        self.question.save()
        self.loop = Loop.objects.create(
            question=self.question,
            user=self.user,
            loop_amount=2,
        )
        self.loop.save()

        self.looping_parent_q = Question.objects.create(
            set=self.question_set,
            text="How do you like my test question?",
            hint="The answer is very much so...",
            sub_should_loop=True,
        )
        self.looping_parent_q.save()
        self.looping_child_q = Question.objects.create(
            set=self.question_set,
            text="LOOPING",
            hint="",
            parent_q=self.looping_parent_q,
        )
        self.looping_child_q.save()


    def test_is_done(self):
        self.assertFalse(self.loop.is_done(self.user))
        Answer.objects.create(
            question=self.question,
            user=self.user,
            text="ABC",
        ).save()
        self.assertFalse(self.loop.is_done(self.user))
        Answer.objects.create(
            question=self.question,
            user=self.user,
            text="ABC",
        ).save()
        self.assertTrue(self.loop.is_done(self.user))

    def test_looping(self):
        ans = Answer.objects.create(
            user=self.user,
            question=self.looping_parent_q,
            text="5"
        )
        ans.save()
        for _ in range(4):
            ans = Answer.objects.create(
                user=self.user,
                question=self.looping_child_q,
                text="ajdf;asd"
            )
            ans.save()
            self.assertEqual(ans.get_next_question(), self.looping_child_q)
        ans = Answer.objects.create(
            user=self.user,
            question=self.looping_child_q,
            text="ajdf;asd"
        )
        ans.save()
        ans.get_next_question()

    def test_looping_sub(self):
        q_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        q_set.save()
        question = Question.objects.create(
            set=q_set,
            text="How do you like my test question?",
            hint="The answer is very much so...",
            sub_should_loop=True,
        )
        question.save()
        loop = Loop.objects.create(
            question=question,
            user=self.user,
            loop_amount=2,
        )
        loop.save()
        sub_q = Question.objects.create(
            set=q_set,
            text="Sub question for loop",
            hint="Text here",
            parent_q=question,
        )
        sub_q.save()
        Satisfy.objects.create(
            parent_question=question,
            sub_question=sub_q,
            text="",
        ).save()

        q = question
        ans = Answer.objects.create(
            question=q,
            text="ANS here",
            user=self.user,
        )
        ans.save()
        self.assertEqual(q.text, "How do you like my test question?")

        q = ans.get_next_question()
        ans = Answer.objects.create(
            question=q,
            text="ANS here",
            user=self.user,
        )
        ans.save()
        self.assertEqual(q.text, "Sub question for loop")

        q = ans.get_next_question()
        ans = Answer.objects.create(
            question=q,
            text="ANS here",
            user=self.user,
        )
        ans.save()
        self.assertEqual(q.text, "How do you like my test question?")
        q = ans.get_next_question()
        ans = Answer.objects.create(
            question=q,
            text="ANS here",
            user=self.user,
        )
        ans.save()
        self.assertEqual(q.text, "Sub question for loop")
        q = ans.get_next_question()
        self.assertIsNone(q)






class TestSatisfy(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="testconsultant@gmail.com",
            username="testconsultant@gmail.com",
            first_name="test",
            last_name="consultant",
        )
        self.consultant = Consultant.objects.create(
            user=self.user
        )
        self.consultant.save()
        self.question_set = QuestionSet.objects.create(
            consultant=self.consultant,
            name="Test Question Set",
            description="A set of questions used for testing",
        )
        self.question_set.save()

        self.question1 = Question.objects.create(
            set=self.question_set,
            text="This is level 0 q2?",
            hint="yes or no.",
        )
        self.question1.save()
        self.question = Question.objects.create(
            set=self.question_set,
            text="This is level 0 q1?",
            hint="Yes or no",
            next_question=self.question1
        )
        self.question.save()
        self.sub_q_next = Question.objects.create(
            set=self.question_set,
            text="This is the level 1 q2?",
            hint="Give some general feedback",
            next_question=self.question1,
        )
        self.sub_q_next.save()
        self.sub_q = Question.objects.create(
            set=self.question_set,
            text="This is level 1 q1?",
            hint="Give some general feedback",
            next_question=self.sub_q_next,
        )
        self.sub_q.save()
        self.satisfy1 = Satisfy.objects.create(
            parent_question=self.question,
            sub_question=self.sub_q,
            text="no",
        )
        self.satisfy1.save()
        self.sub_sub_q = Question.objects.create(
            set=self.question_set,
            text="This is level 2 q1",
            hint="Give some general feedback",
            next_question=self.sub_q.next_question,
        )
        self.sub_sub_q.save()
        self.satisfy1 = Satisfy.objects.create(
            parent_question=self.sub_q,
            sub_question=self.sub_sub_q,
            text="no",
        )
        self.satisfy1.save()

        self.question_num_parent = Question.objects.create(
            set=self.question_set,
            text="This is level 0 q2?",
            hint="yes or no.",
            sub_should_loop=True,
        )
        self.question_num_parent.save()
        self.question_num_sub = Question.objects.create(
            set=self.question_set,
            text="Looping here",
            hint="yes or no.",
            parent_q=self.question_num_parent,
        )
        self.question_num_sub.save()
        self.num_satisfy = Satisfy.objects.create(
            parent_question=self.question_num_parent,
            sub_question=self.question_num_sub,
            text="10",
        )
        self.num_satisfy.save()

    def test_satisfy(self):
        ans = Answer.objects.create(
            question=self.question,
            user=self.user,
            text="sure"
        )
        self.assertEqual(ans.get_next_question(), self.question1)

        ans = Answer.objects.create(
            question=self.question,
            user=self.user,
            text="not really"
        )
        self.assertEqual(ans.get_next_question(), self.sub_q)

        ans = Answer.objects.create(
            question=self.sub_q,
            user=self.user,
            text="no",
        )
        self.assertEqual(ans.get_next_question(), self.sub_sub_q)
        ans = Answer.objects.create(
            question=self.sub_q,
            user=self.user,
            text="yes",
        )
        self.assertEqual(ans.get_next_question(), self.sub_q_next)
        ans = Answer.objects.create(
            question=self.sub_sub_q,
            user=self.user,
            text="yes",
        )
        self.assertEqual(ans.get_next_question(), self.sub_q_next)

    def test_satisfy_num(self):
        ans = Answer.objects.create(
            question=self.question_num_parent,
            user=self.user,
            text="50"
        )
        ans.save()
        self.assertEqual(ans.get_next_question(), self.question_num_sub)

        ans = Answer.objects.create(
            question=self.question_num_parent,
            user=self.user,
            text="No number present"
        )
        ans.save()
        self.assertEqual(ans.get_next_question(), None)


