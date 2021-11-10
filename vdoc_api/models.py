import hashlib
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
    next_question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.text}"


class Satisfy(models.Model):
    parent_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="parent_question")
    sub_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="sub_question")
    text = models.CharField(max_length=255, null=True, blank=True)


class Loop(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    loop_amount = models.IntegerField()

    def is_done(self, user):
        answers = Answer.objects.filter(user=user, question=self.question)
        return len(answers) >= self.loop_amount


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=1028, null=True, blank=True)
    def _similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_next_question(self):
        sub_question_tests = Satisfy.objects.filter(parent_question=self.question)
        max_test = None
        max_score = -1
        for test in sub_question_tests:
            score = self._similar(self.text, test.text)
            if score > max_score:
                max_score = score
                max_test = test

        if max_score > 0.3:
            return max_test.sub_question

        return self.question.next_question

