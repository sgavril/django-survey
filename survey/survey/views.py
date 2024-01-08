"""
Views for the survey app.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateSurveyForm, AddQuestionForm, AddOptionForm
from .models import Survey, Question

def landing_page(request):
    return render(request, 'survey/landing_page.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('survey-list')
    else:
        form = UserCreationForm()
    return render(request, 'survey/register.html', {'form': form})

def get_surveys(request):
    """
    Retrieve and display a list of all Survey objects.
    """
    surveys = Survey.objects.all()
    context = {'surveys': surveys}
    return render(request, 'survey/list.html', context)

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/survey_detail.html', {'survey': survey})

def create_survey(request):
    if request.method == 'POST':
        form = CreateSurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            return redirect('survey-list')
            # survey_obj = form.save()
            # return render(request, 'survey/survey_created.html')
            # return redirect('survey_detail', survey_id=survey_obj.id)
    else:
        form = CreateSurveyForm()

    return render(request, 'survey/create_survey.html', {'form': form})

def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, creator=request.user)
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('survey-list')
    else:
        form = AddQuestionForm()
    
    return render(request, 'survey/edit_survey.html', {'form': form, 'survey': survey})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'survey/question_detail.html', {'question': question})

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AddOptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
            return redirect('question-detail', question_id=question.pk)
    else:
        form = AddOptionForm()

    return render(request, 'survey/edit_question.html', {'form': form, 'question': question})