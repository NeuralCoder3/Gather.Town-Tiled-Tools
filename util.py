import notify2
import time
import pyautogui
import pyperclip
import sys
import pytiled_parser

ignoreNotify=False

try:
    notify2.init('')
except:
    ignoreNotify=True

def getGrid():
    notify('Select upper left corner')
    time.sleep(3)
    x1,y1=pyautogui.position()
    notify('Select four cells right down')
    time.sleep(10)
    x2,y2=pyautogui.position()
    dx,dy=(x2-x1,y2-y1)
    dx=dx//4
    dy=dy//4
    sx=x1+dx/2
    sy=y1+dy/2
    return (dx,dy,sx,sy)

def browserCmd(cmd):
    pyautogui.press("f6")
    pyperclip.copy(":")
    pyautogui.write("javascript")
    pyautogui.hotkey('ctrl','v')
    # pyautogui.write("javascript:")
    pyperclip.copy(cmd)
    pyautogui.hotkey('ctrl','v')
    # pyautogui.typewrite("javascript:document.getElementsByTagName('button')[1].click();")
    time.sleep(1)
    pyautogui.press("enter")

def writeInput(field,text):
    browserCmd("document.getElementById('"+field+"').focus();")
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','a')
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl','v')

def notify(text):
    if ignoreNotify:
        print(text)
    else:
        notify2.Notification('',text).show()
