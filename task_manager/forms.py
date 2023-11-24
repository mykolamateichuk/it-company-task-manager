from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Worker


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "task_type", "assignees"]
        widgets = {
            "deadline": DateInput()
        }


class RegisterWorkerForm(UserCreationForm):

    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "username",
                  "position", "password1", "password2"]


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "username",
                  "position"]


POSITION_CHOICES = (
    ("1", "Project Manager"),
    ("2", "Developer"),
    ("3", "Designer"),
    ("4", "QA"),
    ("5", "DevOps"),
)


class WorkerFilterForm(forms.Form):
    position = forms.ChoiceField(
        choices=POSITION_CHOICES,
        required=False,
        initial="",
        label=""
    )
