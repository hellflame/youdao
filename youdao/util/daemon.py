import sys
import os
import time
import signal
import atexit


def freopen(f, mode, stream):
    oldf = open(f, mode)
    oldfd = oldf.fileno()
    newfd = stream.fileno()
    os.close(newfd)
    os.dup2(oldfd, newfd)


def write_pid_file(pid_file, pid):
    import fcntl
    import stat

    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT,
                     stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        print(e.strerror)
        return -1
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1
    flags |= fcntl.FD_CLOEXEC
    r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    assert r != -1
    # There is no platform independent way to implement fcntl(fd, F_SETLK, &fl)
    # via fcntl.fcntl. So use lockf instead
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        if r:
            print('already started at pid %s' % r.strip())
        else:
            print('already started')
        os.close(fd)
        return -1
    os.ftruncate(fd, 0)
    os.write(fd, str(pid))

    atexit.register(clean)
    return 0


def clean():
    daemon_stop('pid_file')


def daemon_start(pid_file, log_file):

    def handle_exit(signum, _):
        if signum == signal.SIGTERM:
            sys.exit(0)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # fork only once because we are sure parent will exit
    pid = os.fork()
    assert pid != -1

    if pid > 0:
        # parent waits for its child
        time.sleep(5)
        sys.exit(0)

    # child signals its parent to exit
    ppid = os.getppid()
    pid = os.getpid()
    if write_pid_file(pid_file, pid) != 0:
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)

    os.setsid()
    signal.signal(signal.SIG_IGN, signal.SIGHUP)
    # print('started')
    os.kill(ppid, signal.SIGTERM)

    sys.stdin.close()
    try:
        freopen(log_file, 'a', sys.stdout)
        freopen(log_file, 'a', sys.stderr)
    except IOError as e:
        print(e.strerror)
        sys.exit(1)


def daemon_stop(pid_file):
    import errno
    try:
        with open(pid_file) as f:
            buf = f.read()
            pid = int(buf.strip())
            if not buf:
                print("not running")
    except IOError as e:
        print(e.strerror)
        if e.errno == errno.ENOENT:
            # always exit 0 if we are sure daemon is not running
            print('not running')
            return
        sys.exit(1)
    pid = int(pid)
    if pid > 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                print('not running')
                # always exit 0 if we are sure daemon is not running
                return
            print(e.strerror)
            sys.exit(1)
    else:
        print('pid is not positive: %d', pid)

    # sleep for maximum 10s
    for i in range(0, 200):
        try:
            # query for the pid
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                break
        time.sleep(0.05)
    else:
        print('timed out when stopping pid %d' % pid)
        sys.exit(1)
    # print('stopped')
    os.unlink(pid_file)


def run():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 9999))
    current = 0
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            if current == 0:
                current = int(data)
            elif int(data) - current > 60:
                pid_file = '/home/hellflame/PycharmProjects/iplocate/iplocate/util/pid'
                daemon_stop(pid_file)
            else:
                os.popen("echo {} >> /tmp/test".format(data))

    sock.close()


def timer():
    import socket
    import time
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sock.sendto(str(time.time()), ('127.0.0.1', 9999))
    sock.close()

"""
if __name__ == '__main__':
    #daemon_stop('/tmp/pid')
    #daemon_start('/tmp/pid',
    #             '/tmp/log')
    #run()
    timer()

"""

