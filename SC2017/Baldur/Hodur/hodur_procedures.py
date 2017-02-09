# Hodur Vessel Procedures Library


def deorbit():

import krpc
from time import sleep

# Connection

try:
    print('Connecting to server as: Emergency Deorbit')
    conn = krpc.connect(name='Emergency Deorbit')
except krpc.error.NetworkError:
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

# turn to retrograde

# try main engine

# try backup engine

# try emergency RCS

# burn until ap or pe less then 30km