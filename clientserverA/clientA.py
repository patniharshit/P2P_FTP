import socket, sys
from os import getcwd, listdir
from hashlib import sha1
from commands import getstatusoutput

HOST = 'localhost'
PORT = 8000

def put(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    string = commandName.split(' ')
    inputFile = string[1]
    try:
        file_to_send = open(inputFile, 'rb')
        for data in file_to_send:
            socket1.send(data)
    except IOError:
        print "File Error"
        return 0
    socket1.close()
    print 'Upload Finished'
    return


def get(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    string = commandName.split(' ')
    inputFile = string[1]
    try:
        file_to_write = open(inputFile, 'wb')
        while True:
            data = socket1.recv(1024)
            if not data:
                break
            file_to_write.write(data)
    except IOError:
        print "File could not be opened"
        return 0
    file_to_write.close()
    socket1.close()
    print 'Download Finished'
    return

def verify(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    hashValServer = socket1.recv(1024)

    string = commandName.split(' ')
    BLOCKSIZE = 65536
    hasher = sha1()
    try:
        afile = open(string[2], 'rb')
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    except IOError:
        print "File Error"
        return 0
    hashValClient = hasher.hexdigest()
    print 'hashValServer = ' + str(hashValServer)
    print 'hashValClient = ' + str(hashValClient)
    if hashValClient != hashValServer:
        msgprint = 'Changes detected'
    else:
        msgprint = 'Chnages not detected'
    socket1.close()
    print msgprint
    return


def checkall(commandName):
    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)

    string = commandName.split(' ')
    BLOCKSIZE = 65536
    hasher = sha1()
    # print "funct"
    while True:
        # print "inside loop"
        f=socket1.recv(1024)
        try:
            afile = open(f, 'rb')
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        except IOError:
            print "File Error"
            return 0
        hashValClient = hasher.hexdigest()
        hashValServer=socket1.recv(1024)

        print f + '\n' + 'from server : ' + hashValServer + '\n' + 'from client : ' + hashValClient

        if hashValClient == hashValServer:
            print 'No updates'
        else:
            print 'Update Available'
        if not f:
            break
    socket1.close()
    return

def index(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    path = socket1.recv(1024)
    rslt = path.split('\n')
    for f in rslt[1:]:
        print f

    socket1.close()
    return

def ls():
    path = getcwd()
    dirs = listdir(path)
    for f in dirs:
        print f

def lsServer(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    fileStr = socket1.recv(1024)
    fileList = fileStr.split(' ')

    for i in range(len(fileList)-1):
        print fileList[i]
    socket1.close()
    return

while True:
    sys.stdout.write ('ClientA >> ')
    inputCommand = sys.stdin.readline().strip()
    string = inputCommand.split(' ')
    cmdName = string[0]
    if (cmdName == 'exit'):
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        socket1.send(inputCommand)
        socket1.close()
        break
    elif (cmdName == 'ls'):
        ls()
    elif (cmdName == 'lls'):
        lsServer('lls')
    elif cmdName == 'FileUpload':
        put(inputCommand)
    elif cmdName == 'hash':
        string = inputCommand.split(' ')
        if string[1] == 'verify':
            verify(inputCommand)
        elif string[1] == 'checkall':
            checkall(inputCommand)
    elif cmdName == 'index':
        index(inputCommand)
    elif cmdName == 'download':
        get(inputCommand)
