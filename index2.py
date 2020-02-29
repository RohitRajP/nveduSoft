from tkinter import *
import vlc
import pyttsx3
import os
from multiprocessing import Process, Value
from playsound import playsound

# declaring global variables
####################################################################################################################################
# holds the list of files in current directory
dirFiles = []

# holds the current index in the directory
dirFilesIndex = -1

# initializing player variable for vlc
player = None

# initializing TKinter object to construct emulator
window = Tk()

# holds the current mode selected
modes = ["audiobooks", "study", "music"]

# holds the current context
# modeContext - just changed the mode
# inMode - inside a mode 
context = "modeContext"

# holds the current mode index
modeIndex = -1

# holds the root address of the directory structure
rootAddress = ""

# declaring callback functions to perform actions from processes
####################### ##############################################################################################################
# reads out the different modes on MODE button click
def sayMode(modeIndex):
    if modeIndex == 1:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/study.mp3")
    elif modeIndex == 2:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/music.mp3")
    elif modeIndex == 0:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/audioBooks.mp3")

# reads out the current mode
def sayCurrentMode(modeIndex):
    if modeIndex == 1:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInStudy.mp3")
    elif modeIndex == 2:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInMusic.mp3")
    elif modeIndex == 0:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInAudioBooks.mp3")

# say words using test to speech
def sayWords(dialog):
    engine = pyttsx3.init() # object creation
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 120)
    engine.setProperty('voice', voices[11].id)  # changes the voice
    engine.say(dialog)
    engine.runAndWait()

# declaring process instances for each action
#####################################################################################################################################
sayModeProc = Process(target=sayMode)
sayCurrentModeProc = Process(target=sayCurrentMode)
sayWordsProc = Process(target=sayWords)

# declaring middleware functions for execution of code that requires common memory
#####################################################################################################################################
def modeBtnPressed():
    global modeIndex, modes
    if modeIndex == 0:
        modeIndex = 1
    elif modeIndex == 1:
        modeIndex = 2
    elif modeIndex == 2:
        modeIndex = 0
    elif modeIndex == -1:
        modeIndex = 0

# callbackHUB to distribute the calls appropriately
#####################################################################################################################################
def callBackHub(buttonCode):
    global sayModeProc, sayCurrentModeProc, sayWordsProc,context, modeIndex, modes, rootAddress, dirFiles, dirFilesIndex
    # terminating all running processes
    if sayModeProc.is_alive():
        sayModeProc.terminate()
    elif sayCurrentModeProc.is_alive():
        sayCurrentModeProc.terminate()
    elif sayWordsProc.is_alive():
        sayWordsProc.terminate()

    if buttonCode == "modeBtn":
        # setting the current execution context
        context = "modeContext"
        # changing directory to root
        os.chdir(rootAddress)
        # calling method to modify the modeIndex
        modeBtnPressed()
        # changing current dire
        sayModeProc = Process(target=sayMode,args=(modeIndex,))
        sayModeProc.start()
    elif buttonCode == "okBtn":
        # deciding action based on context
        if context == "modeContext":
            # changing context to show that we are now inside a mode
            context = "inMode"
            # changing current directory
            os.chdir(rootAddress+"/"+modes[modeIndex])
            # creating process instance
            sayCurrentModeProc = Process(target=sayCurrentMode, args=(modeIndex,))
            sayCurrentModeProc.start()
    elif buttonCode == "forwardBtn":
        # executing script only for the appropriate context
        if context == "inMode":
            # updating directory listing
            dirFiles = os.listdir()
            # updating the dirFilesIndex
            if dirFilesIndex < len(dirFiles)-1:
                dirFilesIndex += 1
            else:
                dirFilesIndex = 0
            # creating process to say the word
            sayWordsProc = Process(target=sayWords, args=(dirFiles[dirFilesIndex].split(".")[0],))
            sayWordsProc.start()
    elif buttonCode == "backwardBtn":
        # executing script only for the appropriate context
        if context == "inMode":
            # updating directory listing
            dirFiles = os.listdir()
            # updating the dirFilesIndex
            if dirFilesIndex > 0:
                dirFilesIndex -= 1
            else:
                dirFilesIndex = len(dirFiles) - 1
            # creating process to say the word
            sayWordsProc = Process(target=sayWords, args=(dirFiles[dirFilesIndex].split(".")[0],))
            sayWordsProc.start()

# main function implementation
#####################################################################################################################################
if __name__ == "__main__":

    # setting the root address
    rootAddress = os.getcwd()

    # declaring buttons and their callbacks
    #######################################
    # mode button
    modeBtn = Button(window, text="Mode", fg='Black', height=11,width=56, command=lambda: callBackHub("modeBtn"))
    # reverse button
    reverseBtn = Button(window, text="Reverse", fg='Black', height=8, width=26, command=lambda: callBackHub("backwardBtn"))
    # forward Button
    forwardBtn = Button(window, text="Forward", fg='Black',height=8, width=26, command=lambda: callBackHub("forwardBtn"))
    # cancel Button
    cancelBtn = Button(window, text="Cancel", fg='Black',height=6, width=26)
    # ok Button
    okBtn = Button(window, text="OK", fg='Black',height=6, width=26, command=lambda: callBackHub("okBtn"))

    # placing main buttons
    #######################################
    modeBtn.place(x=10, y=130)
    reverseBtn.place(x=10, y=335)
    forwardBtn.place(x=250, y=335)
    cancelBtn.place(x=10,y=10)
    okBtn.place(x=250,y=10)

    # intializing the simulator window
    #######################################
    window.title('NVEDU Demo')
    window.geometry("500x500")
    window.mainloop()