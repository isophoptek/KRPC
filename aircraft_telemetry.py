# Telemetry for aircraft

import krpc
import argparse
from time import sleep
from datetime import timedelta
from math import radians

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path fox export")
parser.add_argument("-n", "--polls", help="Number of polls", type=int, default=1)
parser.add_argument("-i", "--interval", help="Interval between polls", type=int, default=1)
args = parser.parse_args()

num_of_polls = args.polls
interval = args.interval
outFile = args.path

conn = krpc.connect(name='Telemetry')
vessel = conn.space_center.active_vessel
ref_frame = vessel.surface_reference_frame
ref_frame_vel = vessel.orbit.body.reference_frame
ref_frame_orbit = vessel.orbital_reference_frame
flight = vessel.flight
orbit = vessel.orbit
display = conn.ui
canvas = display.add_canvas()
panel = canvas.add_panel()
gui_message = panel.add_text('Telemetry log active')
gui_message.color = 255, 0, 0

# add streams
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
time_to_pe = conn.add_stream(getattr, orbit, 'time_to_periapsis')
inclination = conn.add_stream(getattr, orbit, 'inclination')
speed = conn.add_stream(getattr, flight(ref_frame_vel), 'speed')
pitch = conn.add_stream(getattr, flight(ref_frame), 'pitch')
aoa = conn.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
sideslip = conn.add_stream(getattr, flight(ref_frame), 'sideslip_angle')
temp_stat = conn.add_stream(getattr, flight(ref_frame), 'static_air_temperature')
stall_fraction = conn.add_stream(getattr, flight(ref_frame), 'stall_fraction')
drag_coefficient = conn.add_stream(getattr, flight(ref_frame_orbit), 'drag_coefficient')
lift_coefficient = conn.add_stream(getattr, flight(ref_frame_orbit), 'lift_coefficient')
atmo_density = conn.add_stream(getattr, flight(ref_frame), 'atmosphere_density')
dynamic_pressure = conn.add_stream(getattr, flight(ref_frame), 'dynamic_pressure')
mass = conn.add_stream(getattr, vessel, 'mass')
dry_mass = conn.add_stream(getattr, vessel, 'dry_mass')

# open file for write

filename = str(vessel.name) + str(missionelapsedtime()) + "_Telemetry.csv"
filename = str(outFile) + str(filename)

# add header

try:

    with open(filename, mode='a+') as exportFile:
        exportFile.write('MET;')
        exportFile.write('ASL;')
        exportFile.write('Ap;')
        exportFile.write('ToA;')
        exportFile.write('Pe;')
        exportFile.write('ToP;')
        exportFile.write('Inc;')
        exportFile.write('Speed;')
        exportFile.write('Pitch;')
        exportFile.write('AoA;')
        exportFile.write('Sideslip;')
        exportFile.write('Static temp;')
        exportFile.write('Stall;')
        exportFile.write('Drag;')
        exportFile.write('Lift;')
        exportFile.write('Atmospheric Density;')
        exportFile.write('Dynamic Pressure;')
        exportFile.write('Mass;')
        exportFile.write('Dry mass;')
        exportFile.write(';')
        exportFile.write("\n")

    while True:
        line = ("{met};"
                "{asl};"
                "{ap};"
                "{toa};"
                "{pe};"
                "{top};"
                "{inc};"
                "{speed};"
                "{pitch};"
                "{aoa};"
                "{sideslip};"
                "{static_temp};"
                "{stall};"
                "{drag};"
                "{lift};"
                "{atmo_density};"
                "{dyn_pressure};"
                "{mass};"
                "{dry_mass};"
                "\n").format(met=str(timedelta(seconds=int(missionelapsedtime()))),
                             asl=int(meanaltitude()),
                             ap=int(apoapsis()),
                             toa=str(timedelta(seconds=int(time_to_ap()))),
                             pe=int(periapsis()),
                             top=str(timedelta(seconds=int(time_to_pe()))),
                             inc=radians(int(inclination())),
                             speed=int(speed()),
                             pitch=int(pitch()),
                             aoa=int(aoa()),
                             sideslip=int(sideslip()),
                             static_temp=int(temp_stat()),
                             stall=stall_fraction(),
                             drag=drag_coefficient(),
                             lift=lift_coefficient(),
                             atmo_density=atmo_density(),
                             dyn_pressure=int(dynamic_pressure()),
                             mass=int(mass()),
                             dry_mass=int(dry_mass()),)
        with open(filename, mode='a+') as exportFile:
            exportFile.write(line)

        sleep(interval)
except KeyboardInterrupt:
    print('Telementry stream interupted by user.')

# remove streams
missionelapsedtime.remove()
meanaltitude.remove()
apoapsis.remove()
time_to_ap.remove()
periapsis.remove()
time_to_pe.remove()
inclination.remove()
speed.remove()
pitch.remove()
aoa.remove()
sideslip.remove()
temp_stat.remove()
stall_fraction.remove()
drag_coefficient.remove()
lift_coefficient.remove()
mass.remove()
dry_mass.remove()
display.remove()
conn.close()
