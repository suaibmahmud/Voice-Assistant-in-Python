import os
import subprocess

def openApp(text):
    if text == "browser":
        path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        os.startfile(path)
        
