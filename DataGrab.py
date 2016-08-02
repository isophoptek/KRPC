# DataGrabber for KSP

# (C) Snieder Marton

# original idea by Alexander Korsunsky

import time
import krpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path fox export")
parser.add_argument("-n", "--polls", help="Number of polls", type=int, default=1)
args = parser.parse_args()

# argument interpretation

# num_of_polls = args.polls
num_of_polls = 1
outFile = args.path

# connect to server
try:
    print('Connecting to server...')
    conn = krpc.connect(name='DataGrab')

except krpc.error.NetworkError as e:
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

# create data streams

vessel = conn.space_center.active_vessel
ref_frame = vessel.surface_reference_frame
orbit = vessel.orbit
flight = vessel.flight
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
print('apoapsis: ' + str(apoapsis()))
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
print('periapsis: ' + str(periapsis()))
currentbody = conn.add_stream(getattr, orbit, 'body')
print('current body: ' + str(currentbody()))
inclination = conn.add_stream(getattr, orbit, 'inclination')
print('inclination: ' + str(inclination()))
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
print('mission elapsed time: ' + str(missionelapsedtime()))
currentgforce = conn.add_stream(getattr, flight(ref_frame), 'g_force')
print('current g force: ' + str(currentgforce()))
meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
print('mean altitude: ' + str(meanaltitude()))
terminalvelocity = conn.add_stream(getattr, flight(ref_frame), 'terminal_velocity')
print('terminal velocity: ' + str(terminalvelocity()))

# export file definition

if num_of_polls == 1:
    fileName = "SinglePoll_" + str(vessel.name) + "_" + str(vessel.situation) + "_" + str(missionelapsedtime()) + ".csv"
else:
    fileName = "PollLog_" + str(vessel.name) + "_" + str(missionelapsedtime()) + ".csv"

# outFile += fileName
outFile = "d:\pycharm\datagrab.csv"

# poll loop

poll = 0
with open(outFile, mode='a') as exportFile:
    exportFile.write('UT /n')
    #                  "MET",
    #                  "Current Body",
    #                  "Apoapsis",
    #                  "Periapsis",
    #                  "Inclination",
    #                  "MeanAltitude",
    #                  "G Force",
    #                  "Terminal Velocity",
    #                  "TWR",
    #                  "Stage dV",
    #                  "Total dV",
    #                  "/n")

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
                "/n").format(ut=conn.space_center.ut,
                             met=missionelapsedtime(),
                             body=currentbody,
                             apo=apoapsis,
                             peri=periapsis,
                             inc=inclination,
                             mean_alt=meanaltitude,
                             gforce=currentgforce,
                             vt=terminalvelocity,
                             twr=vessel.available_thrust,
                             stagedv="",
                             totaldv="", )
        poll += 1
        time.sleep(1)
        # TODO get deltaV data

        # TODO write to file
        exportFile.write(line)

# poll += 1
# time.sleep(1)
# TODO poll interval optional parameter
print("Cycle(s) done")

exportFile.close()

# remove streams

conn.remove_stream(apoapsis)
conn.remove_stream(periapsis)
conn.remove_stream(currentbody)
conn.remove_stream(inclination)
conn.remove_stream(missionelapsedtime)
conn.remove_stream(currentgforce)
conn.remove_stream(meanaltitude)
conn.remove_stream(terminalvelocity)
