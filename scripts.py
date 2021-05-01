import os
import re
import signal
import json
import requests as req
import subprocess as sb

from kubipy.utils import minipy

def sCall(cmd):
    return sb.run(cmd, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)


def sReturn(cmd):
    return re.sub("[^!-~]+","",sb.Popen(cmd, stdout=sb.PIPE,shell=True).communicate()[0].decode("utf-8")).strip()


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

def getPod(name):
    return sReturn("kubectl get pods --namespace default | grep "+name+"|awk '{print $1}'")

def runInPod(name,cmd):
    #print("kubectl exec "+getPod(name)+" "+cmd)
    return sReturn("kubectl exec "+getPod(name)+" -- bash -c '"+cmd+"'")

def uploadDashboard():
    with open("grafanaData/header.json") as f: header = json.load(f)
    with open("grafanaData/dashboard.json") as f: dashboard = json.load(f)
    p=req.post("http://admin:password@localhost:3000/api/dashboards/db", headers=header, json=dashboard)
    return(p)