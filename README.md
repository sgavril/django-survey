# django-survey
A Django survey app

Following along with the project outlined here: https://mattsegal.dev/django-survey-project.html

### Overview
5 models: see https://mattsegal.dev/django-survey-project-data-model.html
1. Survey
2. Survey has one or more Question
3. Question has one or more Option
4. Survey has one or more Submission
5. Submission has one or more Answer
    - Answer has exactly one Option

5 forms: see https://mattsegal.dev/django-survey-project-wireframes.html
1. Answer survey
2. Create survey
3. Edit survey
4. Add question to survey
5. Add option to a new question
- Additional: sign up and log-in

12 views <-> 12 templates: also from https://mattsegal.dev/django-survey-project-wireframes.html
- GET all surveys (survey list)
- GET survey by id?
- POST survey
- PATCH survey (edit survey)
- POST question (add question to survey)
- POST options (add options to a new question)
- GET survey details