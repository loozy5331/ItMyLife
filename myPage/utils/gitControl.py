import os
import re
import sys
import shutil
from datetime import datetime

class GitControl:
    """
        console 창에 git을 다루기 위한 클래스
    """
    def __init__(self, gitPath):
        self.originPath = os.getcwd()
        self.gitPath = gitPath
        if not os.path.isdir(gitPath):
            os.makedirs(gitPath)
        
    def initGit(self):
        os.chdir(self.gitPath)
        initMessage = os.popen("git init").read()
        os.chdir(self.originPath)
        print(initMessage)

    def addGit(self):
        os.chdir(self.gitPath)
        addMessage = os.popen("git add *").read()
        os.chdir(self.originPath)
        print(addMessage)
    
    def commitGit(self, message):
        os.chdir(self.gitPath)
        commitMessage = os.popen("git commit -m \"{message}\"".format(message=message)).read()
        os.chdir(self.originPath)
        print(commitMessage)


class GitLog:
    """
        __init__(gitPath, fileName): 파일의 경로를 통해 초기화 후
        makeMessageList()를 통해 message들을 뽑아내고
        displayChange()를 통해 현재 내용과 어떤 것이 다른지 확인 가능 (확인용)
        diffContents(pivotNum, targetNum): pivotNum을 기준으로 targetNum의 내용과 어떻게 다른지 확인. 메시지는 targetNum의 것을 사용

    """
    def __init__(self, gitPath):
        """
            gitPath: git 명령을 실행할 경로
        """
        self.gitPath = gitPath
        self.originPath = os.getcwd()
        sys.path.append(self.gitPath) # 명령어를 실행할 기준 경로 설정
        self.dateList = list()
        self.messageList = list()
        self.contentList = list()

    def makeMessageList(self):
        """
            현재까지 commit한 message들을 self.messageList에 저장
        """
        os.chdir(self.gitPath)
        logs = os.popen("git log").readlines()
        os.chdir(self.originPath)
        logs = [log.strip() for log in logs] # remove \n

        print("===========<message List>==============")
        for i, line in enumerate(logs):
            if(i == 4 or (i - 4) % 6 == 0):
                self.messageList.append(line)
                print("line {}: {}".format(i, line))
            if(i == 2 or (i - 2) % 6 == 0):
                self.dateList.append(datetime.strptime(line[5:].strip(), '%a %b %d %H:%M:%S %Y %z'))
        print("======================================\n")
        print(self.dateList)
        

    def diffContents(self, pivotNum, targetNum):
        """
            pivotNum: 기준이 되는 Commit 가장 최근 것은 0
            targetNum: 확인하고 싶은 Commit 기준이 되는 pivotNum과의 차이점을 "<b></b>"로 표시해준다.
                범위를 넘어가면 에러메시지를 표시하고 종료한다.
        """
        if(targetNum >= len(self.messageList)):
            print("targetNum is out of range!")
            return
        os.chdir(self.gitPath)
        contents = os.popen("git diff --word-diff=plain HEAD~{targetNum} HEAD~{pivotNum} content.txt".format(targetNum=targetNum, 
                                                                                                            pivotNum=pivotNum))
        os.chdir(self.originPath)                                                                                
        contents = [content.strip() for content in contents] # remove \n
        contents = self.removeOtherInfo(contents)
        print("commit number : {targetNum}".format(targetNum=targetNum))
        print("message : {message}".format(message=self.messageList[targetNum - 1]))
        for content in contents:
            self.changeForAddSubPatter(content)

    def changeForAddSubPatter(self, content):
        """
            content: console에 찍힌 log 중에 한 줄
            수정을 통해 빠진 부분은 더하고, 현재 추가된 내용은 빼서 표시해준다. 
        """
        add_pattern = re.compile("\{\+(.*)\+\}")
        sub_pattern = re.compile("\[-(.*)-\]") 
        if(re.search(add_pattern, content)): # 이번에 새로 적은 내용은 빼고
            content = re.sub(add_pattern, "", content)
        if(re.search(sub_pattern, content)): # 전의 자료에서 뺀 부분은 더해주고
            content = re.sub("\[\-", "<b>", content)
            content = re.sub("\-\]", "</b>", content)
        if(len(content.strip()) == 0):
            return
        print(content)
        return content

    def displayChange(self):
        """
            모든 commit의 변경사항을 표시해준다.
            기준은 현재 commit
        """
        for i, message in enumerate(self.messageList):
            if i == 0:
                curr = 0
            else:
                curr = i-1
            next = i
            os.chdir(self.gitPath)
            contents = os.popen("git diff --word-diff=plain HEAD~{next} HEAD~{curr} content.txt".format(next=next, curr=curr)).readlines()
            os.chdir(self.originPath)
            contents = [content.strip() for content in contents]
            contents = self.removeOtherInfo(contents)
            print("commit number : {} ===============================================".format(i))
            print("message: {}".format(message))
            tempContents = list(map(self.changeForAddSubPatter, contents))
            tempContents = [content for content in tempContents if content != ""]
            print(tempContents)
            self.contentList.append("<br>".join(tempContents))
            print("\n")
        
    def removeOtherInfo(self, contents):
        """
            git diff 를 통해 얻은 다른 정보들은 제외하고 표시해준다.
            정확히는 변경한 내용에 관한 내용만.
        """
        lineNum = 0
        modifiedContents = list()
        pattern = re.compile("^@@")
        for i, content in enumerate(contents):
            if(re.search(pattern, content)):
                lineNum = i
                break
        for i in range(lineNum, len(contents)):
            modifiedContents.append(contents[i])
        return modifiedContents
            


if __name__ == "__main__":
    gitlog = GitLog("/", "hello.txt") # 현재 폴더에 hello.txt 파일의 git log 확인
    gitlog.makeMessageList()
    gitlog.displayChange()
    #gitlog.diffContents(0, 2)

    # gitcontrol = GitControl()
    # gitcontrol.initGit()
    # gitcontrol.addGit()
    # gitcontrol.commitGit("git control test for new class")
    
    
