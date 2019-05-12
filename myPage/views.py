from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from .models import MyInfo, MyQuestion, QuestionLog
from .forms import MyInfoForm, MyQuestionForm
from .utils.pythonToWord import makeCertification

import os
import shutil

def main(request):
    return render(request, "myPage/main.html")

def base(request, userId):
    adminUser = User.objects.get(username="admin")
    try:
        user = User.objects.get(username=userId)
    except Exception:
        user = User.objects.get(username="admin")
    myquestionList = list(map(str, user.myquestion_set.all()))
    excludeMyQuestionList = [str(question) for question in MyQuestion.objects.filter(user=adminUser) if str(question) not in myquestionList]
    context = dict()
    context['myquestionList'] = myquestionList
    context['excludeMyQuestionList'] = excludeMyQuestionList
    return render(request, "myPage/base.html", context)

def addQuestion(request, userId):
    questionTitle = request.POST['questionTitle']
    contentNum = int(request.POST['contentNum'])
    user = User.objects.get(username=userId)
    new_q = MyQuestion(user=user, title=questionTitle, contentNum=contentNum)
    new_q.save()
    return HttpResponseRedirect(reverse('myPage:base', args=(userId, )))

def deleteQuestion(request, userId, questionTitle):
    user = User.objects.get(username=userId)
    MyQuestion.objects.filter(user=user).filter(title=questionTitle).delete()
    return HttpResponseRedirect(reverse('myPage:base', args=(userId, )))

def deleteOldImage(userName, imagePath):
    absolutePath = "/".join(imagePath.split("/")[:-1])
    if os.path.isdir(absolutePath):
        shutil.rmtree(absolutePath)

def myInfo(request, userId):
    user = User.objects.get(username=userId)
    if request.method == 'POST':
        myinfo = MyInfo.objects.get(user=user)
        form = MyInfoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = MyInfoForm(data=request.POST, instance=myinfo)
            if 'image' in request.FILES:
                deleteOldImage(user.username, myinfo.image.path)
                myinfo.image = request.FILES['image']
                form = MyInfoForm(data=request.POST, instance=myinfo, initial={"image":myinfo.image})
            form.save()
        return render(request, 'myPage/myInfo.html', {'form':form})
    else:
        try:
            myinfo = MyInfo.objects.get(user=user)
        except Exception:
            myinfo = MyInfo(user=user)
            myinfo.save()
        tempInitDict = model_to_dict(myinfo)
        tempInitDict['image'] = myinfo.image
        form = MyInfoForm(initial=tempInitDict)
    return render(request, 'myPage/myInfo.html', {'form':form})

def questionInfo(request, userId, questionTitle):
    user = User.objects.get(username=userId)
    if request.method == 'POST':
        questionForm = MyQuestionForm(request.POST)
        if questionForm.is_valid():
            newQuestionForm = questionForm.cleaned_data
            MyQuestion.objects.filter(user=user, title=questionTitle).update(**newQuestionForm)
            return render(request, 'myPage/questionInfo.html', {'form':questionForm})
    else:
        try:
            myQuestionInfo = MyQuestion.objects.get(user=user, title=questionTitle)
        except Exception:
            myQuestionInfo = MyQuestion(user=user, title=questionTitle, commitCount=0)
            myQuestionInfo.save()
        questionForm = MyQuestionForm(initial=model_to_dict(myQuestionInfo))
    return render(request, 'myPage/questionInfo.html', {'form':questionForm})

def downloadDoc(request, userId):
    user = User.objects.get(username=userId)
    myinfo = MyInfo.objects.get(user=user)
    context = model_to_dict(myinfo)
    context['image'] = os.path.join('media', context['image'].path)
    context['filePath'] = 'media/{username}/{username}.docx'.format(username=user.username)
    for key, val in context.items():
        context[key] = str(val)
    document = makeCertification(**context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + context['filePath']
    document.save(response)
    return response

def saveQuestion(request, userId, questionTitle):
    pass





