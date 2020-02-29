from videoRecorder import desktopBrowserRecorder
from selenium import webdriver
import time

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
recorder = desktopBrowserRecorder.DesktopBrowserRecorder(dir_path,".mp4")
recorder.startRecordingSession()
driver = webdriver.Chrome()
recorder2 = desktopBrowserRecorder.DesktopBrowserRecorder(dir_path,".mp4",driver)
driver.get("http://www.google.es")
i = 0
while i < 60:
    time.sleep(1)
    if i == 30:
        recorder2.startRecordingSession()
    i+=1
recorder.stopRecordingSession()

i = 0
while i < 30:
    time.sleep(1)
    i+=1
    
recorder2.stopRecordingSession()
driver.quit()