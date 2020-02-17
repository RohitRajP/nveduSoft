from tkinter import *
import vlc
import pyttsx3
import os
from multiprocessing import Process, Value
from playsound import playsound

# declaring global variables
###################################################################################################################################

# holds the list of files in current directory
dirFiles = []

# initializing player variable for vlc
player = None


# initializing TKinter object to construct emulator
window = Tk()

# holds the current mode selected
modes = ["audiobooks", "study", "music"]

# holds the current mode index
modeIndex = 0

# declaring callback functions to perform actions from processes
#####################################################################################################################################

# reads out the different modes on MODE button click
def sayMode(event):
    global modeIndex, modes
    if modeIndex == 0:
        modeIndex = 1
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/study.mp3")
    elif modeIndex == 1:
        modeIndex = 2
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/music.mp3")
    elif modeIndex == 2:
        modeIndex = 0
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/audioBooks.mp3")
        
def moveIntoDir(event):
    global modeIndex, modes
    if modeIndex == 0:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInAudioBooks.mp3")
    elif modeIndex == 1:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInStudy.mp3")
    elif modeIndex == 2:
        os.system("mpg123 " + "/home/rrj/Projects/NVEdu/audioSamples/operationMode/youAreInMusic.mp3")

# main function implementation
#####################################################################################################################################

if __name__ == "__main__":

    # declaring buttons and their callbacks
    #######################################
    # mode button
    modeBtn = Button(window, text="Mode", fg='Black', height=11,width=56)
    # reverse button
    reverseBtn = Button(window, text="Reverse", fg='Black', height=8, width=26)
    # forward Button
    forwardBtn = Button(window, text="Forward", fg='Black',height=8, width=26)
    # cancel Button
    cancelBtn = Button(window, text="Cancel", fg='Black',height=6, width=26)
    # ok Button
    okBtn = Button(window, text="OK", fg='Black',height=6, width=26)

    # placing main buttons
    #######################################
    modeBtn.place(x=10, y=130)
    reverseBtn.place(x=10, y=335)
    forwardBtn.place(x=250, y=335)
    cancelBtn.place(x=10,y=10)
    okBtn.place(x=250,y=10)

    # binding functionality to each button
    #######################################
    # setting mode button to say the different modes on single press
    modeBtn.bind('<Button-1>', sayMode)
    okBtn.bind('<Button-1>', moveIntoDir)

    # intializing the simulator window
    #######################################
    window.title('NVEDU Demo')
    window.geometry("500x500")
    window.mainloop()