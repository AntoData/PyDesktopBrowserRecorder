# PyDesktopBrowserRecorder
 This project allows you to record your desktop or the browser during an automated test using selenium's webdriver
 
 You just have to make the following import:
 from videoRecorder import desktopBrowserRecorder
 
 Then you create a DesktopBrowserRecorder object, you have two modes. You have to provide the following parameters:
 obj = desktopBrowserRecorder.DesktopBrowserRecorder(folder,encoding)
 - folder: Folder where we want to create the folder that will contain the videos for our recording session
 - encoding: Encoding of the video. We only assure that using ".mp4" will work
 This way, when you start the recording session, the desktop will be recorded until we stop the recording session
 
 But you can also provide a third parameter:
  obj = desktopBrowserRecorder.DesktopBrowserRecorder(folder,encoding,driver)
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
  
  Also, in the package config we include the module checkConfiguration.py:
  This module contains the method checkConfiguration() that reads the file importedModules.txt in the same folder and checks the modules listed in every line of this file have been installed in our environment. These modules are needed to run this project successfully. In case one is not installed, the function will tell you how to install it. Also, the module calls this function so you would only have to run this module, but you could also call this function from your program if needed
  
  Also we have a folder test that includes a module called demo.py that you can run to see how this works and how this was tested.
 
