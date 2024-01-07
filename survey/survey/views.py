"""
Views for the survey app.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import CreateSurveyForm
from .models import Survey

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

def get_survey_by_id(request):
    pass

def create_survey(request):
    if request.method == 'POST':
        form = CreateSurveyForm(request.POST)
        if form.is_valid():
            survey_obj = form.save()
            # return render(request, 'survey/survey_created.html')
            return redirect('survey_detail', survey_id=survey_obj.id)
        else:
            form = CreateSurveyForm()

    return render(request, 'survey/create_survey.html', {'form': form})


def edit_survey(request):
    pass

def add_question(request):
    pass