import os
import logging
import shutil
log = logging

def isFile(path):
    return os.path.isfile(path)
def isFolder(path):
    return os.path.isdir(path)

def createFolder(path):
    try:
        os.makedirs(path)
        return True
    except OSError as e:
        log.error("Error when create folder: ", str(e))
    return False

def writeFileConfig(path, content):
    try:
        f = open(path, "w")
        f.write(content)
        f.close()
        os.chmod(path, 0o755)
        return True
    except Exception as e:
        log.error(e)
        return False
        

def clearInFolder(folder):
    ret = True
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            ret = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return ret
    
'''
Remove all ts file and m3u8 file
'''

def cleatTsM3u8FileInFolder(folder):
    ret = True
    for filename in os.listdir(folder):
        print(filename)
        filename = filename.rstrip()
        if filename.endswith('.ts') or filename.endswith('.m3u8'):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                ret = False
                log.error('Failed to delete %s. Reason: %s' % (file_path, e))
    return ret

'''
For test
'''
def main():
    print(cleatTsM3u8FileInFolder('/home/map/tmp/2'))
    exit(0)
    print(clearInFolder('/home/map/tmp'))
    exit(0)
    print(isFile("uploadHls.py"))
    print(isFile("uploadHlas.py"))
    print(isFolder("/home/map/tmp"))
    print(isFolder("/home/map/tmp2"))
    print(createFolder("/home/map/tmp/tmp"))
    print(createFolder("/home/map/tmp3/tmp"))
    print(createFolder("/home/map/tmp/tmp"))
    print(createFolder("/usr/abc"))

if __name__ == "__main__":
    main()
    

