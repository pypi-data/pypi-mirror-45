cimport PyHiSLIP

import struct 

ctypedef class MessageHeader:
    cdef short prologue #"HS"
    cdef unsigned char messageType
    cdef unsinged char controlCode
    cdef unsinged int messageParameter
    cdef unsinged long payloadLength
    cdef char data[]
    cdef char raw

    def unpack(self,data):
        self.prologue=data[:2] # ASCII "HS"
        self.messageType=data[2] # Message Type 
        self.controlCode=data[3] # Control Code
        self.messageParameter=data[4:8] # Message Parameter
        self.payloadLength=long(data[8:16]) # PayloadLength (8byte int:
        self.data=data[16:] # len(self.data) should be self.payloadLength

    def pack(self):
        self.raw=struct.pack(
            "2cccil",
            self.prologue,
            self.messageType,
            self.controlCode,
            self.messageParameter,
            self.payloadLength)
        self.raw +=self.data # extend binary payload

    @classmethod
    def build_packet(cls, mtype, cc, mparm, payload):
        self.raw=struct.pack(
            "2cccil",
            "HS",
            mtype,
            cc,
            mparm,
            len(payload))
        self.raw +=pyload
        retrun self.raw

    @classmethod
    def unpack_packet(raw):
        obj=cls().unpack(raw)
        return obj
    
import socket

cdef HiSLIPDevice:
     def __init__(self,server, port=HiSLIPPort):
         self.syncport=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.ssyncport=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.syncport.connect((server,port))
         self.syncport.send(self.buidmessage(HiSLIPMessageType.Initialize, 0,))


     def Open(self):
         pass

     def Write(self):
         pass

     def Read(self):
         pass

     def ReadSTB(self):
         pass

     def Clear(self):
         pass

     def Lock(self):
         pass

     def AsynLock(self):
         pass

     def Unlock(self):
         pass

     
