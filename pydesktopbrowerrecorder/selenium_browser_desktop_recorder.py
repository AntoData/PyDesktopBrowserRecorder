"""
Contains the basic functionality that records the videos using an instance of
webdriver provided by the user that we clone or the whole desktop if not
provided

Classes:
        SeleniumBrowserRecorder

Exceptions:
        SessionStartedException
        NoSessionStartedException

"""
from __future__ import annotations

import io
import threading
import os
import time
from datetime import datetime
import numpy as np
from selenium import webdriver
import imageio
import pyautogui
from PIL import Image


class SeleniumBrowserRecorder:
    """
    Creates one or several videos using frames taking from a browser using
    Selenium webdriver or the desktop

    :ivar driver: Instance of webdriver we use to record a browser session
    (if None we record the desktop)
    :type driver: webdriver.remote.webdriver.WebDriver
    :ivar __folder: Contains the path where we will create folders that contain
     the videos created during the session
    :type __folder: str
    :ivar __session_path: Contains the path to the folder where we save the
    videos of the recording session
    :type __session_path: str
    :ivar __encoding: Encoding of the video
    :type __encoding: str
    :ivar __keep_recording: Flag to keep adding frames to the video or stop the
     session
    :type __keep_recording: bool
    :ivar frame: Frame to be added to the video
    :type frame: np.typing.ArrayLike
    :ivar __thread: Contains the thread that will start adding frames to the
    video
    :type __thread: threading.Thread
    """

    def __init__(self, folder: str, encoding: str, driver: webdriver = None):
        """
        Class constructor

        :param folder: Contains the path where we will create folders that
        contain the videos created during the session
        :type folder: str
        :param encoding: Encoding of the video
        :type encoding: str
        :param driver: Instance of webdriver we use to record a browser session
         (if None we record the desktop)
        :type driver: webdriver.remote.webdriver.WebDriver
        """
        self.driver: webdriver.remote.webdriver.WebDriver = driver
        self.__folder: str = folder
        self.__session_path: str = ""
        self.__encoding: str = encoding
        self.__keep_recording: bool = False
        self.frame: np.typing.ArrayLike | None = None
        self.__thread: threading.Thread | None = None

    # noinspection PyTypeChecker
    def __thread_take_screenshot(self):
        """
        Takes a screenshot to be added to the video in a parallel thread

        :return: None
        """
        # We first create a string var that contains the path where to
        # allocate the frame we will be taking every number of ms.
        # This will be added to the video while the variable
        # __keep_recording is true (we are recording)
        #
        # If we provided a webdriver (the variable driver is not None)
        # the screenshot will be taken from the browser
        # by selenium.  Otherwise, it will be taken by pyautogui of
        # the desktop.
        #
        # That screenshot will be saved in the attribute frame to be
        # added as a frame to the video.

        while self.__keep_recording:
            if self.driver is not None:
                self.frame = np.asarray(Image.open(io.BytesIO(self.driver
                                                   .get_screenshot_as_png())))
            else:
                self.frame = np.asarray((pyautogui.screenshot()))

            time.sleep(1 / 25)  # 20fps, sleep for 1/25 secs.

    def __build_writer(self) -> imageio.core.format.Writer:
        """
        Creates the object that will be used to build our video frame by frame

        :return: Video writer
        :rtype: imageio.core.format.Writer
        """
        # We first get the current date and time which we join that to
        # the attribute encoding (which contains the extension our
        # video file should have) to get the name of the video file
        # for this video session we are recording
        #
        # Then we create the video writer that will build the video
        # frame by frame.  Finally, we return that object
        now: datetime = datetime.now()
        file_name: str = now.strftime("%d-%m-%Y_%H-%M-%S") + self.__encoding

        writer: imageio.core.format.Writer = imageio.\
            get_writer(self.__session_path + "/" + file_name, fps=20)
        return writer

    def __main_thread_recording_session(self):
        """
        Builds the video in the main thread adding frame by frame

        :return: None
        """
        # First we build the folder that will contain our video (or
        # videos in case our recording session crashes
        # so this module starts another session immediately).
        #
        # We do this using the current date and time and the attribute
        #  __folder where the user set which folder
        # should contain our recording sessions.  Then, we create it
        now: datetime = datetime.now()
        self.__session_path: str = self.__folder + "\\" + now.\
            strftime("%d-%m-%Y_%H-%M-%S")
        try:
            os.mkdir(self.__session_path)
        except (NotADirectoryError, Exception) as e:
            print(e)

        # We create the thread that will take the screenshots for the video
        screenshots_thread: threading.Thread = threading.\
            Thread(target=self.__thread_take_screenshot, args=())

        writer = self.__build_writer()  # To get the video writer

        screenshots_thread.start()  # Start taking screenshots

        # While the flag __keep_recording is True, we will keep adding
        # frames to our video or create a new video if case our
        # recording session crashes.
        #
        # If the frame is not None, which means we already have a
        # frame, we add it to the video
        while self.__keep_recording:
            try:
                if self.frame is not None:
                    writer.append_data(self.frame)
            except (BufferError, Exception):
                # In case there is an exception when trying to add the
                # frame to the video we close the writer. After that,
                # we create a new one immediately.
                #
                # Then, we try to add the new frame to the new video
                # created if t is not None
                #
                # This is the best way to prevent problems when the
                # size of a browser changes. In that case, we just
                # start a new video to keep recording
                writer = self.__build_writer()
                if self.frame is not None:
                    writer.append_data(self.frame)

            time.sleep(1 / 25)  # 20fps, sleep for 1/25 secs

        # Once the flag __keep_recording is False we stop our recording
        # session, so we close our video writer and stop the thread
        # taking the screenshots
        writer.close()
        screenshots_thread.join()

    def start_recording_session(self):
        """
        Kicks off the recording session (main thread and screenshots thread)

        :return: None
        """
        if self.__keep_recording:  # Session already started, exception
            raise SessionStartedException("There is an existing running "
                                          "recording session for this object")
        self.__keep_recording = True  # New recording session

        # We create the main __thread that runs the algorithm and assign
        # it to attribute __thread
        #
        # Then, we start the thread to start the session
        self.__thread = threading.\
            Thread(target=self.__main_thread_recording_session, args=())
        self.__thread.start()

    def stop_recording_session(self):
        """
        Stops the recording session

        :return: None
        """
        if not self.__keep_recording:  # No session, so exception
            raise NoSessionStartedException("There is no current recording "
                                            "session")

        # We set the flag __keep_recording to false to stop the
        # recording process and stop the thread
        #
        # We also set the attribute __thread to None as the recording
        # session is finished
        self.__keep_recording = False
        self.__thread.join()
        self.__thread: threading.Thread | None = None


class SessionStartedException(Exception):
    """
    Custom exception that is raised when we try to start a session when there
    is already one running
    """
    pass


class NoSessionStartedException(Exception):
    """
    Custom exception that is raised when we try to stop a session but there is
     not one in process
    """
    pass


if __name__ == "__main__":
    from selenium.webdriver.chrome.service import Service
    # Selenium webdriver instance
    chrome = Service("./chromedriver.exe")
    # noinspection PyArgumentList
    browser = webdriver.Chrome(service=chrome)
    # Creating instance of SeleniumBrowserRecorder
    browser_recorder = SeleniumBrowserRecorder("./", ".mp4", browser)

    try:
        # Starting recording session
        browser_recorder.start_recording_session()

        # Browsing and performing automated tasks
        browser.get("https://www.google.es/")
        browser.find_element(webdriver.common.by.By.ID, "L2AGLb").click()
        query = browser.find_element(webdriver.common.by.By.NAME, "q")
        query.send_keys("pypi stats privateattributesdecorator")
        query.send_keys(webdriver.common.keys.Keys.ENTER)
        time.sleep(10)
        result = browser.find_element(webdriver.common.by.By.XPATH,
                                      "//h3[contains(text(), "
                                      "'PrivateAttributesDecorator - PyPI')]")\
            .click()

    finally:
        # We always stop the recording session
        browser_recorder.stop_recording_session()
        browser.close()

    desktop_recorder = SeleniumBrowserRecorder("./", ".mp4")

    try:
        # Starting recording session
        desktop_recorder.start_recording_session()

        time.sleep(30)

    finally:
        # We always stop the recording session
        desktop_recorder.stop_recording_session()
