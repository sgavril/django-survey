"""
Views for the survey app.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateSurveyForm, AddQuestionForm, AddOptionForm, AnswerForm, BaseAnswerFormSet
from .models import Survey, Question, Submission

# temporary
import json

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

@login_required
def get_surveys(request):
    """
    Logged in user can view all of their surveys.
    """
    # TODO: display statistics of a survey
    surveys = Survey.objects.filter(creator=request.user).annotate(num_submissions=Count('submission'))
    context = {'surveys': surveys}
    print(context)
    return render(request, 'survey/list.html', context)

@login_required
def survey_detail(request, survey_id):
    """View a survey."""
    survey = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/survey_detail.html', {'survey': survey})

@login_required
def create_survey(request):
    """Logged in user can create new survey."""
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

@login_required
def delete_survey(request):
    """Logged in user can delete a survey."""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == 'POST':
        survey.delete()

    return redirect("list")
        
@login_required
def edit_survey(request, survey_id):
    """Logged in user can add questions to a survey."""
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

def start_survey(request, survey_id):
    """Take a survey."""
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        submission = Submission.objects.create(survey=survey)
        return redirect("submit-survey", survey_pk=survey_id, sub_id=submission.pk)
    
    return render(request, "survey/survey_start.html", {"survey": survey})

def submit_survey(request, survey_id, submission_id):
    """Submit a survey. This is the implementation found at 
        https://github.com/MattSegal/django-survey/blob/master/survey/views/survey.py
    """
    # Survey retrieval and validation
    survey = get_object_or_404(Survey, pk=survey_id)
    submission = Submission.objects.filter(survey=survey)
    questions = survey.question_set.all()
    options = [q.option_set.all() for q in questions]

    # 2. Formset generation for questions
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm,
                                    extra=len(questions),
                                    formset=BaseAnswerFormSet)
    # 3. Process submitted answers
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option=form.cleaned_data["option"],
                        submission_id=submission_id
                    )
                    submission.save()
                return redirect("survey-thanks", pk=survey_id)
        else:
            formset = AnswerFormSet(form_kwargs=form_kwargs)

        question_forms = zip(questions, formset)
        return render(request, "survey/submit.html",
                    {"survey": survey, "question_forms": question_forms, "formset": formset},
                )

    # Demonstrative purposes: convert dict to JSON and return
    data = {'message': 'Debug Info',
            'questions': [q.question for q in questions]}
    return HttpResponse(json.dumps(data), content_type="application/json")


    # Process submitted answers

    # Render survey form
    # for question in questions:
    #     print(question)

# def submit_survey_basic()

# def submit_survey_refactored(request, survey_id, submission_id):
#     # 1. Retrieve objects
#     survey, submission = get_survey_and_submission(survey_id, submission_id)

#     # 2. Initialize formset
#     AnswerFormSet, form_kwargs = initialize_answer_formset(survey)