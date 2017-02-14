import krpc
from time import sleep
from datetime import timedelta
from math import radians

print('Seeking connection, please ensure server is running...')
conn = krpc.connect(name='telemetry')

vessel = conn.space_center.active_vessel
ref_frame = vessel.surface_reference_frame
orbit = vessel.orbit
flight = vessel.flight
control = vessel.control

path = None
interval = 1

print('Output path:')
print(path)
print('Polling interval:')
print(interval)

# add streams
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
currentgforce = conn.add_stream(getattr, flight(ref_frame), 'g_force')
meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
surfacealtitude = conn.add_stream(getattr, flight(ref_frame), 'surface_altitude')
speed = conn.add_stream(getattr, flight(ref_frame), 'speed')
verticalspeed = conn.add_stream(getattr, flight(ref_frame), 'vertical_speed')
pitch = conn.add_stream(getattr, flight(ref_frame), 'pitch')
heading = conn.add_stream(getattr, flight(ref_frame), 'heading')
atmo_density = conn.add_stream(getattr, flight(ref_frame), 'atmosphere_density')
mach = conn.add_stream(getattr, flight(ref_frame), 'mach')
terminalvelocity = conn.add_stream(getattr, flight(ref_frame), 'terminalvelocity')
aoa = conn.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
sideslip = conn.add_stream(getattr, flight(ref_frame), 'sideslip_angle')
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
time_to_pe = conn.add_stream(getattr, orbit, 'time_to_periapsis')
inclination = conn.add_stream(getattr, orbit, 'inclination')
throttle = conn.add_stream(getattr, control, 'throttle')
currentstage = conn.add_stream(getattr, control, 'current_stage')

filename = str(vessel.name) + "_Log.csv"
filename = str(path) + str(filename)
print('Generated output path:')
print(filename)

with open(filename, mode='a+') as exportFile:
    exportFile.write('MET,')
    exportFile.write('G Force,')
    exportFile.write('ASL,')
    exportFile.write('AGL,')
    exportFile.write('Speed,')
    exportFile.write('V Speed,')
    exportFile.write('Pitch,')
    exportFile.write('Heading,')
    exportFile.write('Atmo density,')
    exportFile.write('Mach,')
    exportFile.write('Termival V,')
    exportFile.write('AoA,')
    exportFile.write('AoS,')
    exportFile.write('Ap,')
    exportFile.write('ToA,')
    exportFile.write('Pe,')
    exportFile.write('ToP,')
    exportFile.write('Inc,')
    exportFile.write('Throttle,')
    exportFile.write('Stage,')
    exportFile.write("\n")
try:
    while True:
        exportFile.write(line)
        line = ("{met},"
                "{g_force},"
                "{asl},"
                "{agl},"
                "{speed},"
                "{v_speed},"
                "{pitch},"
                "{heading},"
                "{atmo_density},"
                "{mach},"
                "{terminal_v},"
                "{aoa},"
                "{aos},"
                "{ap},"
                "{toa},"
                "{pe},"
                "{top},"
                "{inc},"
                "{throttle},"
                "{stage},"
                "\n").format(met=str(timedelta(seconds=int(missionelapsedtime))),
                             g_force=int(currentgforce()),
                             asl=int(meanaltitude()),
                             agl=int(surfacealtitude()),
                             speed=int(speed()),
                             v_speed=int(verticalspeed()),
                             pitch=int(pitch()),
                             heading=int(heading()),
                             atmo_density=int(atmo_density()),
                             mach = int(mach()),
                             terminal_v=int(terminalvelocity()),
                             aoa=int(aoa()),
                             aos=int(sideslip()),
                             ap=int(apoapsis()),
                             toa=str(timedelta(seconds=int(time_to_ap))),
                             pe=int(periapsis()),
                             top=str(timedelta(seconds=int(time_to_pe))),
                             inc=radians(int(inclination())),
                             throttle=int(throttle()),
                             stage=int(currentstage()),)
        sleep(interval)
except KeyboardInterrupt:
    print('Interupted')

exportFile.close()

missionelapsedtime.remove()
currentgforce.remove()
meanaltitude.remove()
surfacealtitude.remove()
speed.remove()
verticalspeed.remove()
pitch.remove()
heading.remove()
atmo_density.remove()
mach.remove()
terminalvelocity.remove()
aoa.remove()
sideslip.remove()
apoapsis.remove()
time_to_ap.remove()
periapsis.remove()
time_to_pe.remove()
inclination.remove()
throttle.remove()
currentstage.remove()
conn.close()
