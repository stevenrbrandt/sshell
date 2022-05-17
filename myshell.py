from shell import shell, interactive
import os
import sys
from colored import colored
from here import here
from shutil import which

# This example limits shell access to a handful of commands
# and gives the user access only to files in the workpath
workpath = os.path.join("/tmp",os.environ["USER"])

def allow_access(fn):
    fn = os.path.abspath(fn)
    if fn == workpath or fn.startswith(workpath+"/"):
        return True
    else:
        print(colored(f"Access of file '{fn}' not allowed.","red"))
        return False

def allow_set_var(var, val):
    if var in ["USER","LOGNAME","HOME","PATH"]:
        print(colored(f"Setting of var '{var}' is not allowed.","red"))
        return False
    else:
        return True

allowed_cmds = dict()

def add_cmd(nm,*flags):
    w = which(nm)
    allowed_cmds[w] = flags

class filename():
    def __init__(self):
        pass
    def ok(self,f):
        return allow_access(f)

class regex:
    def __init__(self,r):
        self.r = r
    def ok(self,a):
        return re.match(r"^"+self.r+r"$", a)

Any = regex(".*")

add_cmd("which",Any)
add_cmd("ls","-l","-s","-ls","-a",filename())
add_cmd("file",filename())
add_cmd("ps",Any)
add_cmd("mkdir","-p",filename())
add_cmd("rmdir",filename())
add_cmd("rm","-r",filename())
add_cmd("exit",regex("[0-9]+"))
add_cmd("date",Any)
add_cmd("echo",Any)
add_cmd("cal",regex("[0-9]+"))
add_cmd("pwd")

def allow_cmd(args):
    allow = True
    if args[0] in allowed_cmds:
        for a in args[1:]:
            found = False
            for p in allowed_cmds[args[0]]:
                if type(p) == str:
                    if p == a:
                        found = True
                        break
                elif p.ok(a):
                    found = True
                    break
            if not found:
                allow = False
                break
    else:
        allow = False

    if allow:
        return True
    else:
        print(colored(f"Command '{args}' is not allowed.","red"))
        return False

if __name__ == "__main__":

    # Ensure the workpath exists
    os.makedirs(workpath,exist_ok=True)

    # Start in the workpath
    os.chdir(workpath)

    # Create the shell
    s = shell()

    # Limit chdir
    s.allow_cd = allow_access

    # Limit read by the < mechanism
    s.allow_read = allow_access

    # Limit write by the > mechansim
    s.allow_write = allow_access

    # Limit append by the >> mechanism
    s.allow_append = allow_access

    # Limit shell variables that may be set
    s.allow_set_var = allow_set_var

    # Limit commands that may be run
    s.allow_cmd = allow_cmd

    if len(sys.argv) == 1:
        rc = interactive(s)
        exit(rc)
    else:
        for f in sys.argv[1:]:
            with open(f,"r") as fd:
                s.run_text(fd.read())