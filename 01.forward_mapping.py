import os
import sys
import socket
import platform
import yaml                                 # pip install pyyaml

FORWARD_MAPPING_VERSION = "2.0.0"

with open("blynkgo_gbprimepay_config.yml", "r") as file:
    config = yaml.safe_load(file)

NGROK_AUTH_TOKEN       = config["NGROK_AUTH_TOKEN"]

ngrok_yaml_string = f'''
version: "2"
authtoken: {NGROK_AUTH_TOKEN}
tunnels:
  gbprimepay:
    proto: http
    addr: 12345
  line:
    proto: http
    addr: 6789
'''

with open("ngrok.yml", "w") as f:
    f.writelines(ngrok_yaml_string)


if platform.system() == "Windows":
  # os.system(f'start /min cmd /c ngrok start --all --config=ngrok.yml');
  # os.system(f'start /min cmd /c python 03.webhook_server.py')
  os.system(f'start cmd /c ngrok start --all --config=ngrok.yml');
  os.system(f'start /b cmd /c python 03.webhook_server.py')
elif platform.system() == "Linux":
  # os.system("xterm -iconic -e 'ngrok start --all --config=ngrok.yml'")
  # os.system("xterm -iconic -e 'python 03.webhook_server.py'")
  os.system("xterm -e 'ngrok start --all --config=ngrok.yml'")
  os.system("xterm -e 'python 03.webhook_server.py'")

import time
time.sleep(10)
os.system('start /b cmd /c python 02.forward_publishing.py')
