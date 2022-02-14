import subprocess
import hashlib
import sys
import os
import grp
import pwd
import shutil
import fileinput

def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root
        
def run (command):
    command = list(iterFlatten(command))
    print(command)
    process = subprocess.Popen(command, shell=False, 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    STDOUT = process.stdout.read()
    STDERR = process.stderr.read()
    response = {'STDOUT':STDOUT, 'STDERR':STDERR}
    process.communicate()
    return response

def sha256FileChecksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def sha256BufferChecksum(buffer):
    sha256 = hashlib.sha256()
    sha256.update(buffer)
    return sha256.hexdigest()

def writeBuffer(buffer, filePath):
    file = open(filePath, "w")
    file.write(buffer)
    file.close()

def installFile(filePath, buffer, user, group, mode, info):
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    if os.path.isfile(filePath):
        digest = sha256FileChecksum(filePath)
        newDigest = sha256BufferChecksum(buffer.encode())
        if digest == newDigest:
            if info:
                print('unmodified :', filePath)
        else:
            if info:
                print('updated :', filePath)
            writeBuffer(buffer, filePath)
        
        stat_info = os.stat(filePath)
        oldUser = pwd.getpwuid(stat_info.st_uid)[0]
        oldGroup = grp.getgrgid(stat_info.st_gid)[0]
        if oldUser == user and oldGroup == group:
            pass
        else:
            shutil.chown(filePath, user, group)
            os.chmod(filePath, mode)
    else:
        if info:
            print('created :', filePath)
        writeBuffer(buffer, filePath)
        shutil.chown(filePath, user, group=group)
        os.chmod(filePath, mode)
    pass

def installElem(root, element, info):
    filePath = root + element['file']
    buffer = element['data']
    user = element['user']
    group = element['group']
    mode = element['mode']
    installFile(filePath, buffer, user, group, mode, info)

def replace(filename, text_to_search, replacement_text):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')
    return

#replace('/etc/hosts', 'raspberry', 'host')
