"""
Models for the survey app.
"""
from django.contrib.auth.models import User
from django.db import models

class Survey(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=255)

class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    answer = models.ForeignKey(Option, on_delete=models.CASCADE)