from django import forms
from .models import Survey, Question, Option

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']

class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class AddOptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option']

class AnswerForm(forms.Form):
    """
    Define structure and behavior of a single form within a formset.
    Dynamically create a form based on provided options.
    """
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = {(o.pk, o.option) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["options"] = option_field

    # class Meta:
    #     fields = ['answer']

class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['options'] = kwargs['options'][index]
        return kwargs