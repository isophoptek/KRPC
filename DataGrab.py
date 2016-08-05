# DataGrabber for KSP

# (C) Snieder Marton

# original idea by Alexander Korsunsky

import time
import krpc
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path fox export")
parser.add_argument("-n", "--polls", help="Number of polls", type=int, default=1)
parser.add_argument("-i", "--interval", help="Interval between polls", type=int, default=1)
parser.add_argument("-c", "--continuous", help="Continuous", action='store_true')
args = parser.parse_args()

# argument interpretation

num_of_polls = args.polls
interval = args.interval
continuous = args.continuous
outFile = args.path


def sectionheader(sectiontitle):
    print('----------------------------------------')
    print(sectiontitle)
    print('----------------------------------------')

# connect to server
sectionheader('Seeking server')

try:
    print('Connecting to server...')
    conn = krpc.connect(name='DataGrab')

except krpc.error.NetworkError as e:
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

# create data streams
sectionheader('setting up streams')
vessel = conn.space_center.active_vessel
ref_frame = vessel.surface_reference_frame
orbit = vessel.orbit
flight = vessel.flight
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
print('apoapsis: (%.2f)' % apoapsis())
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
print('periapsis: (%.2f)' % periapsis())
currentbody = conn.add_stream(getattr, orbit.body, 'name')
print('current body: ' + str(currentbody()))
inclination = conn.add_stream(getattr, orbit, 'inclination')
print('inclination: (%.3f)' % inclination())
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
print('mission elapsed time: ' + datetime.timedelta(seconds=int(missionelapsedtime())))
currentgforce = conn.add_stream(getattr, flight(ref_frame), 'g_force')
print('current g force: (%.2f)' % currentgforce())
meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
print('mean altitude: (%.2f)' % meanaltitude())
terminalvelocity = conn.add_stream(getattr, flight(ref_frame), 'terminal_velocity')
print('terminal velocity: (%.2f)' % terminalvelocity())

# export file definition

sectionheader('Writing file')

if num_of_polls == 1:
    fileName = "SinglePoll_" + str(vessel.name) + "_" + str(vessel.situation) + "_" + str(missionelapsedtime()) + ".csv"
else:
    fileName = "PollLog_" + str(vessel.name) + "_" + str(missionelapsedtime()) + ".csv"

outFile = str(outFile) + str(fileName)
# outFile = "d:\pycharm\datagrab.csv"

# poll loop

poll = 0
with open(outFile, mode='a+') as exportFile:
    exportFile.write('UT,')
    exportFile.write('MET,')
    exportFile.write('Current Body,')
    exportFile.write('Apoapsis,')
    exportFile.write('Periapsis,')
    exportFile.write('Inclination,')
    exportFile.write('MeanAltitude,')
    exportFile.write('G Force,')
    exportFile.write('Terminal Velocity,')
    exportFile.write('TWR,')
    exportFile.write('Stage dV,')
    exportFile.write('Total dV,')
    exportFile.write("\n")

    while poll < num_of_polls:
        line = ("{ut},"
                "{met},"
                "{body},"
                "{apo},"
                "{peri},"
                "{inc},"
                "{mean_alt},"
                "{gforce},"
                "{vt},"
                "{twr},"
                "{stagedv},"
                "{totaldv},"
                "\n").format(ut=str(datetime.timedelta(seconds=int(conn.space_center.ut))),
                             met=str(datetime.timedelta(seconds=int(missionelapsedtime()))),
                             body=currentbody(),
                             apo=int(apoapsis()),
                             peri=int(periapsis()),
                             inc=int(inclination()),
                             mean_alt=int(meanaltitude()),
                             gforce=int(currentgforce()),
                             vt=terminalvelocity(),
                             twr=vessel.available_thrust,
                             stagedv="",
                             totaldv="", )
        poll += 1
        print('Current poll value: ' + str(poll))
        print('Poll limit: ' + str(num_of_polls))
        if continuous:
            poll -= 1
            print('Continuous flag active')
        print('Sleep with interval: ' + str(interval))
        time.sleep(interval)
        # TODO get deltaV data

        # TODO write to file
        exportFile.write(line)

# poll += 1
# time.sleep(1)
# TODO poll interval optional parameter
print("Cycle(s) done")

exportFile.close()

# remove streams

sectionheader('Closing streams')

apoapsis.remove()
periapsis.remove()
currentbody.remove()
inclination.remove()
missionelapsedtime.remove()
currentgforce.remove()
meanaltitude.remove()
terminalvelocity.remove()
