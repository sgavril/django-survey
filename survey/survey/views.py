"""
Views for the survey app.
"""
from django.http import HttpResponse
from django.shortcuts import render
from .models import Survey

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
    pass

def edit_survey(request):
    pass

def add_question(request):
    pass