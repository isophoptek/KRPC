# Telemetry for engine test rigs

# requies FAR
# single engine setups only

import krpc
import argparse
from time import sleep
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path for export")
parser.add_argument("-i", "--interval", help="Interval between polls", type=int, default=1)
args = parser.parse_args()

interval = args.interval
outFile = args.path

conn = krpc.connect(name='Engine Telemetry')
vessel = conn.space_center.active_vessel
control = vessel.control

engine = vessel.parts.engines[0]

# add streams
print('setting up datastreams...')
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
engine_is_active = conn.add_stream(getattr, engine, 'active')
engine_thrust = conn.add_stream(getattr, engine, 'thrust')
engine_available_thrust = conn.add_stream(getattr, engine, 'available_thrust')
engine_max_thrust = conn.add_stream(getattr, engine, 'max_thrust')
engine_max_vacuum_thrust = conn.add_stream(getattr, engine, 'max_vacuum_thrust')
engine_specific_impulse = conn.add_stream(getattr, engine, 'specific_impulse')
engine_vacuum_specific_impulse = conn.add_stream(getattr, engine, 'vacuum_specific_impulse')
engine_propellant_names = conn.add_stream(getattr, engine, 'propellant_names')
engine_propellant_ratios = conn.add_stream(getattr, engine, 'propellant_ratios')
engine_throttle = conn.add_stream(getattr, engine, 'throttle')
