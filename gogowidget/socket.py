import base64
import bz2
import hashlib
import json
import os

from utils.path import cd
from utils.storage import compress, decompress


def recvsize(socket):
    "Receive a message containing the size."
    data = b''
    last = socket.recv(1)
    while last != b':':
        data += last
        last = socket.recv(1)

    return int(data)


def recvbig(socket):
    size = recvsize(socket)
    msg = socket.recv(size)
    return msg


def sendbig(socket, msg):
    header = str(len(msg)).encode() + b':'
    socket.sendall(header + msg)
