import cv2, requests
import numpy as np
import threading
from skimage import io
import tkinter as tk

ip = "192.168.212.11"

KeyA = False
KeyD = False
KeyW = False
KeyS = False


randomText = open("Text.txt", "r").read().split("\n")

randomTextIndex = 0

listing = []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Speed = 50
        self.title("Hello World")
        self.geometry("300x300")
        self.resizable(False, False)

        self.label = tk.Label(self, text="Hello World")
        self.label.pack()

        self.label2 = tk.Label(self, text="")
        self.label2.pack()

def ArrowUp(e):
    P = {
        "Pitch": 5,
        "Roll": 0,
        "Yaw": 0,
        "Velocity": 100,
        "Units": "position"
    }
    r = requests.post(f"http://{ip}/api/head", params=P)
    print(r.text)

def ArrowDown():
    P = {
        "Pitch": -5,
        "Roll": 0,
        "Yaw": 0,
        "Velocity": 100,
        "Units": "position"
    }
    r = requests.post(f"http://{ip}/api/head", params=P)
    print(r.text)

def ArrowLeft():
    P = {
        "Pitch": 0,
        "Roll": 0,
        "Yaw": 5,
        "Velocity": 100,
        "Units": "position"
    }
    r = requests.post(f"http://{ip}/api/head", params=P)
    print(r.text)

def ArrowRight():
    P = {
        "Pitch": 0,
        "Roll": 0,
        "Yaw": -5,
        "Velocity": 100,
        "Units": "position"
    }
    r = requests.post(f"http://{ip}/api/head", params=P)
    print(r.text)

def ResetHead():
    P = {
        "Pitch": 0,
        "Roll": 0,
        "Yaw": 0,
        "Velocity": 100,
        "Units": "position"
    }
    r = requests.post(f"http://{ip}/api/head", params=P)
    print(r.text)

def keyDown(e):
    global KeyA, KeyD, KeyW, KeyS
    global randomText, randomTextIndex
    print(e.char)
    if(e.char == "a"):
        KeyA = True
    elif(e.char == "d"):
        KeyD = True
    elif(e.char == "w"):
        KeyW = True
    elif(e.char == "s"):
        KeyS = True
    elif(e.char == "q"):
        listing.append("q")
        app.destroy()
    elif(e.char == "f"):
        Slower()
    elif(e.char == "r"):
        Faster()
    elif(e.char == "t"):
        randomTextIndex = randomTextIndex + 1
        if(randomTextIndex >= len(randomText)):
            randomTextIndex = 0
        app.label2.config(text=f"Random Text: {randomText[randomTextIndex]}")

    elif(e.char == "g"):
        randomTextIndex = randomTextIndex - 1
        if(randomTextIndex < 0):
            randomTextIndex = len(randomText) - 1
        app.label2.config(text=f"Random Text: {randomText[randomTextIndex]}")

    elif(e.char == "8"):
        ArrowUp(e)
    elif(e.char == "2"):
        ArrowDown()
    elif(e.char == "4"):
        ArrowLeft()
    elif(e.char == "6"):
        ArrowRight()
    elif(e.char == "5"):
        ResetHead()

    elif(e.char == ' '):
        Speak()


def checkLoop():
    global KeyA, KeyD, KeyW, KeyS

    while True:
        if(listing != []):
            exit()
        try:
            if(KeyA and not KeyW and not KeyD and not KeyS):
                f = left()
            elif(KeyD and not KeyW and not KeyA and not KeyS):
                f = right()
            elif(KeyW and not KeyA and not KeyD and not KeyS):
                f = forward()
            elif(KeyS and not KeyA and not KeyD and not KeyW):
                f = reverse()
            elif(KeyA and KeyW and not KeyD and not KeyS):
                f = LeftForward()
            elif(KeyD and KeyW and not KeyA and not KeyS):
                f = RightForward()
            elif(KeyA and KeyS and not KeyD and not KeyW):
                f = LeftReverse()
            elif(KeyD and KeyS and not KeyA and not KeyW):
                f = RightReverse()
            else:
                f = stop()
            if("LeftTrackSpeed" in f):
                r = requests.post(f"http://{ip}/api/drive/track", params=f)
            else:
                r = requests.post(f"http://{ip}/api/drive", params=f)
            print(f)
            print(r.text)
        except:
            print("Error")
            continue
        # time.sleep(0.1)

def keyUp(e):
    global KeyA, KeyD, KeyW, KeyS

    if(e.char == "a"):
        KeyA = False
    elif(e.char == "d"):
        KeyD = False
    elif(e.char == "w"):
        KeyW = False
    elif(e.char == "s"):
        KeyS = False

def Slower():
    app.Speed = app.Speed - 5
    if(app.Speed < 0):
        app.Speed = 0
    app.label.config(text=f"Speed: {app.Speed}")
    print("Slower")

def Faster():
    app.Speed = app.Speed + 5
    if(app.Speed > 100):
        app.Speed = 100
    app.label.config(text=f"Speed: {app.Speed}")
    print("Faster")

def left():
    print("Left")
    return {"LeftTrackSpeed": -app.Speed, "RightTrackSpeed": app.Speed}

def right():
    print("Right")
    return {"LeftTrackSpeed": app.Speed, "RightTrackSpeed": -app.Speed}

def forward():
    print("Forward")
    return {"LinearVelocity": (app.Speed), "AngularVelocity": 0}
    return {"LeftTrackSpeed": app.Speed, "RightTrackSpeed": app.Speed}

def LeftForward():
    print("LeftForward")
    return {"LeftTrackSpeed": app.Speed/1.5, "RightTrackSpeed": app.Speed*1.5}

def RightForward():
    print("RightForward")
    return {"LeftTrackSpeed": app.Speed*1.5, "RightTrackSpeed": app.Speed/1.5}

def LeftReverse():
    print("LeftReverse")
    return {"LinearVelocity": -(app.Speed / 2), "AngularVelocity": -(app.Speed/4)}

def RightReverse():
    print("RightReverse")
    return {"LinearVelocity": -(app.Speed / 2), "AngularVelocity": (app.Speed/4)}

def reverse():
    print("Reverse")
    return {"LinearVelocity": -(app.Speed / 2), "AngularVelocity": 0}

def stop():

    return {"RightTrackSpeed": 0, "LeftTrackSpeed": 0}


def Speak():
    f = requests.post(f"http://{ip}/api/tts/speak", params={"Text": randomText[randomTextIndex]})
    print(f.text)

def Camera():
    url = f"http://{ip}/api/cameras/fisheye?base64=false&cacheBreak={np.random.randint(0, 100000)}"
    global listing
    while True:
        if(listing != []):
            break
        try:
            image = io.imread(url)
        except:
            print("Couldnt get image")
            continue
        image = cv2.resize(image, (1280, 720))
                
        cv2.imshow('test', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()




if __name__ == '__main__':
    app = App()
    app.bind("<KeyPress>", keyDown)
    app.bind("<KeyRelease>", keyUp)
    # app.bind("<Up>", ArrowUp)
    # app.bind("<Down>", ArrowDown)
    # app.bind("<Left>", ArrowLeft)
    # app.bind("<Right>", ArrowRight)
    threading.Thread(target=checkLoop, args=(listing)).start()
    threading.Thread(target=Camera).start()
    app.mainloop()
    