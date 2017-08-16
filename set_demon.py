#!/usr/bin/python
#coding=utf-8
#设置为守护进程

import os,sys,commands,time

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """set daemonize """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed (%d) %s\n " %(e.errno, e.strerror))
        sys.exit(0)
    
    os.setsid()
    os.chdir('.')
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed (%d) %s\n " %(e.errno, e.strerror))
        sys.exit(0)
    
    if not stderr:
        stderr = stdout
    si = file(stdin, "r")
    so = file(stdout, "w+")
    se = file(stderr, "a+")
    pid = str(os.getpid())
    print "start with pid :[%s]" % pid
    fp = open("pid","w")
    print >> fp, pid
    fp.close()
    sys.stderr.flush()
    
    sys.stdout.flush()
    sys.stderr.flush()
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def main():
    daemonize(stdout='../log/stdout.log', stderr='../log/stderr.log')
    
    cmd = "ls" 
    while 1:
        (status, ret) = commands.getstatusoutput(cmd)
        print status
        print ret      
        time.sleep(10)

if __name__ == "__main__":
    main()
