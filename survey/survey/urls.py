"""
URL configuration for survey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from survey import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('admin/', admin.site.urls),
    path('register', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='survey/login.html', next_page='survey-list'), name='login'),
    # Surveys
    path('list/', views.get_surveys, name='survey-list'),
    path('create-survey/', views.create_survey, name='create-survey'),
    path('survey/<int:survey_id>/', views.survey_detail, name='survey-detail'),
    path('edit-survey/<int:survey_id>/', views.edit_survey, name='edit-survey'),
    # Questions
    path('question/<int:question_id>/', views.question_detail, name='question-detail'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit-question'),
    path('start_survey/<int:survey_id>/', views.start_survey, name='start-survey'),
    path('submit_survey/<int:survey_id>/<int:submission_id>', views.submit_survey, name='submit-survey'),
    path('survey-thanks', views.thank_user, name='survey-thanks'),
]
