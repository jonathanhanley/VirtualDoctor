import hashlib
import sys
from difflib import SequenceMatcher

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    code = models.CharField(max_length=5, null=True, default="")


# Create your models here.
class Consultant(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=5, null=True, default="")

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super(Consultant, self).save(*args, **kwargs)

    def generate_code(self):
        string = f"{self.user.email} - {self.user.first_name} - {self.user.last_name} - {self.user.username}"
        code = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return code[:5]


class QuestionSet(models.Model):
    consultant = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    created = models.DateField(auto_now=True)


class Question(models.Model):
    set = models.ForeignKey('QuestionSet', on_delete=models.CASCADE)
    text = models.TextField(max_length=1028, null=True, blank=True)
    hint = models.TextField(max_length=1028, null=True, blank=True)
    next_question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, related_name="+")
    sub_should_loop = models.BooleanField(default=False)
    parent_q = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.text}"


class Satisfy(models.Model):
    parent_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="parent_question")
    sub_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="sub_question")
    text = models.CharField(max_length=255, null=True, blank=True)

    def _ans_is_int(self, answer):
        try:
            return int(answer)
        except ValueError:
            return False
        except TypeError:
            return False

    def is_satisfied(self, answer):
        if self._ans_is_int(answer):
            answer = self._ans_is_int(answer)
            if self.parent_question.sub_should_loop:
                return sys.maxsize

        ratio = SequenceMatcher(None, self.text, answer).ratio()
        return ratio


class Loop(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    loop_amount = models.IntegerField()

    def is_done(self, user):
        answers = Answer.objects.filter(user=user, question=self.question)
        return len(answers) >= self.loop_amount


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=1028, null=True, blank=True)

    def _ans_is_int(self):
        try:
            return int(self.text)
        except ValueError:
            return False
        except TypeError:
            return False

    def save(self, *args, **kwargs):
        if self.question.sub_should_loop:
            loop_num = self._ans_is_int()
            if loop_num:
                sub_q = Question.objects.filter(
                    parent_q=self.question,
                ).last()
                Loop.objects.create(
                    question=sub_q,
                    loop_amount=loop_num,
                    user=self.user,
                ).save()

        super(Answer, self).save(*args, **kwargs)

    def get_next_question(self):
        loops = Loop.objects.filter(
            question=self.question,
            user=self.user,
        )
        if len(loops):
            loop = loops.last()
            if not loop.is_done(self.user):
                sub_questions = Satisfy.objects.filter(parent_question=self.question)
                if sub_questions:
                    sub_question = sub_questions[0]
                    if sub_question.sub_question:
                        return sub_question.sub_question
                    return sub_question.parent_question
                return self.question

            sub_qs = Question.objects.filter(parent_q=self.question)
            if sub_qs:
                sub_q = sub_qs[0]
                if len(Answer.objects.filter(user=self.user, question=sub_q)) < loop.loop_amount:
                    return sub_q
        sub_question_tests = Satisfy.objects.filter(parent_question=self.question)
        max_test = None
        max_score = -1
        for test in sub_question_tests:
            score = test.is_satisfied(self.text)
            if score > max_score:
                max_score = score
                max_test = test

        if max_score > 0.3:
            return max_test.sub_question

        if self.question.parent_q and self.question.parent_q.sub_should_loop and self.question.next_question is None:
            loop = Loop.objects.filter(
                question=self.question.parent_q,
                user=self.user,
            ).last()

            if loop and (loop.is_done(self.user) or len(Answer.objects.filter(question=self.question.parent_q, user=self.user)) == loop.loop_amount):
                return self.question.parent_q.next_question

            return self.question.parent_q
        return self.question.next_question

    def __str__(self):
        return f"{self.question} - {self.text} - {self.user.username}"

