#!/usr/bin/python3
import urllib.request
import io
import os
from tld import get_tld

def GetIPAddress(url):
    LinuxCommand = "host " + url
    StartProcess = os.popen(LinuxCommand)
    results = str(StartProcess.read())
    marking = results.find('has address') + 12
    return results[marking:].splitlines()[0]

def GetDomainName(url):
    DomainName = get_tld(url)
    print(GetIPAddress(DomainName))
    return DomainName

def GetRobots(url):
    print(GetDomainName(url))
    if url.endswith("/"):
        path = url
    else:
        path = url + "/"
    requestingData = urllib.request.urlopen(path + "robots.txt", data=None)
    data = io.TextIOWrapper(requestingData, encoding ="utf 8")
    return data.read()

print(GetRobots("https://peterm.wordpress.com/"))


