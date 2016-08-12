import krpc
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="Target Altitude in maters", type=int, default=15)
args = parser.parse_args()

try:
    print('Connecxting to server as: Hover Control')
    conn = krpc.connect(name='Hover Control')
except krpc.error.NetworkError:
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

vessel = conn.space_center.active_vessel
control = vessel.control
flight = vessel.flight(vessel.orbit.body.reference_frame)

# target = 15
target = args.target  # target altitude above the surface, in meters
print('Target altitude set:' + str(target))
g = 9.81
refresh_freq = 0
while True:
    if refresh_freq == 1:
        os.system('cls')
        print('----------------------------------------')
        print('Target altitude: ' + str(target))
    alt_error = target - flight.surface_altitude
    if refresh_freq == 1:
        print('Current altitude error:' + str(alt_error))

    # compute the desired acceleration:
    #   g   to counteract gravity
    #   -v  to push the vertical speed towards 0
    #   e   to push the altitude error towards 0
    a = g - flight.vertical_speed + alt_error

    # Compute throttle setting using newton's law F=ma
    F = vessel.mass * a
    control.throttle = F / vessel.available_thrust
    if refresh_freq == 1:
        print('----------------------------------------')
        print('Force: ' + str(F))
        print('Throttle: ' + str(control.throttle))
        refresh_freq = 0
    refresh_freq += 0.01
time.sleep(0.01)
