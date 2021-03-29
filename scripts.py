import subprocess as sb

def sCall(cmd):
    return sb.call(cmd, shell=True)

def sReturn(cmd):
    return sb.check_output(cmd, shell=True)