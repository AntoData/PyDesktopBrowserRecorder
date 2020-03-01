'''
Created on 29 feb. 2020

@author: ingov

This module allows you to check if you have installed all packages/modules needed to run this
project.
You can whether run this module or use the function created here.
'''
__version__="0.1.4"
#We need to import pathlib to get  the path of our current project
import pathlib

def checkConfiguration():
    """ 
    This function loads the file importedModules.txt where the modules needed to use this
    project are listed. We try to import them and if they are not installed we print a message. 
  
    Parameters: 
        None
          
    Returns: 
        None 
    """
    #We build the path for the file where we listed the modules needed for this project
    configFile = str(pathlib.Path(__file__).parent.absolute())+"/importedModules.txt"
    #We open this file
    file = open(configFile)
    #We go through every line in the file because each module is listed in a new line
    for line in file.read().splitlines():
        try:
            #We try to import that module
            __import__(line)
        except ImportError:
            #If the module was not installed, we print a message indicating it and asking you
            #to install it
            print("Module {0} is not install".format(line))
            print("Try in command line: pip install {0}".format(line))
    
#We execute this method so you can run this module and get which modules you need
checkConfiguration()