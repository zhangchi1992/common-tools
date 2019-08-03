import fcntl
import subprocess


class FLOCK(object):
    def __init__(self, name):
        self.fobj = open(name, 'w')
        self.fd = self.fobj.fileno()

    def lock(self):
        try:
            fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except:
            return False


if __name__ == "__main__":
    url = 'http://www.baidu.com'
    locker = FLOCK('hello')
    flag = locker.lock()
    if flag:
        subprocess.Popen(['disktool', 'upload', '-u', url])
    else:
        exit(0)

