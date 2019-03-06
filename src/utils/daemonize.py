import os
import sys

def daemonize(pidfile=None):  
    # flush io
    sys.stdout.flush()  
    sys.stderr.flush()  
    # Do first fork.  
    try:  
        pid = os.fork()  
        if pid > 0: sys.exit(0) # Exit first parent.  
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))  
        sys.exit(1)         
        # Decouple from parent environment.  
        # os.chdir("/")  
        os.umask(0)  
        os.setsid()  
        # Do second fork.  
    try:  
        pid = os.fork()  
        if pid > 0: sys.exit(0) # Exit second parent.  
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))  
        sys.exit(1)
    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open('/dev/null', 'r')
    so = se = open('./nohup.out', 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())  

    pid = str(os.getpid())  

    if pidfile: open(pidfile, 'w+').write("%s\n" % pid)