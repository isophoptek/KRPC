import krpc
import argparse
from time import sleep


def get_current_thrust():
    active_engines = filter(lambda e: e.active and e.has_fuel, vessel.parts.engines)
    thrust = sum(engine.thrust for engine in active_engines)
    return thrust

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--apoapsis", help="Target Apoapsis in meters", type=int, default=350000)
parser.add_argument("-i", "--initialturn", help="Initial turn in degrees", type=int, default=3)
parser.add_argument("-v", "--turnvelocity", help="Velocity to initiate turn at, in seconds", type=int, default=100)
parser.add_argument("-g", "--gracetime", help="Gracetime after initial turn, in seconds", type=int, default=4)
parser.add_argument("-hd", "--heading", help="Heading", type=int, default=90)

# get arguments

args = parser.parse_args()

target_apoapsis = args.apoapsis
turn_initial = args.initialturn
turn_velocity = args.turnvelocity
turn_gracetime = args.gracetime
target_heading = args.heading
g = 9.81

# open connection

try:
    print('Connecting to server...')
    conn = krpc.connect(name='launch_control')

except krpc.error.NetworkError as e:
    print(e)
    print('------------------------------------------------------------')
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

print('getting active vessel...')
vessel = conn.space_center.active_vessel
print('connected to ' + str(vessel.name) + '(' + str(vessel.type) + ')')
print('setting up control uplink...')
control = vessel.control
orbit = vessel.orbit
flight = vessel.flight
ref_frame_vel = vessel.orbit.body.reference_frame
ref_frame = vessel.surface_reference_frame
ap = vessel.auto_pilot
ap.reference_frame = vessel.orbit.body.reference_frame
ap.speedmode = 'surface'

# setup streams

missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
mass = conn.add_stream(getattr, vessel, 'mass')
speed = conn.add_stream(getattr, flight(ref_frame_vel), 'speed')
pitch = conn.add_stream(getattr, flight(ref_frame), 'pitch')
aoa = conn.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
time_to_pe = conn.add_stream(getattr, orbit, 'time_to_periapsis')

# create gui

display = conn.ui
screen_size = display.stock_canvas.rect_transform.size
canvas = display.add_canvas()
panel = canvas.add_panel()
panel.rect_transform.size = (200, 100)
panel.rect_transform.position = (110-(screen_size[0]/2), 0)
gui_message = panel.add_text('Launch Control Running')
gui_message.color = (0, 255, 0)
gui_message.rect_transform.position = (0, -20)

# launch
print('Launch in:')
for t in range(10,0):
    print(t)
print('Launch!')
# spool up engines before release
control.throttle = 1
print('Throttle set to maximum')
control.activate_next_stage()
print('---------')
print('Ignition!')
print('---------')

twr = 0
while twr < 1.25:
    twr = get_current_thrust() / (mass() * g)
    pass
print('TWR reachhed: ' + str(twr))
# release rocket straight up
ap.target_pitch_and_heading = 90, target_heading
ap.engage()
print('autopilot parameters (p,h):')
print(ap.target_pitch_and_heading)
control.activate_next_stage()
print('--------')
print('Release!')
print('--------')
# wait for initial turn
while speed() < turn_velocity:
    pass
print('initial turn')
print('speed: ' + str(speed()))
print('turn_velocity: ' + str(turn_velocity))
# initiate gravity turn, set ap for prograde after gracetime
ap.target_pitch_and_heading = 90 - turn_initial, target_heading
ap.wait()
# ap.sas_mode.stabiltity_assist()
ap.disengage()
ap.sas = True
sleep(turn_gracetime)
print('autopilot parameters (p,h):')
print(ap.target_pitch_and_heading)
print('end of grace time')
ap.target_direction = (0, 1, 0)
print('autopilot set to prograde')
ap.engage()
ap.wait()
print('target vector reached')

# wait for target apoapsis
while apoapsis < target_apoapsis:
    pass
print('ap reached, setting autopilot to zero pitch')

# set pitch to zero
ap.target_pitch_and_heading = 0, target_heading
print('autopilot parameters:')
print(ap.target_pitch_and_heading)

while apoapsis < periapsis:
    pass
print('apoapsis less then periapsis')
control.throttle = 0
print('Throttle set to zero')
print('end of program.')


