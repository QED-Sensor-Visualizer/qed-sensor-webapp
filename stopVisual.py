from scripts import sCall

def closePorts():
    sCall("sudo fuser -k 3000/tcp")
    sCall("sudo fuser -k 8086/tcp")

def stopMinikube():
    print("Close Minikube?")
    answer=input().upper()
    if "Y" in answer:
    	sCall("minikube stop")

if __name__ == '__main__':
    closePorts()
    stopMinikube()
