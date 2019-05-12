from django import forms
from .models import MyInfo, MyQuestion
from django.contrib.auth.models import User

class MyInfoForm(forms.ModelForm):
    user = User()
    class Meta:
        model = MyInfo
        fields = ['name', 'age', 'sex','address', 'image','highSchoolName', 'highSchoolAdmDate', 'highSchoolGradDate',
                 'univSchoolName', 'univSchoolAdmDate', 'univSchoolGradDate',
                 'certName', 'certGetDate', 'compName', 'compTask', 'compFirstDate',
                 'compLastDate']

class MyQuestionForm(forms.ModelForm):
    user = User()
    class Meta:
        model = MyQuestion
        fields = ['title', 'content', 'message']