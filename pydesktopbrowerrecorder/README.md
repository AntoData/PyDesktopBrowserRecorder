# PyDesktopBrowserRecorder
 This project allows you to record your desktop or the browser during an automated test using selenium's webdriver
 
 You just have to make the following import:
 from pydesktopbrowerrecorder import selenium_browser_desktop_recorder
 
 Then you create a SeleniumBrowserRecorder object, you have two modes. You have to provide the following parameters:
 obj = selenium_browser_desktop_recorder.SeleniumBrowserRecorder(folder,encoding)
 - folder: Folder where we want to create the folder that will contain the videos for our recording session
 - encoding: Encoding of the video. We only assure that using ".mp4" will work
 This way, when you start the recording session, the desktop will be recorded until we stop the recording session
 
 But you can also provide a third parameter:
  obj = selenium_browser_desktop_recorder.SeleniumBrowserRecorder(folder,encoding,driver)
  - driver: A webdriver object
  In this case, we will record only the browser window(s) that are being controlled by that webdriver object
  
  To start the recording session once we build the object we only have to use this method:
  obj.startRecordingSession()
  And our object will start recording in a parallel thread
  
  To stop the recording session we only have to:
  obj.stopRecordingSession()
  The video will be saved and the threads finished
  
  NOTE: If we are recording a browser and the size of it changes, we will stop the current video and start a new one with the new
  size of the window
 
NOTE: This was developed using the following versions of the following external libraries:
- imageio_ffmpeg = 0.4.5 
- numpy~=1.22.2 
- imageio==2.15.0 
- PyAutoGUI~=0.9.53 
- selenium~=4.1.0 
- Pillow~=9.0.1