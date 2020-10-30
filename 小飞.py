import sys#加载程序库
import time
import pyttsx3
import os
from random import randint
from threading import Thread
from playsound import playsound
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

engine=pyttsx3.init()
engine.setProperty("voice","zh")
 
talkdic=dict()#对话字典
talk0=["nihaoma","woyeshi","woshuaima","yiqinuli","woxihuanni"]
talk1=["我很好,你呢","嗯","当然,魏宁是最帅的","嗯,一起努力,加油","我也喜欢你"]
for i in range(len(talk0)):
    talkdic[talk0[i]]=talk1[i]
randtalk=["加油","今天是个好日子","别忘了学习英语"]
   
class 小飞(QWidget):#这是我最，最，最好的朋友，我叫她阿飞：）
    _isTracking = False
    _startPos = None
    _endPos = None
    def __init__(self):
        super().__init__()
        self.initUI() 
        self.speak("一起努力变得更优秀吧")     
    def initUI(self):

        self.shape=dict()#加载精灵动画集
        shape_name=["stance","crouch","dizzy","jump","run","walkback","walkforward","stance0"]#不知道为什么win无法加载
        for name in shape_name:
            self.shape[name]=QMovie("Pictures/yuri/"+name+".gif") 

        self.setGeometry(1700,700,210,300)#初始化窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.g=True

        self.label0=QLabel(self)#亲密度标签
        self.label0.setGeometry(0,0,210,20)      
        self.label0.setStyleSheet("color:rgb(0,0,255)")
        f=open("亲密度","r")
        self.x=f.read()
        f.close()
        y="当前亲密度:"+self.x
        print(y)
        self.label0.setText(y)

                
        self.pre=QMovie("Downloads/小飞.gif")#精灵动画
        self.now=self.pre
        self.label=QLabel(self)
        self.label.setGeometry(0, 20,210,280)        
        self.label.setMovie(self.pre)
        self.pre.start()
        
        self.timer =QTimer(self)#时间事件
        self.timer.start(1000*60)
        self.timer.timeout.connect(self.start)
        self.show()
    def start(self):
        self.label.setMovie(self.shape["jump"])
        self.shape["jump"].start()
        Thread(target=self.togethere, daemon=True).start()
        self.to_now()    
    def togethere(self):
        self.x=str(1+int(self.x))       
        y="亲密度:"+self.x
        print("我和小飞更亲密了：）       "+y)
        self.label0.setText(y)
        #self.show()   
        f=open("亲密度","w")
        f.write(self.x)
        f.close()
        #playsound("Downloads/up.wav")
        t=time.localtime(time.time())#定时事件
        if t[3]==17:
            self.speak("该吃午饭了")         
        elif t[3]==18 and t[4]<=1:
            print(0)
            self.speak("现在是郑州时间六点")
        elif t[3]==21 and t[4]<=1:
            print(1)
            for i in range(5):
                self.speak("该跑步了")
        elif t[3]>=22 and t[3]<=23:
            for i in range(5):
                self.speak("该准备睡觉了")
        else:
            print(2)
            self.speak(randtalk[randint(0,len(randtalk)-1)])    
        
    def geometry_go(self):#清除残影
        if self.g:
            self.setGeometry(1700,700,210,299)
            self.g=False
        else:
            self.setGeometry(1700,700,210,300)
            self.g=True
    
    def speak(self,text):#skill-speak
        self.text=text
        Thread(target=self.speak0,daemon=True).start()                     
    def speak0(self):
        engine.say(self.text)
        engine.runAndWait()
    
    def sing(self,song):
        self.song=song
        Thread(target=self.sing0,daemon=True).start()
    def sing0(self):
        playsound(self.song)

    def source(self,cmd):
        self.cmd=cmd
        Thread(target=self.source0,daemon=True).start()
    def source0(self):
        os.system(self.cmd)        
    def change(self,shape):
        self.geometry_go()               
        self.label.setMovie(self.shape[shape])
        self.shape[shape].start()
        self.now=self.shape[shape]
    def back(self):
        self.geometry_go()
        self.label.setMovie(self.pre)
        self.pre.start()
        self.now=self.pre
    def to_now(self):
        Thread(target=self.to_now0,daemon=True).start()
    def to_now0(self):
        time.sleep(1)
        self.geometry_go()
        self.label.setMovie(self.now)
        self.now.start()
    def talk(self):#与精灵对话
        text,ok=QInputDialog.getText(self,"talk","talking with me")
        text=str(text)
        if ok:
            if text in talkdic:
                self.speak(talkdic[text])
            else:
                self.speak("你说的啥呀,我听不懂") 
    def getText(self):#技能事件监听
        text,ok=QInputDialog.getText(self,"skill","do the skill")
        text=str(text)
        if ok:
            if text=="sing":          
                self.sing("Downloads/moon.mp3")
            elif text in self.shape:
                self.change(text)
            elif text=="back":
                self.back()
            elif text=="self":
                self.source("gedit ~/小飞.py")
            else:
                self.speak("sorry,没有"+text)
                QMessageBox.information(self,"sorry","now do not have")

    def mouseMoveEvent(self, e: QMouseEvent): # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
        if e.button() == Qt.RightButton:
            menu = QMenu(self)
            quitAction = menu.addAction("休眠")
            aboutAction=menu.addAction("技能")
            action = menu.exec_(self.mapToGlobal(e.pos()))
            if action == quitAction:
                exit()
            if action == aboutAction:
                self.getText()
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
        if e.button() == Qt.RightButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None 
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Z:
            self.back()
        elif event.key()==Qt.Key_Space:
            self.getText()
        elif event.key()==Qt.Key_T:
            self.talk()
        elif event.key()==Qt.Key_S:
            self.speak("一起努力变得更优秀吧")
        elif event.key()==Qt.Key_R:
            self.change("run")
        elif event.key()==Qt.Key_C:
            self.source("python3 ~/小飞.py")
        elif event.key()==Qt.Key_O:
            self.source("python3 ~/小飞.py")
            exit()
        elif event.key()==Qt.Key_Escape:
            exit()
  
if __name__=="__main__":#启动虚拟精灵
    app=QApplication(sys.argv)
    小飞=小飞()
    sys.exit(app.exec_())

