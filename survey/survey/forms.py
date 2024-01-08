from django import forms
from .models import Survey, Question, Option

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']

class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['survey', 'question']
        print("hmmm")

class AddOptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question', 'option']