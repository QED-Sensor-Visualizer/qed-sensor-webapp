import os
import signal
import subprocess as sb

from kubipy.utils import minipy

def sCall(cmd):
    return sb.run(cmd, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)


def sReturn(cmd):
    return sb.Popen(cmd, stdout=sb.PIPE,shell=True).communicate()[0].decode("utf-8")


def sOpen(cmd):
    return sb.Popen(cmd, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)


def sKill(pro):
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def getMinikube():
    cluster=minipy(False)
    cluster.install()
    cluster.start()
    sCall("kubectl config view --raw >~/.kube/config")
    sCall("minikube start")