import pyautogui as pag
import time


mousetime = 0.5
screenwidth = pag.size().width
screenheight = pag.size().height
midpoint = screenheight/2
leftx = int(screenwidth*0.025)
rightx = int(screenwidth*0.975)

def moveandclick(nscreens,timedelay):
    time.sleep(timedelay)
    while True:
        pag.moveTo(rightx,midpoint,duration=mousetime)
        for i in range(nscreens):
            pag.click()
            time.sleep(timedelay)
        pag.moveTo(leftx,midpoint,duration=mousetime)
        for i in range(nscreens):
            pag.click()
            time.sleep(timedelay)

if __name__=="__main__":
    moveandclick(3,5)
