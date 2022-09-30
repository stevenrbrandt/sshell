import os
from here import here

seq = 1

class tmpfile:
    def __init__(self):
        global seq
        self.fname = os.path.join("/tmp",f"tfile-{seq}-{os.getpid()}.out")
        self.fd = open(self.fname,"w")
        self.is_open = True
        seq += 1
        #here("open",depth=2)
    def flush(self):
        assert self.is_open
        return self.fd.flush()
    def write(self,msg):
        assert self.is_open
        return self.fd.write(msg)
    def close(self):
        #here("close",depth=0)
        assert self.is_open
        self.is_open = False
        self.fd.flush()
        return self.fd.close()
    def fileno(self):
        return self.fd.fileno()
    def isatty(self):
        return self.fd.isatty()
    def getvalue(self):
        if self.is_open:
            #here("close",depth=0)
            self.close()
        with open(self.fname,"r") as fd:
            return fd.read()
        os.unlink(self.fname)
    def __repr__(self):
        return f"tmp({self.fname},{self.is_open})"

if __name__ == "__main__":
    t = tmpfile()
    print("t:",t)
    t.close()
