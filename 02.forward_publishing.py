import requests
import paho.mqtt.client as mqtt   # pip install paho-mqtt
import time
import json
import socket
import yaml                                 # pip install pyyaml

FORWARD_PUBLISHING_VERSION = "2.0.0"


def getIP():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  IP = s.getsockname()[0]
  s.close()
  return IP

while True:
  with open("blynkgo_gbprimepay_config.yml", "r") as file:
    config = yaml.safe_load(file)

  MQTT_HOST                     = config["MQTT_HOST"]
  MQTT_PORT                     = config["MQTT_PORT"]
  MQTT_TUNNEL_TOPIC             = config["MQTT_TUNNEL_TOPIC"]
  MQTT_LINE_TUNNEL_TOPIC        = config["MQTT_LINE_TUNNEL_TOPIC"]
  MQTT_TUNNEL_UPDATE_INTERVAL   = config["MQTT_TUNNEL_UPDATE_INTERVAL"]
  WEBHOOK_LOG                   = config["WEBHOOK_LOG"]


  url = "http://localhost:4040/api/tunnels"
  response = requests.get(url)

  # Check for successful response
  if response.status_code == 200:
      json_string = response.text

      IP = getIP()
      json_string = json_string.replace("localhost", IP) 

      # Parse the JSON string
      json_data = json.loads(json_string)
      # Find the desired data
      for tunnel in json_data["tunnels"]:
          if tunnel["name"] == "gbprimepay":
              json_string = '{"tunnels":[' + json.dumps(tunnel) + '],"uri":"/api/tunnels"}\n'
          elif tunnel["name"] == "line":
              json_line_tunnel_string = '{"tunnels":[' + json.dumps(tunnel) + '],"uri":"/api/tunnels"}\n'
              # Create MQTT client
              client_line = mqtt.Client()
              client_line.connect(MQTT_HOST, MQTT_PORT)
              # Publish response text to topic
              client_line.publish(MQTT_LINE_TUNNEL_TOPIC, json_line_tunnel_string, retain=True)
              client_line.disconnect()

      with open("tunnels.txt", "w") as f:
          f.write(json_string)

      # Create MQTT client
      client = mqtt.Client()
      client.connect(MQTT_HOST, MQTT_PORT)
      # Publish response text to topic
      client.publish(MQTT_TUNNEL_TOPIC, json_string, retain=True)
      client.disconnect()
  else:
      print(f"Request failed with status code: {response.status_code}")

  time.sleep(MQTT_TUNNEL_UPDATE_INTERVAL)
