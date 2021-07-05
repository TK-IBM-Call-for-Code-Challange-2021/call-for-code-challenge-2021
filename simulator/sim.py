import simpy
import json
import time
import datetime
from pydblite.sqlite import Database, Table
from dateutil import parser
import sys
import click
import paho.mqtt.client as mqtt

env = None#simpy.Environment()

context={}

def get_sim_time(step_time):
    start_time = context['start_time']
    actual_time = start_time + (context['sim_interval_multiplier']*step_time)
    return actual_time


class MQTT:
    def __init__(self, host, port):
        print(f"MQTT: {host} {port}")
        self.client = mqtt.Client()
        self.host = host
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def connect(self):
        self.client.connect(self.host, self.port, 60)
    
    def publish(self, topic, msg):
        self.client.publish(topic, msg)

#class DataStorage:
#    def __init__(self):
#        self.db = Database(":memory:")
#        self.table = Table("sim_data", self.db)
#        self.table.create(("uuid","TEXT"),("watts", "REAL"), ("timestamp", "INTEGER"), ("model","TEXT"), ("appliance_type","TEXT"))
#        self.table.open()
#    
#    def insert(self, record):
#        table.insert(watts=record['watts'], timestamp=record['timestamp'], model=record["model"], appliance_type=record['type'])

class SimulatedObject(object):
    def __init__(self, env, sim_interval=1):
        self.sim_interval = sim_interval
        self.env = env
        self.action = self.env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(self.sim_interval)
            self.custom_process()
            

    def custom_process(self):
        pass

    def get_current_time(self):
        return datetime.datetime.utcfromtimestamp(get_sim_time(self.env.now)).isoformat()


class Appliance(SimulatedObject):
    watthours=0
    def __init__(self, data, env=None, sim_interval=1):
        """
        Simulated Appliance.
        Sim Interval is in minutes
        Is loaded from a data dictionary. See sim_models.json
        """
        self.model = data['model']
        self.watt_per_min = data['watts_per_hour'] / 60.0
        self.appliance_type = data['type']
        super(Appliance, self).__init__(env, sim_interval)
                
    def custom_process(self):
        interval_watts = self.sim_interval * self.watt_per_min
        record = {
            "watts": interval_watts,
            "timestamp": self.get_current_time(),
            "model": self.model,
            "type": self.appliance_type
        }
        print(record)
        self.publish(record)

    def publish(self, record):
        client = context.get('mqtt', None)
        if client is not None:
            client.publish(context['mqtt_topic'], json.dumps(record))

    
class Building(object):
    def __init__(self, env, building_type, appliances):
        self.env = env
        self.appliances = appliances
        self.building_type = building_type


@click.command()
@click.option("--timestamp")
@click.option("--run_iterations")
@click.option("--logfile")
@click.option("--mqtt", default=None)
@click.option("--mqtt_topic", default=None)
@click.option("--sim_interval_multiplier", default=60)
@click.option("--sim_real_time", is_flag=True, default=False)
def main(timestamp, run_iterations, logfile, mqtt, mqtt_topic, sim_interval_multiplier, sim_real_time):
    if not sim_real_time:
        print("Creating normal sim environment")
        env = simpy.Environment()
    else:
        print("Create Realtime Environment")
        env = simpy.rt.RealtimeEnvironment(factor=1)

    context['sim_interval_multiplier'] = sim_interval_multiplier

    if mqtt is not None:
        mqtthost,mqttport = mqtt.split(":")
        mqttport = int(mqttport)
        mqtt_client = MQTT(mqtthost, mqttport)
        mqtt_client.connect()
        context['mqtt_topic']=mqtt_topic
        context['mqtt']=mqtt_client
 
    print("Appliance Simulator")
    from dateutil import parser
    start_date = parser.parse(timestamp)
    context['start_time']=start_date.timestamp()

    sim_model_config = None
    with open("sim_models.json", ) as f:
        sim_model_config = json.load(f)
    print(sim_model_config)

    appliance_dict = {}
    for a in sim_model_config['appliances']:
        appliance_dict[a['id']] = Appliance(a, env=env, sim_interval=a['sim_interval'])

    building = Building(env, "House", [appliance_dict['1'], appliance_dict["2"]])
    print("Starting simulator")
    env.run(until=run_iterations)

if __name__=="__main__":
    main()