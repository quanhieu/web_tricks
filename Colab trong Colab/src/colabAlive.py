#Only use for google colab
#@markdown <center><h3>Colab alive and vnc</h3></center><br>
import os,sys
import random
import string
import urllib.request
from IPython.display import HTML, clear_output
import time

#####################################
USE_FREE_TOKEN = True # @param {type:"boolean"}
TOKEN = ""  # @param {type:"string"}
BROWSER_FILE = "colab_miniwebbrowser.py" # @param {type:"string"}
HOME = os.path.expanduser("~")
system_raw = get_ipython().system_raw

if not os.path.exists(f"{HOME}/.ipython/ttmg.py"):
    hCode = "https://raw.githubusercontent.com/helloW3c/" \
                "Google-Colab-CloudTorrent/master/res/ttmg.py"
    urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ttmg.py")

from ttmg import (
    runSh,
    loadingAn,
    PortForward_wrapper,
    displayUrl,
    findProcess,
    textAn,
)

loadingAn()

def serviceColabAlive():
  data = f'''
#!/bin/bash
while true; do
  if ! pgrep -x "Xvfb" > /dev/null
  then
    Xvfb :99 -br -nolisten tcp -screen 0 1280x720x24 &
  fi
  if ! pgrep -f "python3 {BROWSER_FILE}" > /dev/null
  then
    export DISPLAY=:99
    python3 {BROWSER_FILE} &
  fi
  sleep 30
done
  '''
  with open("serviceColabAlive.sh", "w") as f: f.write(data)
  system_raw("bash serviceColabAlive.sh &")

def autoResetBrowser():
  data = f'''
#!/bin/bash
while true; do
  sleep 3600
  pkill -f "python3 {BROWSER_FILE}"
  export DISPLAY=:99
  python3 {BROWSER_FILE} &
done
  '''
  with open("autoResetBrowser.sh", "w") as f: f.write(data)
  system_raw("bash autoResetBrowser.sh &")

if not findProcess("python3", BROWSER_FILE):
  !pip3 install PyQt5==5.14.1 PyQtWebEngine==5.14.0
  !apt install xvfb xfonts-base
  serviceColabAlive()
  autoResetBrowser()

# password ganarate
VNC_PASSWORD = '12345'
#Install and Start vnc server
if not findProcess("x11vnc"):
  textAn("Wait for almost 60 seconds. It's doing for VNC ready ...")
  os.makedirs(f'{HOME}/.vnc', exist_ok=True)
  system_raw('apt update -y')
  system_raw('apt install x11vnc')
  system_raw(rf'echo "{VNC_PASSWORD}" | vncpasswd -f > ~/.vnc/passwd')
  os.chmod(f'{HOME}/.vnc/passwd', 0o400)
  runSh('x11vnc -display :99 -forever -loop -noxdamage -repeat -shared &', shell=True)

# github latest releases tag define
def latestTag(link):
  import re
  from urllib.request import urlopen
  htmlF = urlopen(link+"/releases/latest").read().decode('UTF-8')
  return re.findall(r'.+\/tag\/([.0-9A-Za-z]+)".+/', htmlF)[0]

# Install and start vnc client
if not findProcess("easy_novnc"):
  os.makedirs("tools/noVnc", exist_ok=True)
  BASE_URL = "https://github.com/geek1011/easy-novnc"
  LATEST_TAG = latestTag(BASE_URL)
  output_file = "tools/noVnc/easy_novnc"
  urlF = f"{BASE_URL}/releases/download/{LATEST_TAG}/easy-novnc_linux-64bit"
  try:
    urllib.request.urlretrieve(urlF, output_file)
  except OSError:
    pass
  os.chmod(output_file, 0o755)
  cmdDo = "./easy_novnc --addr 0.0.0.0:6080 --port 5900 &"
  runSh(cmdDo, cd="tools/noVnc/", shell=True)

# Start ngrok and forward traffic
Server = PortForward_wrapper("ngrok", TOKEN, USE_FREE_TOKEN, 
                             [['vnc', 6080, 'http']], 'us', 
                             [f"{HOME}/.ngrok2/noVncFast.yml", 4455])

data = Server.start('vnc', displayB=False)
clear_output()
displayUrl(data, pNamU='noVnc : ',
            EcUrl=f'/vnc.html?autoconnect=true&password={VNC_PASSWORD}&path=vnc&resize=scale&reconnect=true&show_dot=true')