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

print('Argument parsed:')
print('path set to: ' + str(outFile))
print('polling interval: ' + str(interval))
print('opening connection...')

conn = krpc.connect(name='Engine Telemetry')
print('getting active vessel...')
vessel = conn.space_center.active_vessel
print('setting up control uplink...')
control = vessel.control

display = conn.ui
screen_size = display.stock_canvas.rect_transform.size
canvas = display.add_canvas()
panel = canvas.add_panel()
panel.rect_transform.size = (200, 100)
panel.rect_transform.position = (110-(screen_size[0]/2), 0)
gui_message = panel.add_text('Telemetry log active')
gui_message.color = (0, 255, 0)
gui_message.rect_transform.position = (0, -20)
stop_button = panel.add_button("Stop transmission")
stop_button.rect_transform.position = (0, 20)
stop_button_clicked = conn.add_stream(getattr, stop_button, "clicked")

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
engine_has_fuel = conn.add_stream(getattr, engine, 'has_fuel')
engine_throttle_stream = conn.add_stream(getattr, engine, 'throttle')

# open file for write
print('setting up export...')
filename = str(vessel.name) + "_" + str(missionelapsedtime()) + "_Telemetry.csv"
filename = str(outFile) + str(filename)

try:
    print('writing file header...')
    with open(filename, mode='a+') as exportFile:
        exportFile.write('MET;')
        exportFile.write('ACTIVE;')
        exportFile.write('THRUST;')
        exportFile.write('AVAILABLE_THRUST;')
        exportFile.write('MAX_THRUST;')
        exportFile.write('MAX_VACUUM_THRUST;')
        exportFile.write('SPECIFIC_IMPULSE;')
        exportFile.write('VACUUM_SPECIFIC_IMPULSE;')
        exportFile.write('PROPELLANT_NAMES;')
        exportFile.write('PROPELLANT_RATIOS;')
        exportFile.write('HAS_FUEL;')
        exportFile.write('THROTTLE;')
        exportFile.write("\n")

    # control.throttle = 0
    # print('throttle set to zero')
    print('countdown:')
    for t in range(10, 0, 1):
        print(t)
        sleep(1)
    print('throttle set to maximum')
    control.throttle = 1
    print('stage')
    control.activate_next_stage()

# write content
    print('sending data...')
    while True:
        if stop_button_clicked():
            print('STOP signal recieved.')
            print('Telementry stream interupted by user. (stop_button_clicked)')
            break
        engine_propellant_name_list = ''
        ###
        ### for prop in engine_propellant_names:
        ### engine_propellant_name_list += prop
        ###
        line = ("{met};"
                "{active};"
                "{thrust};"
                "{available_thrust};"
                "{max_thrust};"
                "{max_vacuum_thrust};"
                "{specific_impulse};"
                "{vacuum_specific_impulse};"
                "{propellant_names};"
                "{propellant_ratios};"
                "{has_fuel};"
                "{throttle};"
                "\n").format(met=str(timedelta(seconds=int(missionelapsedtime()))),
                             active=engine_is_active(),
                             thrust=engine_thrust(),
                             available_thrust=engine_available_thrust(),
                             max_thrust=engine_max_thrust(),
                             max_vacuum_thrust=engine_max_vacuum_thrust(),
                             specific_impulse=engine_specific_impulse(),
                             vacuum_specific_impulse=engine_vacuum_specific_impulse(),
                             propellant_names=engine_propellant_names(),
                             propellant_ratios=engine_propellant_ratios(),
                             has_fuel=engine_has_fuel(),
                             throttle=engine_throttle_stream())
        with open(filename, mode='a+') as exportFile:
            exportFile.write(line)

        sleep(interval)
except KeyboardInterrupt:
    print('Telementry stream interupted by user. (keyboardinterupt)')
finally:
    print('ending dataloop...')
    control.throttle = 0
    print('throttle set to zero')
    print('closing streams...')
    missionelapsedtime.remove()
    engine_is_active.remove()
    engine_thrust.remove()
    engine_available_thrust.remove()
    engine_max_thrust.remove()
    engine_max_vacuum_thrust.remove()
    engine_specific_impulse.remove()
    engine_vacuum_specific_impulse.remove()
    engine_propellant_names.remove()
    engine_propellant_ratios.remove()
    engine_has_fuel.remove()
    engine_throttle_stream.remove()
    print('closing connection...')
    conn.close()

print('streams and connection closed.')


