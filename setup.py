'''
Created on 1 mar. 2020

@author: ingov
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ingov", # Replace with your own username
    version="0.0.1",
    author="Anto P",
    author_email="ingovanpe@gmail.com",
    description="This project allows you to record your desktop or a browser controlled by Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/AntoData/PyDesktopBrowserRecorder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)