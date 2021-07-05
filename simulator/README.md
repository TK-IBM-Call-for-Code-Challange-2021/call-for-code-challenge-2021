Running the Sim
===============

@click.command()
@click.option("--timestamp")    - Starting Timestamp
@click.option("--run_iterations")  - How many iterations to run for
@click.option("--logfile")         - Where to log to #Not working
@click.option("--mqtt", default=None) - host:port for mqtt
@click.option("--mqtt_topic", default=None) - publish topic
@click.option("--sim_interval_multiplier", default=60) 60=1hour time steps. 1 = 1 minute timestamp
