from flask import Flask, request, abort     # pip install flask
import paho.mqtt.client as mqtt             # pip install paho-mqtt
from datetime import datetime               # built-in module
import yaml                                 # pip install pyyaml

BLYNKGO_GBPRIMEPAY_WEBHOOK_VERSION = "2.0.0"



app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        json_str = str(request.json)
        json_str = json_str.replace("{'",  "{\"" )
        json_str = json_str.replace(", '",  ", \"" )
        json_str = json_str.replace(": '",  ": \"" )
        json_str = json_str.replace("',",  "\"," )
        json_str = json_str.replace("':",  "\":" )
        json_str = json_str.replace(": None",  ": null" )        
        # print(json_str+"\n")

        with open("blynkgo_gbprimepay_config.yml", "r") as file:
            config = yaml.safe_load(file)

        MQTT_HOST       = config["MQTT_HOST"]
        MQTT_PORT       = config["MQTT_PORT"]
        MQTT_PAID_TOPIC = config["MQTT_PAID_TOPIC"]
        WEBHOOK_LOG     = config["WEBHOOK_LOG"]
        WEBHOOK_PORT    = config["WEBHOOK_PORT"]

        # Get the current date and time
        now = datetime.now()
        # Format the date and time to a string
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # Append the date and time to the webhook data
        webhook_data_log = current_time + ' : ' + json_str
        print(webhook_data_log)

        if(WEBHOOK_LOG):
            with open("webhook_data.log", "a", encoding="utf-8") as f:
                f.write(webhook_data_log + '\n')


        # Connect to the MQTT broker
        client = mqtt.Client()
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.publish(MQTT_PAID_TOPIC, json_str +'\n')
        client.disconnect()
        
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    with open("blynkgo_gbprimepay_config.yml", "r") as file:
        config = yaml.safe_load(file)
    WEBHOOK_PORT    = config["WEBHOOK_PORT"]
    app.run(port=WEBHOOK_PORT, debug =True)
