Running the Sim
===============

@click.command()
@click.option("--timestamp")    - Starting Timestamp
@click.option("--run_iterations")  - How many iterations to run for
@click.option("--logfile")         - Where to log to #Not working
@click.option("--mqtt", default=None) - host:port for mqtt
@click.option("--mqtt_topic", default=None) - publish topic
@click.option("--sim_interval_multiplier", default=60) 60=1hour time steps. 1 = 1 minute timestamp


python sim.py --timestamp="2020-09-01T01:01:01Z" --run_minutes=50000 --mqtt=call-for-code.wop.al:1883 --mqtt_topic=testsim