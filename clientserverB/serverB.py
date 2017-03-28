import socket
from os import getcwd, listdir
from hashlib import sha1
from commands import getstatusoutput

def lls():
    toSend = ""
    dirs = listdir(getcwd())
    for f in dirs:
        toSend = toSend + f + ' '
    return toSend

def longlistFunc():
    path = getcwd()
    var = getstatusoutput("ls -l " + path + " | awk '{print $9, $5, $6, $7, $8}'")
    var1 = ""
    var1 = var1 + '' + var[1]
    return var1

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failure in creating socket : '
    print str(msg)

try:
    s.bind(('localhost', 8000))
except socket.error, msg:
    print 'Problem in binding : '
    print str(msg)

s.listen(10)
print 'Server up and running!'

while True:
    conn, addr = s.accept()
    reqCommand = conn.recv(1024)
    print 'ServerB>' + str(reqCommand)
    string = reqCommand.split(' ')

    cmdName = string[0]
    if(cmdName != 'exit' and cmdName != 'lls'):
        cmdArg = string[1]
    if (cmdName == 'exit'):
        break
    elif (cmdName == 'lls'):
        toSend = lls()
        conn.send(toSend)
    elif (cmdArg == 'longlist'):
        var1 = longlistFunc()
        conn.send(var1)
    elif (cmdName == 'hash'):
        if(cmdArg == 'verify'):
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
            conn.send(hasher.hexdigest())
            print 'Hash Successful'
        elif (cmdArg == 'checkall'):
            BLOCKSIZE = 65536
            hasher = sha1()

            dirs = listdir(getcwd())
            for f in dirs:
                conn.send(f)
                try:
                    afile = open(f, 'rb')
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)
                except IOError:
                    print "File Error"
                conn.send(hasher.hexdigest())
                print 'Hash Successful'
    else:
        string = reqCommand.split(' ')
        cmdArgs = string[0]
        if(len(string) > 1):
            reqFile = string[1]
            if (cmdArgs == 'FileUpload'):
                # print "checkin"
                file_to_write = open(reqFile, 'wb')
                si = string[2:]
                for p in si:
                    p = p + " "
                    file_to_write.write(p)
                    print p
                while True:
                    data = conn.recv(1024)
                    print data
                    if not data:
                        break
                    file_to_write.write(data)
                file_to_write.close()
                print 'File Received'
            elif (cmdArgs == 'download'):
                # print "download"
                with open(reqFile, 'rb') as file_to_send:
                    for data in file_to_send:
                        conn.sendall(data)
                    print 'File Sent'
    conn.close()
s.close()
