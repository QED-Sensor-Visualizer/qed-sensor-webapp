from scripts import sCall

def closePorts():
    sCall("sudo fuser -k 3000/tcp")
    sCall("sudo fuser -k 8080/tcp")

if __name__ == '__main__':
    closePorts()
    sCall("minikube stop")