import krpc
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="Target Altitude in maters", type=int, default=15)
args = parser.parse_args()

conn = krpc.connect()
vessel = conn.space_center.active_vessel
control = vessel.control
flight = vessel.flight(vessel.orbit.body.reference_frame)

# target = 15
target = args.target  # target altitude above the surface, in meters
g = 9.81
while True:

    alt_error = target - flight.surface_altitude

    # compute the desired acceleration:
    #   g   to counteract gravity
    #   -v  to push the vertical speed towards 0
    #   e   to push the altitude error towards 0
    a = g - flight.vertical_speed + alt_error

    # Compute throttle setting using newton's law F=ma
    F = vessel.mass * a
    control.throttle = F / vessel.available_thrust

time.sleep(0.01)