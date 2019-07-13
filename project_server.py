from machine import Pin,PWM
from time import sleep
from _thread import start_new_thread as thread
import network
import urequests
import json
ssid = "exceed16_8"
pwd = "12345678"
station = network.WLAN(network.STA_IF)
station.active(True)
#station.connect(ssid,pwd)
data = 0

url = "https://exceed.superposition.pknn.dev/data/pangpond"
data = {"temp":34,"type":12}
headers = {"Content-Type":"application/json"}

BTN = 19
btn = Pin(BTN,Pin.IN)

GMT0time=0
"""
#################################
def get_local():
  global local_hour
  global GMT0time
  try:
    import usocket as socket
  except:
    import socket
  try:
    import ustruct as struct
  except:
    import struct

  # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
  NTP_DELTA = 3155673600
  LAST_NTP = NTP_DELTA

  host = "th.pool.ntp.org"

  def time():
    global LAST_NTP
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    if val != 0:
      LAST_NTP = val
    else:
      val = LAST_NTP
    return val - NTP_DELTA

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())

  def settime():
    global GMT0time
    t = time()
    import machine
    import utime
    tm = utime.localtime(t)
    print(tm)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    print(tm,1)
    machine.RTC().datetime(tm)
    GMT0time = utime.localtime()
"""


##################################################################

task = []
time = []
category = []
task_now = []
count = 0
last_dict_from_web = ""

def sound_after_1_count():
  buzzer = 0
  for i in range(2):
    buzzer = PWM(Pin(25))
    buzzer.freq(10)
    sleep(1)
  buzzer.deinit()

def check_category():
  for i in range(len(category)):
    if category[i] == 1 and time[i] - local_hour == 1:
      print(category[i])
      task_now.append(category[i])
    elif category[i] == 2 and time[i] == local_hour:
      print(category[i])
      task_now.append(category[i])
    if time[i] > localtime:
      task_now.remove(category[i])
      category.pop(i)

def switch():
  while(1):
    while btn.value() == 0:
      if btn.value() == 1:
        if count == 1:
          sound_after_1_count()
          break
        count = count + 1
        print(task_now)
        break
      sleep(0.01)

def WIFICheck():
  if not station.isconnected():
    station.connect(ssid,pwd)
    print("Connecting...")
    while not station.isconnected():
      sleep(0.5)
    if station.isconnected():
      print("Connected")

def WIFIMon():
  while True:
    WIFICheck()
    sleep(5)
  
def import_from_web():
  while True:
    global dict_from_web
    dict_from_web = urequests.get(url).json()
    #print(dict_from_web)
    global count
    global last_dict_from_web
    global task
    global time
    global category
    global now_hour
    global task_now
    global GMT0time
    global local_hour
    #while dict_from_web:
    task = dict_from_web["task"]
    time = dict_from_web["time"]
    category = dict_from_web["category"]
    GMT0time = dict_from_web["current time"]
    if GMT0time > 16:
      local_hour = (GMT0time+7) - 24
    else :
      local_hour = GMT0time + 7
  sleep(10)


"""  
def sent_back():
  js = json.dumps({"data":data})
  r = urequest.post(url,data=js,headers = headers)
  result = r.json()
  print(result)
"""  
  
########## Main ##########
WIFICheck()
thread(WIFIMon, ())
#thread(get_local, ())
thread(import_from_web, ())
thread(check_category, ())
thread(switch, ())

while True:
  print("GMT :", GMT0time)
  #print("local_hour :", local_hour)
  print("task :", task)
  print("category :", category)
  print("time :",time)
  print("current times", GMT0time)
  print(task_now)
  print(dict_from_web)
  sleep(3)

