import notify2
import time
import pyautogui
import pyperclip
import sys
import pytiled_parser

notify2.init('')

def getGrid():
    notify2.Notification('','Select upper left corner').show()
    time.sleep(3)
    x1,y1=pyautogui.position()
    notify2.Notification('','Select two cells right down').show()
    time.sleep(3)
    x2,y2=pyautogui.position()
    dx,dy=(x2-x1,y2-y1)
    dx=dx//2
    dy=dy//2
    sx=x1+dx/2
    sy=y1+dy/2
    return (dx,dy,sx,sy)

def browserCmd(cmd):
    pyautogui.press("f6")
    pyautogui.write("javascript:")
    pyperclip.copy(cmd)
    pyautogui.hotkey('ctrl','v')
    # pyautogui.typewrite("javascript:document.getElementsByTagName('button')[1].click();")
    time.sleep(1)
    pyautogui.press("enter")
