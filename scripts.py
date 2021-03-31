import os
import signal
import subprocess as sb


def sCall(cmd):
    return sb.run(cmd, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)


def sReturn(cmd):
    return sb.check_output(cmd, stdout=sb.PIPE,shell=True, preexec_fn=os.setsid)


def sOpen(cmd):
    return sb.Popen(cmd, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)


def sKill(pro):
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
