import os
import subprocess
import datetime

def runExcute(path):
    print(os.getcwd())
    exePath = os.getcwd() + path
    print(exePath)
    # os.startfile(exePath)
    subproc = subprocess.Popen([exePath,"auturun"])
    subproc.wait()
    return

def preExcute():
    workingDir = "\\..\\python_gui\\"
    excuteFile = workingDir + "convertPython.bat"
    runExcute(excuteFile)

    
    output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(output_date)
    return


