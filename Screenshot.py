#for image processing, install Pillow 
#pip install Pillow
import pyautogui  #pip install PyAutoGUI
import datetime

def takeScreenshot():
    pic_loc = "screenshot/"
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    img = pyautogui.screenshot()
    img.save(f"{pic_loc}screenshot-{time_stamp}.png")