from django.db import models
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    _, ext = os.path.splitext(filename)
    username = instance.user.username
    return '{}/{}'.format(username, username + ext)

class MyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to=user_directory_path)
    
    # 고등학교
    highSchoolName = models.CharField(max_length=100, null=True, blank=True)
    highSchoolAdmDate = models.DateField(null=True, blank=True)
    highSchoolGradDate = models.DateField(null=True, blank=True)
    
    # 대학교
    univSchoolName = models.CharField(max_length=100, null=True, blank=True)
    univSchoolAdmDate = models.DateField(null=True, blank=True)
    univSchoolGradDate = models.DateField(null=True, blank=True)
    
    # 자격증
    certName = models.CharField(max_length=100, null=True, blank=True)
    certGetDate = models.DateField(null=True, blank=True)
    
    # 경력
    compName = models.CharField(max_length=100, null=True, blank=True)
    compTask = models.CharField(max_length=1000, null=True, blank=True)
    compFirstDate = models.DateField(null=True, blank=True)
    compLastDate = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class MyQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    contentNum = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField(max_length=5000, null=True, blank=True)
    commitCount = models.IntegerField(null=True, blank=True)
    lastCommitDate = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    

class QuestionLog(models.Model):
    myQuestion = models.ForeignKey(MyQuestion, on_delete=models.CASCADE)
    commitNo = models.IntegerField()
    commitDate = models.DateField(auto_now=True)