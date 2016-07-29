# DataGrabber for KSP

# (C) Snieder Marton

import sys
import krpc
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("outfile", help="Output filename")
parser.add_argument("-n", "--polls", help="Number of polls", type=int, default=1)
args = parser.parse_args()

# connect to server

conn = krpc.connect(name='DataGrab')

# create data streams

vessel = conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame
position = conn.add_stream(vessel.position, refframe)
apoapsis = conn.add_stream(vessel.orbit.apoapsis_altitude)
periapsis = conn.add_stream(vessel.orbit.periapsis_altitude)
currentbody = conn.add_stream(vessel.orbit.body)
inclination = conn.add_stream(vessel.orbit.inclination)
missionelapsedtime = conn.add_stream(vessel.met)
currentgforce = conn.add_stream(vessel.flight.g_force)
meanaltitude = conn.add_stream(vessel.flight.mean_altitude)
terminalvelocity = conn.add_stream(vessel.flight.terminal_velocity)

# poll loop
num_of_polls = args.polls
poll = 0

while poll < num_of_polls:
    # TODO get data values
    # TODO write to file
    poll += 1

print("Cycle done")
